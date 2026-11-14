---
id: index
title: "Loop / Graph Engineering Wiki"
type: index
updated: 2026-11-13
---

# Loop / Graph Engineering Wiki

> 給 AI 與人共讀的知識庫：把「一句話 Prompt」升級成「可驗證的工作流」。

## 這個 Wiki 是什麼

這個 Wiki 的主題是 **Loop / Graph Engineering**：如何把一個模糊的工作（例如「做一份教學簡報」）拆成 AI 能執行、能檢查、能退回的流程。它結合三個來源脈絡：

1. **Week 10 課程**：Harness、Loop、Graph 三層工程，以及 LLM Wiki 與簡報工作流。
2. **Week 9 的 AI 閱讀筆記**：Anthropic 的 agent 設計、LangGraph 的圖與狀態、Harness 工程、自我改進迴圈。
3. **本專案的實際執行**：從 7 篇來源生成 13 頁教學簡報的完整紀錄。

**主要讀者**：大學部高年級或研究所初學者，用過 ChatGPT 但沒有寫過 agent workflow；以及下游的簡報生成 AI。

## 怎麼讀

### 路徑 A：完全新手（約 20 分鐘）

1. [[concepts/harness-loop-graph]]：先搞懂三層工程。
2. [[concepts/loop-five-elements]]：Loop 的五個要素。
3. [[comparisons/prompt-loop-graph]]：什麼時候用哪一種。
4. [[concepts/verification]]：為什麼要雙軌驗證。

### 路徑 B：要動手做（約 40 分鐘）

1. [[methods/llm-wiki]]：先建知識庫。
2. [[concepts/graph-nodes-edges]]：Graph 的基本元素。
3. [[concepts/fallback-edges]]：退回邊與檢查前移。
4. [[concepts/information-scoping]]：權限隔離。
5. [[concepts/state-as-files]]：狀態即檔案。
6. [[methods/teaching-deck-pipeline]]：本專案的完整 Graph。

### 路徑 C：要設計自己的流程（約 60 分鐘）

1. [[concepts/human-in-the-loop]]：人類該在哪裡介入。
2. [[concepts/stop-conditions]]：剎車怎麼設。
3. [[concepts/verification]]：檢查怎麼寫。
4. [[methods/teaching-deck-pipeline]]：照著抄一遍，再改成自己的主題。

## 頁面總表

### 概念頁（Concepts）

| ID | 標題 | 一句話 |
|---|---|---|
| [[concepts/harness-loop-graph]] | Harness、Loop、Graph：三層工程的分工 | Harness 決定能用什麼，Loop 決定怎麼修正，Graph 決定誰控制誰。 |
| [[concepts/loop-five-elements]] | Loop 的五個要素 | 目標、限制、驗證、剎車、觸發，缺一不可。 |
| [[concepts/verification]] | 雙軌驗證 | 程式檢查「有沒有做到」，獨立 AI 審查「有沒有做對」。 |
| [[concepts/graph-nodes-edges]] | Graph 的基本元素 | 節點、邊、條件邊、狀態，四個元素組成工作流。 |
| [[concepts/fallback-edges]] | 退回邊與檢查前移 | 大圈少轉，小圈快轉；錯在哪裡就退回哪裡。 |
| [[concepts/information-scoping]] | 資訊與權限隔離 | 每個節點只能看它該看的，不能做超出職責的事。 |
| [[concepts/state-as-files]] | State as Files | 沒有變成檔案的產出，等於沒有發生。 |
| [[concepts/human-in-the-loop]] | Human-in-the-loop | 人類不該當迴圈，而該當關卡。 |
| [[concepts/stop-conditions]] | 停止條件 | 沒有剎車的 Loop 只是燒錢。 |

### 比較頁（Comparisons）

| ID | 標題 | 一句話 |
|---|---|---|
| [[comparisons/prompt-loop-graph]] | Prompt、Loop、Graph 怎麼選？ | 不要問哪個高級，要問這個任務需要多少結構。 |

### 方法頁（Methods）

| ID | 標題 | 一句話 |
|---|---|---|
| [[methods/llm-wiki]] | LLM Wiki 的建置方法 | 給 AI 讀的知識庫，結構比文筆重要。 |
| [[methods/teaching-deck-pipeline]] | 本專案的 Graph | 7 個節點、5 個關卡、3 輪檢查的簡報流程。 |

### 來源頁（Sources）

