---
id: ai-agent-system-design-course
title: "前 Google 工程師的 AI Agent 系統設計課"
type: source
source_kind: course-summary
original_url: "https://x.com/LunarResearcher/status/2084984207495827776"
ingested: 2026-11-13
updated: 2026-11-20
reliability: medium
coverage: [harness, loop, graph, memory, evolution]
---

# 前 Google 工程師的 AI Agent 系統設計課

## 這篇在說什麼

這是一堂約 3 小時的 AI agent 系統設計課的筆記，從 RAG 基礎、多 agent 架構、記憶體系，一路講到 Loop/Graph 工程化、LLM Ops 評估閉環與開源專案部署。課程把 agent 的演進整理成一個階梯：Prompt Engineering → Context Engineering → Skills/Procedural Memory → Loop → Graph。

對本 Wiki 最重要的是兩點：第一，Loop 與 Graph 互補：Loop 適合探索性任務（例如 Deep Research），Graph 適合 SOP 固定的企業流程。第二，Graph 的節點可以是確定性的程式，也可以是非確定性的 LLM 呼叫；因此需要 LLM routing 的邊與 guards 的防護。

## 關鍵主張（可引用）

| # | 主張 | 原文位置 | 本 Wiki 用到的地方 |
|---|---|---|---|
| 1 | Agent 工程演進階梯：Prompt → Context → Skills/Procedural Memory → Loop → Graph。 | 「第四階段：工程演進階梯」段 | [[concepts/harness-loop-graph]]、[[comparisons/prompt-loop-graph]] |
| 2 | Loop 適合探索性任務（Deep Research）；Graph 適合 SOP 固定的企業級流程。 | 同上 | [[comparisons/prompt-loop-graph]] |
| 3 | Graph 的節點包含非確定性 LLM 呼叫、LLM routing 的邊，並需要 guards 防護。 | 同上 | [[concepts/graph-nodes-edges]]、[[concepts/verification]] |
| 4 | Harness 注入四類記憶：程序記憶（技能）、語義/耐久事實、事件記憶、工作記憶。 | 「Agent Harness、記憶體系」段 | [[concepts/harness-loop-graph]] |
| 5 | Hermes harness 用 `soul.md`、`Skills/*.md`、`memory.md`、`state.db` 管理記憶，並以錯誤/重複任務蒸餾更新技能。 | 同上 | [[concepts/state-as-files]] |
| 6 | 缺乏內建 eval 是這類 harness 的弱點，需自行整合 LangSmith/Langfuse 等觀測工具。 | 同上 | [[concepts/verification]] |

## 本 Wiki 用到的地方

- [[concepts/harness-loop-graph]]：演進階梯與 Harness 的記憶。
- [[comparisons/prompt-loop-graph]]：Loop 與 Graph 的互補。
- [[concepts/graph-nodes-edges]]：非確定性節點、routing 邊、guards。
- [[concepts/state-as-files]]：`soul.md`、`Skills/`、`memory.md`、`state.db`。
- [[concepts/verification]]：eval 與觀測工具。

## 限制與注意

- 這是課程筆記的二手整理，課程中的產品與 GitHub 星數可能隨時間變動；本 Wiki 不引用會過期的數字。
- 「Loop 適合探索、Graph 適合 SOP」是教學上的簡化；實務上常見 Graph 內含 Loop 的混合結構。
- 本 Wiki 沒有實際安裝 Hermes 或 waku-agent，只引用其記憶與 graph 設計概念。

## 原始出處

- 課程來源貼文：<https://x.com/LunarResearcher/status/2084984207495827776>
