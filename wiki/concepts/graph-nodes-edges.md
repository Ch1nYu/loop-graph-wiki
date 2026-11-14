---
id: graph-nodes-edges
title: "Graph 的基本元素：節點、邊、條件邊、狀態"
type: concept
audience: beginner
updated: 2026-11-13
sources: [week10-lecture, langgraph-agents-course, agentic-workflow-humaneval, ai-agent-system-design-course]
related: [fallback-edges, state-as-files, harness-loop-graph]
---

# Graph 的基本元素：節點、邊、條件邊、狀態

> 一句話：節點是「誰做事」，邊是「下一步去哪裡」，條件邊是「依什麼決定」，狀態是「做到哪裡」。

## 從圖論看三種結構

課程用圖論把 Prompt、Loop、Graph 放在同一個框架裡（[[sources/week10-lecture]] §3.3）：

1. **Prompt**：只有一個節點 `A`，跑一次就結束。
2. **Loop**：一個節點 `A`，加一條回到自己的邊（`A ↺`）。
3. **Graph**：多個節點（`A → B → C`），加上條件分支與退回邊。

這個視角的好處是：你不會把 Graph 想成「比較高級的 Loop」，而會看到它們的結構差異——Graph 多了**多節點**與**條件邊**，因此可以分工、可以並行、可以精準退回。

## 四個基本元素

### 節點（Node）

節點是一個處理單元，可以是一個 LLM 呼叫、一個工具、一個 Python 函式，或一個人工審核關卡。LangGraph 的節點可以是 `call_model`、`action`、`planner`、`generate` 等（[[sources/langgraph-agents-course]] §Agentic Workflow 基礎）。

節點的設計原則是**單一職責**：一個節點只做一件事，輸入與輸出都是明確的檔案或狀態欄位。例如「抽證據卡」只負責從單篇來源抽卡，不負責寫大綱。

### 邊（Edge）

邊是固定的流向：`A → B` 表示 A 完成後一定去 B。邊讓流程可預測，也讓「不能跳關」變成結構上的保證（[[sources/week10-lecture]] §3.3）。

### 條件邊（Conditional Edge）

條件邊是決策分流：依某個條件決定去哪裡。例如「覆蓋率 < 3 頁 → 停止；否則 → 抽證據卡」（[[sources/langgraph-agents-course]] §Agentic Workflow 基礎）。

條件邊是 Graph 的靈魂：沒有條件邊，Graph 只是一條 pipeline；有條件邊，才能做分支、重試與退回。

### 狀態（State）

狀態是流程的記憶體：目前做到哪一關、已經通過哪些檢查、有哪些檔案。LangGraph 用 `TypedDict` 定義 State，用 `Annotated[..., operator.add]` 讓訊息累加，未標註的欄位則覆寫（[[sources/langgraph-agents-course]] §Agentic Workflow 基礎）。

狀態可以是記憶體中的物件，也可以是檔案（State as Files）。本專案採用後者：每個節點的產出都是執行資料夾下的實體檔案，因此可以 diff、可以重跑、可以只退回某一關（[[sources/week10-lecture]] §5.3(4)）。

## 一個最小 Graph

```text
[檢索] → <覆蓋率 ≥ 3?> ──否──▶ [停止]
              │是
              ▼
         [抽證據卡] → [寫大綱] → [寫逐頁稿] → [渲染] → [交件]
                            ▲            │
                            └──退回──────┘
```

這個 Graph 有四種邊：

- 固定邊：檢索 → 抽卡 → 大綱 → 逐頁稿 → 渲染 → 交件。
- 條件邊：覆蓋率檢查 → 停止或繼續。
- 退回邊：逐頁稿檢查失敗 → 退回該頁重寫。
- 終止邊：交件或停止。

## Graph 與 Pipeline 的差別

| 維度 | Pipeline | Graph |
|---|---|---|
| 流向 | 單向 | 有分支、有迴圈、有退回 |
| 錯誤處理 | 整條重跑 | 錯在哪一關，退回哪一關 |
| 並行 | 較難 | 可以扇出/扇入 |
| 適用 | 步驟固定的簡單任務 | 多階段、需要條件判斷與復原的任務 |

課程用「公文流程」比喻 Graph：系辦 → 院辦 → 教務處，每一關有明確職責，不能跳關，哪一關卡住就退回特定的一關（[[sources/week10-lecture]] §3.3）。

## 非確定性節點與 Guards

Graph 的節點不一定是確定的程式；很多節點是 LLM 呼叫，輸出有隨機性。課程提到現代 agent graph 的新點在於：非確定性節點、LLM routing 的邊，以及 guards 防護（[[sources/ai-agent-system-design-course]] §第四階段）。

因此，Graph 不能假設每個節點都會成功；每個 LLM 節點都應該有：

- 明確的輸入與輸出格式。
- 失敗時的重試或退回規則。
- 輸出驗證（例如 JSON schema、關鍵字、長度）。
- 必要時的人工審核。

## Checkpoint 與時間旅行

LangGraph 的 Checkpointer 在每個節點前後保存狀態快照，配合 `thread_id` 實現多會話隔離與斷點續傳；`get_state_history` 可以列出歷史快照，用過去的 `thread_ts` 重新執行，實現時間旅行（[[sources/langgraph-agents-course]] §Checkpointer 與 Thread、§時間旅行）。

時間旅行不是「改變過去」，而是「從某個快照開一個新分支」，原分支保留。這對除錯很有用：你可以回到「大綱剛寫完」的狀態，換一個教學順序，看看結果差多少。

## 常見誤解

| 誤解 | 為什麼錯 | 正確做法 |
|---|---|---|
| 「Graph 就是流程圖，畫好看就好」 | 沒有狀態與條件邊的圖，只是裝飾。 | 每個節點要有輸入、輸出、檢查與退回路線。 |
| 「節點越多越專業」 | 節點太多會增加協調成本與失敗點。 | 用單一職責與最小可運作節點數。 |
| 「Graph 一定要用框架」 | 小專案用資料夾與腳本就能實作 Graph。 | 先用檔案與腳本，需要持久化再上框架。 |
| 「有 Checkpoint 就不會出錯」 | Checkpoint 只保存狀態，不保證狀態正確。 | 每個節點仍要有驗證。 |

## 教學用法

先讓學生用紙筆畫出「從主題到簡報」的流程，標出每個節點的輸入與輸出；再把「如果第 6 頁講錯，要退回哪裡」畫成一條退回邊。學生通常會發現：如果沒有把逐頁稿獨立成節點，就只能整份重跑。

## 檢查清單

- [ ] 每個節點是否只有一個職責？
- [ ] 每個節點的輸入與輸出是否都是明確的檔案或狀態欄位？
- [ ] 是否有條件邊與退回邊？
- [ ] 是否有狀態保存與恢復機制？
- [ ] 每個 LLM 節點是否有輸出驗證與失敗處理？

## 出處

- [[sources/week10-lecture]] §3.3、§5.3
- [[sources/langgraph-agents-course]] §Agentic Workflow 基礎、§Checkpointer 與 Thread、§時間旅行
- [[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph
- [[sources/ai-agent-system-design-course]] §第四階段
