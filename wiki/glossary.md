---
id: glossary
title: "術語表"
type: glossary
audience: beginner
updated: 2026-11-13
sources: [week10-lecture, agentic-workflow-humaneval, building-effective-ai-agents, langgraph-agents-course, agentic-harness-kimi-k3]
related: [index]
---

# 術語表

> 這頁只定義本 Wiki 會用到的術語；每個定義都連回主要頁面與來源。

| 術語 | 白話定義 | 主要頁面 |
|---|---|---|
| **Agent** | 由 LLM 在執行時動態決定流程與工具使用的系統；與 workflow 的差別是「誰決定下一步」。 | [[concepts/harness-loop-graph]] |
| **Harness** | Agent 的周邊控制層：上下文、工具、權限、狀態、安全與觀測。 | [[concepts/harness-loop-graph]] |
| **Loop** | 觀察—行動—驗證的反覆循環，有明確觸發與以證據為基礎的停止規則。 | [[concepts/loop-five-elements]] |
| **Graph** | 用節點與邊描述的工作流拓撲，包含條件邊與退回邊。 | [[concepts/graph-nodes-edges]] |
| **Node（節點）** | Graph 中的一個處理單元，可以是 LLM 呼叫、工具、函式或人工關卡。 | [[concepts/graph-nodes-edges]] |
| **Edge（邊）** | 節點之間的固定流向。 | [[concepts/graph-nodes-edges]] |
| **Conditional Edge（條件邊）** | 依條件決定下一步去哪的邊。 | [[concepts/graph-nodes-edges]] |
| **Fallback Edge（退回邊）** | 檢查不通過時，退回前面某個節點的邊。 | [[concepts/fallback-edges]] |
| **State（狀態）** | 流程的記憶體：做到哪一關、通過哪些檢查、有哪些檔案。 | [[concepts/state-as-files]] |
| **Checkpoint** | 每個節點前後保存的狀態快照，用於恢復與時間旅行。 | [[concepts/state-as-files]] |
| **Human-in-the-loop** | 在關鍵決策點讓人類介入，而不是全程盯場。 | [[concepts/human-in-the-loop]] |
| **ACI** | Agent-Computer Interface：工具與介面的設計，應投入與 HCI 同等的精力。 | [[concepts/information-scoping]] |
| **Evaluator-Optimizer** | 一個 LLM 生成、另一個 LLM 依標準評估並回饋的迴圈模式。 | [[concepts/verification]] |
| **Prompt Chaining** | 把任務拆成固定子任務序列，每輪 LLM 處理上一輪輸出。 | [[sources/building-effective-ai-agents]] |
| **Routing** | 先分類輸入，再導向專門的下游流程。 | [[sources/building-effective-ai-agents]] |
| **Orchestrator-Workers** | 中央 LLM 動態拆解任務、分派給多個 worker，再彙整結果。 | [[sources/building-effective-ai-agents]] |
| **Guardrail** | 限制 agent 行為的防護機制，例如最大迭代次數、權限、沙箱。 | [[concepts/stop-conditions]] |
| **Stop Condition** | 什麼時候停止迴圈的規則，例如硬上限、資料不足、成本上限。 | [[concepts/stop-conditions]] |
| **Evidence Card（證據卡）** | 從單一來源抽出的可引用證據，包含原文、位置與 URL。 | [[methods/teaching-deck-pipeline]] |
| **Coverage（覆蓋率）** | 簡報是否涵蓋了 Wiki 中與主題相關的重要來源。 | [[concepts/verification]] |
| **Faithfulness（忠實度）** | 簡報內容是否忠於來源，沒有講反、腦補或斷章取義。 | [[concepts/verification]] |
| **LLM Wiki** | 給 AI 檢索的結構化 Markdown 知識庫，用 index 與連結取代向量資料庫。 | [[methods/llm-wiki]] |
| **RAG** | Retrieval-Augmented Generation：先檢索外部資料，再生成回答。 | [[methods/llm-wiki]] |
| **Context Engineering** | 設計要給 AI 什麼上下文、什麼順序、什麼格式。 | [[concepts/harness-loop-graph]] |
| **State as Files** | 把每個節點的狀態與產出存成實體檔案，讓流程可 diff、可重跑。 | [[concepts/state-as-files]] |
| **Fail Closed** | 檢查失敗或腳本壞掉時，預設拒絕，而不是默默跳過。 | [[concepts/stop-conditions]] |
| **Gate** | 在副作用發生處攔截的關卡，例如部署前的人工核准。 | [[concepts/information-scoping]] |
| **Ledger** | 有序、僅追加的事件紀錄，讓執行可重播、可審計。 | [[concepts/state-as-files]] |

## 出處

- [[sources/week10-lecture]] §1.3、§3.2、§3.3、§5.3
- [[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph
- [[sources/building-effective-ai-agents]] §Workflow patterns
- [[sources/langgraph-agents-course]] §Agentic Workflow 基礎
- [[sources/agentic-harness-kimi-k3]] §七大原語
