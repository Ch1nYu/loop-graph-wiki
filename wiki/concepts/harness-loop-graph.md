---
id: harness-loop-graph
title: "Harness、Loop、Graph：三層工程的分工"
type: concept
audience: beginner
updated: 2026-11-13
sources: [week10-lecture, agentic-workflow-humaneval, building-effective-ai-agents, agentic-harness-kimi-k3, ai-agent-system-design-course]
related: [loop-five-elements, graph-nodes-edges, prompt-loop-graph]
---

# Harness、Loop、Graph：三層工程的分工

> 一句話：Harness 決定「AI 能用什麼」，Loop 決定「AI 怎麼反覆修正」，Graph 決定「誰在什麼時候把控制權交給誰」。

## 為什麼需要分層

很多人把「AI 做不好」歸咎於模型不夠強，但實際問題常常出在三個不同的層次：模型沒有拿到正確的上下文與工具（Harness）、沒有明確的完成標準與停止條件（Loop）、或是流程的責任與退回路線沒有設計（Graph）。把這三層混在一起，就會出現「在還沒理解行為前就畫流程圖」、「讓同一個模型自己評分」、「無上限重試」等昂貴失誤（[[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph）。

課程把生成式 AI 的工程演進整理成五層：Prompt Engineering、Context Engineering、Harness Engineering、Loop Engineering、Graph Engineering（[[sources/week10-lecture]] §1.3）。本頁聚焦後三層，因為它們是「把工作拆成 AI 能做的流程」的核心。

## 三層各自的問題

| 層次 | 它回答的問題 | 主要產出 | 缺少它會怎樣 |
|---|---|---|---|
| **Harness** | AI 能看到什麼、能用什麼工具、有什麼權限、狀態存在哪裡？ | 專案規則、任務 Skill、工具、沙箱、權限、記憶、觀測 | 模型拿到錯的上下文、亂用工具、越權修改檔案 |
| **Loop** | 這一輪要做什麼、怎麼知道做完了、什麼時候停？ | 目標、限制、驗證、停止條件、觸發 | 人類變成人工迴圈；AI 無限重試或提早收工 |
| **Graph** | 有哪些節點、誰把控制權交給誰、錯了退回哪裡？ | 節點、邊、條件邊、狀態、退回路線 | 每次修正都整份重跑；錯誤在最後才被發現 |

這三層不是替代關係，而是疊加關係。Harness 是地板，Loop 是引擎，Graph 是路網（[[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph）。

## Harness：把「工作」而不是「模型」放在中心

Harness 的原文定義是「周邊機制：上下文、工具、權限、持續性、控制、安全與可觀測性」（[[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph）。另一個說法是：Harness 是針對「工作」裁剪的控制層，不是針對某個模型；模型是商品，Harness 才是資產（[[sources/agentic-harness-kimi-k3]] §五大核心概念）。

在實作上，Harness 包含：

- **規則**：專案手冊定義目標、邊界、寫作規範與完成定義。
- **技能**：任務 Skill 定義特定任務的標準步驟與檢查。
- **工具與權限**：哪些檔案可讀、可寫、可執行；哪些動作需要人工核准。
- **狀態**：檔案、資料庫、ledger 或 checkpoint，讓下一輪能接續。
- **觀測**：log、diff、測試結果、截圖，讓人類能驗收。

課程用「AI Agent = AI Model（大腦）+ Harness（工作裝備）」來描述這個關係（[[sources/week10-lecture]] §1.3）。同一個模型，換一套 Harness，產出品質可能差很多；這就是為什麼與其一直換模型，不如先把 Harness 建好。

## Loop：把「修正」寫成規格

Loop 不是「一直重試」，而是「觀察—行動—驗證」的循環，並且有明確的觸發與以證據為基礎的停止規則（[[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph）。一個完整的 Loop 要寫清楚五件事：目標、限制、完成標準與驗證、停止條件、觸發條件（[[sources/week10-lecture]] §3.2）。

Loop 與 Prompt 的差別，不是「有沒有用文字」，而是「誰決定下一步」：寫 Prompt 是寫這一輪要做什麼，人類讀完輸出再寫下一句；寫 Loop 是寫一份會自己執行的規格，系統依檢查結果決定下一步（[[sources/week10-lecture]] §3.1）。

## Graph：把「控制權」畫出來

Graph 用節點與邊描述工作流拓撲，控制允許的下一步、分支、併發、狀態轉移與復原路徑（[[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph）。在 LangGraph 的實作裡，節點是處理單元、邊是固定流向、條件邊是決策分流、State 是全域狀態（[[sources/langgraph-agents-course]] §Agentic Workflow 基礎）。

Graph 的價值不是「看起來比較專業」，而是**精準退回**：錯在哪一關，就退回哪一關，不用整份重跑（[[sources/week10-lecture]] §5.3）。這也是 Graph 與單純 pipeline 的差別：pipeline 只有往前，Graph 有條件分支與退回邊。

## 三層如何協作

以「從 Wiki 生成教學簡報」為例：

1. **Harness**：專案規則限定可使用的知識庫、唯讀來源與每頁出處要求；任務 Skill 規定節點與檢查。
2. **Loop**：逐頁稿節點內部跑「寫一頁 → 對來源 → 修改」的小迴圈，最多 2 輪；渲染節點跑「產生 HTML → 截圖 → 修版面」的小迴圈，最多 3 輪。
3. **Graph**：檢索 → 證據卡 → 大綱 → 逐頁稿 → 渲染 → 交件；每個關卡有條件邊與退回路線。

這樣的組合，就是課程說的「Graph 決定大流程，Loop 負責每一格內部的反覆修正」（[[sources/week10-lecture]] §5.3(3)）。

## 常見誤解

| 誤解 | 為什麼錯 | 正確做法 |
|---|---|---|
| 「Harness 就是系統提示詞」 | 系統提示詞只是 Harness 的一部分；Harness 還包含工具、權限、狀態與觀測。 | 把 Harness 當成整個工作環境來設計。 |
| 「Loop 就是一直重試」 | 沒有停止條件與證據的重試，是無限迴圈。 | 先寫完成標準與剎車，再寫重試。 |
| 「Graph 一定比 Loop 好」 | Graph 的成本與維護複雜度更高；簡單任務用 Graph 是過度設計。 | 先用 Prompt，重複出現再升級 Loop，多階段才拆 Graph。 |
| 「三層可以分開看」 | 三層會互相影響：Harness 的權限決定 Loop 能做什麼，Loop 的檢查決定 Graph 的退回邊。 | 設計時一起考慮，但實作時分層負責。 |

## 教學用法

教初學者時，先用「Prompt 是一句話、Loop 是一份規格、Graph 是一張流程圖」建立直覺，再用「誰決定下一步」與「錯了退回哪裡」兩個問題區分 Loop 與 Graph。最後用一個真實的小專案（例如這份簡報）示範三層如何疊起來。

## 檢查清單

- [ ] 這個任務的 Harness 有什麼？規則、工具、權限、狀態、觀測是否齊全？
- [ ] 這個 Loop 的目標、限制、驗證、停止條件、觸發是否寫清楚？
- [ ] 這個 Graph 的節點、邊、條件邊、退回路線是否畫出來？
- [ ] 三層是否有互相矛盾的地方？（例如 Harness 禁止改檔，但 Loop 要求自動修檔。）

## 出處

- [[sources/week10-lecture]] §1.3、§3.1、§3.2、§5.3
- [[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph
- [[sources/building-effective-ai-agents]] §What are agents?
- [[sources/agentic-harness-kimi-k3]] §五大核心概念
- [[sources/ai-agent-system-design-course]] §第四階段
