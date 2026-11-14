---
id: self-improving-coding-loop
title: "用 DeepSeek V4 Flash 在 Codex 建立自我改進編碼循環"
type: source
source_kind: article-summary
original_url: "https://x.com/cyrilXBT/status/2088542962854629672"
ingested: 2026-11-13
updated: 2026-11-13
reliability: medium
coverage: [loop, evaluator, log, prompt-rewrite, cost]
---

# 用 DeepSeek V4 Flash 在 Codex 建立自我改進編碼循環

## 這篇在說什麼

這篇筆記整理兩件事：第一，如何在 Codex 裡用三個模型建立自我改進的編碼循環——DEEPSEEK 執行任務、LUNA 評估並寫入 `log.md`、SOL 依評估重寫 `prompt.md`；並用 `watcher.md` 與 `rewriter.md` 限制程式碼不超過 12 行、prompt 增長不超過 20%。第二，一套 10 週的 Graph Architect 課程，涵蓋知識圖譜、實體解析、代理圖設計與作品集。

對本 Wiki 最重要的是「迴圈要有紀錄與預算」：`log.md` 是評估紀錄，`prompt.md` 是下一輪的輸入，`watcher.md` / `rewriter.md` 是防止迴圈失控的規則。這正是 Loop Engineering 的具體樣貌：不是無盡重試，而是每一輪都留下可檢查的狀態。

## 關鍵主張（可引用）

| # | 主張 | 原文位置 | 本 Wiki 用到的地方 |
|---|---|---|---|
| 1 | 三模型循環：DEEPSEEK 執行、LUNA 評估並寫 `log.md`、SOL 依評估重寫 `prompt.md`。 | 「自我改進編碼循環」段 | [[concepts/loop-five-elements]]、[[concepts/verification]] |
| 2 | `watcher.md` 與 `rewriter.md` 限制程式碼 ≤ 12 行、prompt 增長 ≤ 20%，用預算防止迴圈失控。 | 同上 | [[concepts/stop-conditions]] |
| 3 | 把 Opus 5 換成 DeepSeek v4-flash，在不犧牲品質的前提下降低自動迭代的成本。 | 同上 | [[concepts/stop-conditions]] |
| 4 | Graph Architect 的知識圖譜四階段：Extract、Resolve、Assemble、Query；實體解析是最被低估的步驟。 | 「知識圖譜四階段」段 | [[concepts/graph-nodes-edges]] |
| 5 | 代理圖三大承諾：不可變計畫、分離層級、嚴格升級；用可審計性換取靈活度。 | 「代理圖三大承諾」段 | [[concepts/information-scoping]]、[[concepts/stop-conditions]] |
| 6 | 作品集的價值不在複雜度，而在誠實記錄失敗模式；從第 1 週起建立錯誤日誌。 | 「作品集」與「錯誤日誌」段 | [[methods/teaching-deck-pipeline]] 的反思 |

## 本 Wiki 用到的地方

- [[concepts/loop-five-elements]]：三模型循環與每輪紀錄。
- [[concepts/verification]]：評估者與執行者分離。
- [[concepts/stop-conditions]]：prompt 增長上限與成本意識。
- [[concepts/graph-nodes-edges]]：知識圖譜與代理圖。
- [[concepts/information-scoping]]：不可變計畫與分離層級。
- [[methods/teaching-deck-pipeline]]：錯誤日誌與誠實紀錄。

## 限制與注意

- 這是 X 貼文的二手整理，三模型循環的實際效果與成本節省來自作者說法，本 Wiki 沒有重跑。
- 「12 行」、「20%」是該特定系統的規則，不是通用標準；本 Wiki 只引用「用預算限制迴圈」的原則。
- Graph Architect 課程與本 Wiki 的 Graph Engineering 相關，但不是同一套方法；不要混為一談。

## 原始出處

- 原文：<https://x.com/cyrilXBT/status/2088542962854629672>
