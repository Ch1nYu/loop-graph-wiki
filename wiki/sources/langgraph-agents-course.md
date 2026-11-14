---
id: langgraph-agents-course
title: "Andrew Ng 與 LangChain 的 LangGraph Agent 課程"
type: source
source_kind: course-summary
original_url: "https://x.com/AnatoliKopadze/status/2088684163167670725"
ingested: 2026-11-13
updated: 2026-11-13
reliability: high
coverage: [graph, nodes, edges, state, checkpoint, human-in-the-loop]
---

# Andrew Ng 與 LangChain 的 LangGraph Agent 課程

## 這篇在說什麼

這是 DeepLearning.AI 與 LangChain 合作課程的筆記，由 Andrew Ng 主持，Harrison Chase 與 Anatoli Kopadze 等講師講解。課程用 LangGraph 從零建構具備工具調用、持久化、人機介入與時間旅行能力的 agent 系統。

LangGraph 的核心抽象是 **Nodes**（處理單元）、**Edges**（固定流向）、**Conditional Edges**（決策分流）與 **State**（全域狀態）。State 用 `TypedDict` 定義，搭配 `Annotated[..., operator.add]` 實現累加語義；Checkpointer 在每個節點前後保存快照，配合 `thread_id` 實現多會話隔離、斷點續傳與時間旅行。

## 關鍵主張（可引用）

| # | 主張 | 原文位置 | 本 Wiki 用到的地方 |
|---|---|---|---|
| 1 | LangGraph 以有向循環圖建模 agent 行為，核心概念是 Nodes、Edges、Conditional Edges 與 State。 | 「Agentic Workflow 基礎」段 | [[concepts/graph-nodes-edges]] |
| 2 | State 是全域可見的資料結構；`operator.add` 讓訊息累加，未標註欄位則覆寫。 | 同上 | [[concepts/graph-nodes-edges]] |
| 3 | Checkpointer 在每個節點前後保存狀態快照，配合 `thread_id` 實現跨請求記憶、中斷續跑與多會話隔離。 | 「Checkpointer 與 Thread」段 | [[concepts/state-as-files]] |
| 4 | `interrupt_before` / `interrupt_after` 讓圖在特定節點暫停，前端可取得狀態、修改參數，再恢復執行。 | 「Human-in-the-loop」段 | [[concepts/human-in-the-loop]] |
| 5 | `get_state_history` 可列出歷史快照，用過去的 `thread_ts` 重新執行，實現時間旅行與分支實驗。 | 「時間旅行」段 | [[concepts/state-as-files]] |
| 6 | Essay Writer 用 Plan-and-Execute + Reflection：planner → research → generate → reflect → research_critique → generate，並以 `max_revisions` 控制停止。 | 「Plan-and-Execute + Reflection」段 | [[concepts/loop-five-elements]]、[[concepts/stop-conditions]] |
| 7 | Multi-agent 共享單一 State；Supervisor 讓子代理擁有獨立 State；Flow Engineering 是線性管線夾雜關鍵迴圈。 | 「進階架構」段 | [[concepts/harness-loop-graph]] |

## 本 Wiki 用到的地方

- [[concepts/graph-nodes-edges]]：Nodes / Edges / Conditional Edges / State。
- [[concepts/state-as-files]]：Checkpointer、快照、時間旅行。
- [[concepts/human-in-the-loop]]：interrupt 與人工審核。
- [[concepts/loop-five-elements]]：Plan-and-Execute + Reflection 的迴圈。
- [[concepts/stop-conditions]]：`max_revisions` 與重試上限。

## 限制與注意

- 這是課程筆記，程式碼細節以 LangGraph 官方文件為準；本 Wiki 只引用架構概念。
- 課程示範的是 Python 與 LangGraph 生態，其他框架（AutoGen、CrewAI）的實作不同。
- 「時間旅行」是狀態快照與重放的能力，不是真的改變過去；會產生新分支，原分支保留。

## 原始出處

- 課程來源貼文：<https://x.com/AnatoliKopadze/status/2088684163167670725>
- LangGraph 官方文件：<https://langchain-ai.github.io/langgraph/>
