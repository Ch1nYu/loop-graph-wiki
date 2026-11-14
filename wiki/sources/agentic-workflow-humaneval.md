---
id: agentic-workflow-humaneval
title: "Agentic workflow 讓 GPT-3.5 在 HumanEval 達到 95.1%"
type: source
source_kind: article-summary
original_url: "https://x.com/N01ennn/status/2097264706088014123"
ingested: 2026-11-13
updated: 2026-11-13
reliability: medium
coverage: [harness, loop, graph, verification, stop-conditions]
---

# Agentic workflow 讓 GPT-3.5 在 HumanEval 達到 95.1%

## 這篇在說什麼

這篇筆記整理 NO1ennn 的兩則 X 貼文：第一則用 HumanEval 的數字說明，加入反思、工具使用、規劃與多智能體協作後，GPT-3.5 的表現可以從 48.1% 提升到 95.1%，高於 GPT-4 單次回答的 67.0%。第二則把 agent 系統拆成 Harness、Loop、Graph 三層，並提出零信任的五條規則。

這篇的價值在於把「三層工程」講得很清楚：Harness 是周邊機制，Loop 是觀察—行動—驗證循環，Graph 是節點與邊的拓撲。它同時提醒，混淆這三層會產生昂貴的失敗，例如讓同一個模型自己評分、製造無上限重試、在 harness 塞入過多工具。

## 關鍵主張（可引用）

| # | 主張 | 原文位置 | 本 Wiki 用到的地方 |
|---|---|---|---|
| 1 | Harness engineering 是周邊機制：上下文、工具、權限、持續性、控制、安全與可觀測性。 | 「Harness、Loop 與 Graph 三層工程」段 | [[concepts/harness-loop-graph]] |
| 2 | Loop engineering 是觀察—行動—驗證循環，必須有明確觸發與以證據為基礎的停止規則，而不是無盡重試。 | 同上 | [[concepts/loop-five-elements]]、[[concepts/stop-conditions]] |
| 3 | Graph engineering 以節點與邊模型工作流拓撲，控制允許的下一步、分支、併發、狀態轉移與復原路徑。 | 同上 | [[concepts/graph-nodes-edges]]、[[concepts/fallback-edges]] |
| 4 | GPT-3.5 加上四種 agentic 模式後，HumanEval 從 48.1% 提升到 95.1%；GPT-4 單次回答為 67.0%。 | 「Agentic 工作流提升 GPT-3.5」段 | [[methods/teaching-deck-pipeline]] 的教學動機 |
| 5 | 零信任五規則：僅基於證據前進、限制重試次數、終止狀態必須是驗證輸出或記錄拒絕、權限按步驟分配、開發者自己掌控圖結構。 | 「GPT-6 Astra 與零信任」段 | [[concepts/verification]]、[[concepts/stop-conditions]] |
| 6 | IAL-Scan 掃描 6,549 個 agent 倉庫，找到 68 個確定的無限 agentic 迴圈失敗，精準度 91.9%；其中 95.6% 伴隨 API 成本耗盡或模型拒絕服務。 | 「實證發現」段 | [[concepts/stop-conditions]] |
| 7 | 36,710 個工程軟體倉庫中，只有 0.59%（217 個）運行自主 agent 迴圈；多數只在 pull request 或排程觸發，且幾乎沒有狀態檔、驗證子代理或預算宣告。 | 同上 | [[concepts/verification]]、[[concepts/state-as-files]] |
| 8 | 沒有 Harness、Loop、Graph 三層，296 個 agent 只是雜訊；有這三層，才會收斂成一個可控制的結構。 | 「Harness、Loop 與 Graph」段 | [[concepts/harness-loop-graph]] |

## 本 Wiki 用到的地方

- [[concepts/harness-loop-graph]]：三層的定義與分工。
- [[concepts/verification]]：零信任五規則與證據式前進。
- [[concepts/stop-conditions]]：重試上限與無限迴圈的實證。
- [[concepts/fallback-edges]]：Graph 的復原路徑。
- [[methods/teaching-deck-pipeline]]：本作業的 Graph 設計動機。

## 限制與注意

- 這是 X 貼文的二手整理，HumanEval 與 IAL-Scan 的數字來自貼文引用的研究，本 Wiki 沒有重跑實驗。
- 「95.1%」是特定 agentic workflow 與特定基準的結果，不能推論到所有任務。
- 貼文提到的 GPT-6 Astra 是 2026 年的產品情境；本 Wiki 只引用其架構概念，不引用產品規格。

## 原始出處

- 第一篇貼文：<https://x.com/N01ennn/status/2097264706088014123>
- 第二篇貼文：<https://x.com/N01ennn/status/2096962591125905888>
- 零信任論文：Towards Agentic Cloud Engineering: Graph and Loop Engineering with a Zero-Trust Agent Harness（arXiv 2609.00050）
