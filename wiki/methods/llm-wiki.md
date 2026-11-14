---
id: llm-wiki
title: "LLM Wiki 的建置方法：給 AI 讀的知識庫"
type: method
audience: beginner
updated: 2026-11-13
sources: [week10-lecture, ai-agent-system-design-course]
related: [state-as-files, verification, teaching-deck-pipeline]
---

# LLM Wiki 的建置方法：給 AI 讀的知識庫

> 一句話：LLM Wiki 不是給人看的百科全書，而是給 AI 檢索的結構化記憶。

## 什麼是 LLM Wiki

課程引用 Andrej Karpathy 的 LLM Wiki 構想：它是一種 Context Engineering 的實踐，作用類似 RAG，但不需要先架設向量資料庫與 embedding 切塊程式（[[sources/week10-lecture]] §4.1）。

LLM Wiki 的重點不是「寫得很漂亮」，而是「讓 AI 能快速找到正確的頁面、正確的段落、正確的出處」。因此它的結構比文筆重要：

- `index.md` 是檢索入口，列出所有頁面與主題。
- `sources/` 一篇來源一頁，保留原始 URL 與可引用主張。
- `concepts/` 跨來源綜整概念，每個事實都連回來源。
- `comparisons/` 並陳不同做法，幫助選擇。
- `methods/` 記錄可重複的流程。
- `glossary.md` 統一術語。
- `log.md` 記錄何時 ingest 了什麼、改了哪些頁。

## 為什麼要「先討論、後生成」

課程比較了兩種建 Wiki 的方式（[[sources/week10-lecture]] §4.1）：

- **一句話生成**：把 Karpathy 的 gist 丟給 AI，說「幫我建 Wiki」。一秒建好，但長出來的是通用規則，不符合你的主題。
- **先討論、後生成**：先讓 AI 訪談你 8–10 題，釐清讀者、頁面類型、語言、出處粒度、衝突處理、ingest 模式、下游應用、lint 規則；整理成需求摘要，確認後才建立專案規則與資料夾。

差別在於：前者是「通用模板」，後者是「你的工作流」。LLM Wiki 的價值在於貼合你的領域，而不是套用別人的結構。

## 八個設計決策

課程列舉了訪談時應該釐清的八個維度（[[sources/week10-lecture]] §4.2）：

| 維度 | 問題 | 本專案的決定 |
|---|---|---|
| 讀者是誰 | 自己、學弟妹、外行客戶，還是下游 AI？ | 大學部高年級/研究所初學者，以及下游的簡報生成 AI |
| 頁面類型 | 只有論文摘要，還是要有概念頁、比較頁、術語表？ | source、concept、comparison、method、glossary |
| 語言 | 全中文、中英雙語，還是英文？ | 繁體中文（台灣），專有名詞保留英文 |
| 出處粒度 | 只標論文，還是標到章節/頁碼？ | 每篇來源頁 + 章節；簡報每頁 footer 標 wiki 與原始 URL |
| 衝突處理 | 兩篇結論相反怎麼辦？ | 並陳雙方說法、年份、條件，標記「有爭議」 |
| ingest 模式 | 一次一篇，還是批次？ | 一次一篇，先寫來源頁，再更新概念頁 |
| 下游應用 | 簡報、文獻回顧、考題？ | 13 頁教學 HTML 簡報 |
| lint 檢查 | 死連結、孤兒頁、格式、缺出處？ | 全部檢查，見下方 |

## Ingest 的標準流程

1. 把原始資料放進獨立資料夾，設為唯讀。
2. 一次讀一篇，寫 `wiki/sources/<id>.md`：
   - frontmatter：`original_url`、`raw_file`、`ingested`、`reliability`。
   - 摘要：這篇在說什麼、為什麼重要。
   - 可引用主張表：主張、原文位置、本 Wiki 用到的地方。
   - 限制與注意：這篇的偏誤、二手性質、過期風險。
3. 更新相關的 `concepts/`、`comparisons/`、`methods/` 頁，補上 `[[sources/<id>]]` 引用。
4. 更新 `index.md` 的頁面清單與 `log.md` 的 ingest 紀錄。
5. 執行 `python scripts/check_wiki.py`，修到 0 error。

## 引用粒度

本專案的引用規則是：

- 每個事實句至少一個 `[[sources/<id>]]`。
- 數字、百分比、年份、頁數、輪數，必須能在來源頁找到。
- 引用原文時用 `> ` 區塊，保留原文，不改寫。
- 來源頁的「可引用主張」表要標原文位置（章節或段落）。
- 簡報每頁 footer 至少一個 wiki 連結與一個原始 URL。

這樣做的目的是：當讀者質疑「這句話哪來的」時，可以從簡報 → wiki → 來源頁 → 原始 URL，一路追下去。

## 衝突處理

LLM Wiki 一定會遇到來源衝突。本專案的原則是「並陳，不選邊」：

1. 同一段列出雙方說法。
2. 標註年份、實驗條件、樣本差異。
3. 如果無法判斷，明確寫「兩篇說法不同，尚無共識」。
4. 不把其中一方寫成「錯的」，除非有更強的來源。

這樣做的好處是：讀者可以看到爭議，而不是被單一說法誤導。

## Lint：Wiki 的健康檢查

`scripts/check_wiki.py` 檢查以下項目：

- frontmatter 必填欄位（id、title、type、updated、sources）。
- id 唯一。
- `index.md` 收錄所有頁面。
- 所有 `[[...]]` 連結可解析。
- 沒有孤兒頁（沒有被 index 或其他頁連結）。
- 來源頁有 `original_url`、`raw_file`、至少 3 條可引用主張。
- 概念頁至少引用 2 個來源。
- 沒有未完成的佔位文字。
- 沒有常見簡體字。

這些檢查讓 Wiki 不會隨著時間腐化：新增頁面時，index 與連結會自動被要求更新；引用斷掉時，lint 會報錯。

## 本專案的實作

- 7 篇來源：week 10 課程筆記、Harness/Loop/Graph 三層工程、Anthropic Building Effective AI Agents、LangGraph 課程、Agentic Harness、自我改進迴圈、AI Agent 系統設計課。
- 22 個 Wiki 頁面：7 篇來源、9 篇概念、1 篇比較、2 篇方法、index、log、glossary。
- 3 個檢查腳本：`check_wiki.py`、`check_deck.py`、`render_check.py`。
- 1 次獨立 AI 審查：留下獨立審查報告。

## 限制

- 本 Wiki 沒有向量檢索，靠 `index.md` 與連結手動維護；規模大了之後，可能需要加搜尋。
- 7 篇來源中有 6 篇是 week 9 的閱讀筆記（二手整理），不是原始論文；引用時已標註 `reliability: medium`。
- 本 Wiki 沒有多語言版本，只有繁體中文。

## 檢查清單

- [ ] 是否有 `index.md`、`log.md`、`sources/`、`concepts/`？
- [ ] 每篇來源是否有 `original_url` 與 `raw_file`？
- [ ] 每個事實是否有引用？
- [ ] 數字是否能在來源頁找到？
- [ ] 衝突是否並陳？
- [ ] lint 是否 0 error？

## 出處

- [[sources/week10-lecture]] §4.1、§4.2、§4.3
