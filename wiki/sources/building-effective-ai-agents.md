---
id: building-effective-ai-agents
title: "Building Effective AI Agents（Anthropic）"
type: source
source_kind: engineering-article
original_url: "https://www.anthropic.com/engineering/building-effective-agents"
ingested: 2026-11-13
updated: 2026-11-13
reliability: high
coverage: [workflow, agent, evaluator-optimizer, aci, guardrails]
---

# Building Effective AI Agents（Anthropic）

## 這篇在說什麼

Anthropic 整理過去一年與數十個團隊合作建構 LLM agent 的經驗，把「agentic systems」分成兩類：**Workflows** 是由預先寫好的程式碼路徑編排 LLM 與工具；**Agents** 是由 LLM 在執行時動態決定流程與工具使用。文章的核心建議是：先找最簡單的方案，只有在單輪 LLM 真的不夠時，才增加多步驟的複雜度。

文章也整理了五種常見 workflow 模式：prompt chaining、routing、parallelization、orchestrator-workers、evaluator-optimizer。其中 evaluator-optimizer 對本 Wiki 特別重要：它讓一個 LLM 生成初稿，另一個 LLM 依明確標準給回饋，若不合格就帶著回饋重寫。這正是「生成者與審查者分離」的工程版本。

## 關鍵主張（可引用）

| # | 主張 | 原文位置 | 本 Wiki 用到的地方 |
|---|---|---|---|
| 1 | Workflows 由預先寫好的程式碼路徑編排；Agents 由 LLM 動態決定流程與工具使用。 | 「What are agents?」 | [[concepts/harness-loop-graph]]、[[comparisons/prompt-loop-graph]] |
| 2 | 應先找最簡單的方案，只在必要時增加複雜度；有時甚至不該建 agentic system。 | 「When (and when not) to use agents」 | [[comparisons/prompt-loop-graph]] |
| 3 | Evaluator-optimizer 模式：一個 LLM 生成，另一個 LLM 依標準評估並回饋，形成迭代迴圈。 | 「Workflow: Evaluator-optimizer」 | [[concepts/verification]] |
| 4 | 工具設計就是 ACI（agent-computer interface），應投入與 HCI 同等的精力；例如強制絕對路徑可大幅降低工具呼叫錯誤。 | Appendix 2 | [[concepts/information-scoping]] |
| 5 | Agent 的自主性帶來更高成本與錯誤複合風險；應在沙箱測試、設置 guardrails、包含最大迭代次數等停止條件。 | 「Agents」 | [[concepts/stop-conditions]] |
| 6 | 框架能加速起步，但抽象層會遮蔽 prompt/response、增加除錯難度；進生產環境時應考慮減少抽象層。 | 「When and how to use frameworks」 | [[concepts/harness-loop-graph]] |
| 7 | 好的 agent 設計三原則：保持簡單、優先透明、精心打造 ACI。 | 「Summary」 | [[concepts/information-scoping]] |

## 本 Wiki 用到的地方

- [[concepts/harness-loop-graph]]：Workflow 與 Agent 的區分。
- [[concepts/verification]]：evaluator-optimizer 與生成者/審查者分離。
- [[concepts/information-scoping]]：ACI 與工具介面設計。
- [[concepts/stop-conditions]]：最大迭代次數與 guardrails。
- [[comparisons/prompt-loop-graph]]：先簡單、後複雜的選擇原則。

## 限制與注意

- 文章發布於 2024 年 12 月，部分產品與框架名稱（Claude Agent SDK、Strands 等）在 2026 年已有變化；本 Wiki 只引用架構原則。
- HumanEval 等 benchmark 數字不在本文；本 Wiki 不把本文與其他來源的數字混用。
- 文章是工程實務建議，不是對所有團隊都成立的實驗定律。

## 原始出處

- 原文：<https://www.anthropic.com/engineering/building-effective-agents>