| ID | 標題 | 類型 | 可信度 |
|---|---|---|---|
| [[sources/week10-lecture]] | Week 10 課程筆記 | lecture-notes | high |
| [[sources/agentic-workflow-humaneval]] | Agentic workflow 讓 GPT-3.5 在 HumanEval 達到 95.1% | article-summary | medium |
| [[sources/building-effective-ai-agents]] | Building Effective AI Agents | engineering-article | high |
| [[sources/langgraph-agents-course]] | Andrew Ng 與 LangChain 的 LangGraph Agent 課程 | course-summary | high |
| [[sources/agentic-harness-kimi-k3]] | How to Build An Agentic Harness using Kimi K3 | engineering-essay | medium |
| [[sources/self-improving-coding-loop]] | 用 DeepSeek V4 Flash 在 Codex 建立自我改進編碼循環 | article-summary | medium |
| [[sources/ai-agent-system-design-course]] | 前 Google 工程師的 AI Agent 系統設計課 | course-summary | medium |

### 其他

| ID | 標題 | 用途 |
|---|---|---|
| [[glossary]] | 術語表 | 統一 Loop / Graph / Harness 相關術語 |
| [[log]] | Ingest 與變更日誌 | 記錄何時 ingest、改了哪些頁 |

## 來源登記

| ID | 原始 URL | 來源類型 | 備註 |
|---|---|---|---|
| week10-lecture | <https://www.youtube.com/live/pEmuTl9vTf8> | 課程直播與講義 | 本 Wiki 的主要概念來源 |
| agentic-workflow-humaneval | <https://x.com/N01ennn/status/2097264706088014123> | 文章整理 | 三層工程與零信任 |
| building-effective-ai-agents | <https://www.anthropic.com/engineering/building-effective-agents> | 工程文章 | Anthropic 官方文章 |
| langgraph-agents-course | <https://x.com/AnatoliKopadze/status/2088684163167670725> | 課程整理 | LangGraph 課程 |
| agentic-harness-kimi-k3 | <https://x.com/Av1dlive/status/2085405823782842835> | 工程長文 | Harness 工程實作 |
| self-improving-coding-loop | <https://x.com/cyrilXBT/status/2088542962854629672> | 文章整理 | 自我改進迴圈 |
| ai-agent-system-design-course | <https://x.com/LunarResearcher/status/2084984207495827776> | 課程整理 | Agent 系統設計課 |

## 主題覆蓋地圖

| 主題 | 主要頁面 |
|---|---|
| 三層工程 | [[concepts/harness-loop-graph]] |
| Loop 設計 | [[concepts/loop-five-elements]]、[[concepts/stop-conditions]] |
| Graph 設計 | [[concepts/graph-nodes-edges]]、[[concepts/fallback-edges]] |
| 驗證 | [[concepts/verification]] |
| 權限 | [[concepts/information-scoping]] |
| 狀態 | [[concepts/state-as-files]] |
| 人類介入 | [[concepts/human-in-the-loop]] |
| 選擇結構 | [[comparisons/prompt-loop-graph]] |
| 建 Wiki | [[methods/llm-wiki]] |
| 本專案流程 | [[methods/teaching-deck-pipeline]] |

## 維護規則

1. 新增來源時，先寫 `wiki/sources/<id>.md`，再更新概念頁與 `log.md`。
2. 每個事實句都要有 `[[sources/<id>]]`。
3. 數字、百分比、年份必須能在來源頁找到。
4. 新增頁面後，更新本頁的頁面總表。
5. 每次修改後執行 `python scripts/check_wiki.py`。
6. 如果來源衝突，並陳雙方說法，不選邊。

## 快速回答

**Q：Loop 和 Graph 的差別是什麼？**
A：Loop 是「一個節點加一條回到自己的邊」，Graph 是「多個節點加條件邊與退回邊」。Loop 由 AI 在規格內決定下一步，Graph 由人類事先畫好流程（[[comparisons/prompt-loop-graph]]）。

**Q：為什麼不能只寫 Prompt？**
A：一次性任務可以；但如果你一直重複說同樣的修正指令，就代表你需要 Loop；如果不同階段有不同驗收標準，就代表你需要 Graph（[[comparisons/prompt-loop-graph]]）。

**Q：為什麼不能讓 AI 自己檢查？**
A：生成者會有自我護航的偏見；獨立審查必須用新上下文，只給成品與來源（[[concepts/verification]]）。

**Q：什麼是 State as Files？**
A：把每個節點的狀態與產出存成檔案，讓流程可以 diff、重跑、只退回某一關（[[concepts/state-as-files]]）。
