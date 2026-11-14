---
id: state-as-files
title: "State as Files：資料夾就是流程的記憶體"
type: concept
audience: intermediate
updated: 2026-11-13
sources: [week10-lecture, langgraph-agents-course, agentic-harness-kimi-k3, ai-agent-system-design-course]
related: [graph-nodes-edges, information-scoping, verification]
---

# State as Files：資料夾就是流程的記憶體

> 一句話：如果一個節點的產出沒有變成檔案，它就等於沒有發生。

## 為什麼要把狀態存成檔案

檔案不只是備份，而是下一輪的輸入；沒有它，AI 只能從對話裡猜。

課程在 Graph 版工作流裡提出「State as Files」：每一個節點的狀態與產出都是一個實體檔案，因此可以打開來看、可以放進 git、可以單獨重跑（[[sources/week10-lecture]] §5.3(4)）。

這解決了三個問題：

1. **可追溯**：出錯時可以看到是哪一關的哪個檔案有問題。
2. **可重跑**：不用整份流程重來，只要重跑壞掉的那一關。
3. **可協作**：人類可以直接打開檔案，不需要理解整個系統。

## 本專案的狀態檔

```text
run/
├── sources.md             # N1：檢索結果與覆蓋率
├── cards/                 # N2：每篇來源一張證據卡
├── outline.md             # N3：大綱（含人類確認紀錄）
├── drafts/                # N4：逐頁稿
├── report.md              # N6：檢查與修正紀錄
└── review.md              # N6：獨立審查報告
```

最終產出是一份 HTML；中間狀態全部留在執行資料夾，不覆蓋、不刪除。這樣即使簡報改了 3 輪，我們還是可以回頭看第 1 輪的檢索結果與大綱，知道當時為什麼做那個決定。

## 狀態不是只有「檔案」，還有「事件」

Harness 的文章提出 **Ledger**：有序、僅追加的事件紀錄，先持久化再廣播；讓每一次執行可重播、可審計（[[sources/agentic-harness-kimi-k3]] §BUILD 02）。

檔案是「快照」，Ledger 是「事件流」。兩者互補：

- 快照告訴你「現在長什麼樣」。
- 事件流告訴你「怎麼變成這樣」。

對本專案而言，檢查報告就是簡化版的事件流：記錄每一輪發現什麼、改了什麼、為什麼改；機器可讀的檢查結果則是當下的快照。

## Checkpoint：可恢復的狀態

LangGraph 的 Checkpointer 在每個節點前後保存狀態快照，配合 `thread_id` 實現跨請求記憶、中斷續跑與多會話隔離；生產環境可外接 PostgreSQL/Redis（[[sources/langgraph-agents-course]] §Checkpointer 與 Thread）。

Checkpoint 的價值是「恢復」：如果流程跑到一半中斷，可以從最後一個 checkpoint 繼續，不用從頭來。對長時間的簡報生成流程，這可以節省大量重複工作。

## 時間旅行：從舊快照開新分支

`get_state_history` 可以列出歷史快照，用過去的 `thread_ts` 重新執行，實現時間旅行；這會產生新分支，原分支保留（[[sources/langgraph-agents-course]] §時間旅行）。

對寫作的啟示：如果你不確定「先講 Loop 再講 Graph」還是「先講 Graph 再講 Loop」比較好，可以從「大綱完成」的快照開兩個分支，各寫一版，再比較。這比在腦中想像更可靠。

## 記憶的四個類型

課程提到 Harness 注入四類記憶：程序記憶（技能/如何行動）、語義/耐久事實（私有知識）、事件記憶（跨對話時間序列）、工作記憶（當下上下文）（[[sources/ai-agent-system-design-course]] §Agent Harness、記憶體系）。

對應到本專案：

- **程序記憶**：任務 Skill 與 workflow 定義。
- **語義記憶**：Wiki 的 concept 與 source 頁。
- **事件記憶**：檢查報告與 Wiki 變更日誌。
- **工作記憶**：簡報規格與執行中的逐頁稿。

這個分類可以幫助你判斷「這個資訊應該放在哪裡」：技能放規則檔、事實放知識庫、過程放日誌、當前任務放執行資料夾。

## 反模式

| 反模式 | 問題 | 替代做法 |
|---|---|---|
| 狀態只存在對話裡 | 對話一關就消失，無法重跑 | 每個節點寫檔 |
| 每次都覆蓋同一個檔案 | 無法比較前後版本 | 用 `run/<date>-<topic>/` 保留每次執行 |
| 只存最終成品 | 出錯時不知道哪一關壞 | 保留中間產出與檢查報告 |
| 沒有事件紀錄 | 知道結果，不知道原因 | 寫 `report.md` 或 ledger |

## 教學用法

讓學生比較「把東西貼在對話框」與「把東西存成檔案」的差別。可以問：「如果你明天要接續這份簡報，你要從哪裡開始？」如果答案是「往上滑對話」，就代表狀態沒有變成檔案。

## 檢查清單

- [ ] 每個節點是否有明確的輸出檔案？
- [ ] 中間產出是否保留，而不是被覆蓋？
- [ ] 是否有事件紀錄（誰在什麼時候改了什麼）？
- [ ] 是否可以用單一指令重跑某一關？
- [ ] 是否區分程序記憶、語義記憶、事件記憶、工作記憶？

## 出處

- [[sources/week10-lecture]] §5.3(4)
- [[sources/langgraph-agents-course]] §Checkpointer 與 Thread、§時間旅行
- [[sources/agentic-harness-kimi-k3]] §BUILD 02
- [[sources/ai-agent-system-design-course]] §Agent Harness、記憶體系
