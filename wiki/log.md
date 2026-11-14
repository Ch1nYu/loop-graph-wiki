---
id: log
title: "Ingest 與變更日誌"
type: log
updated: 2026-11-13
---

# Ingest 與變更日誌

## 2026-11-13：建立 Wiki 與 ingest 7 篇來源

### 需求訪談與規格

- 依使用者指定的 week 10 作業目標，以及 week 9 的 `ai-reading-notes` 專案脈絡，整理 10 題需求訪談與需求摘要。
- 建立專案手冊、簡報 Skill 與 Graph workflow 定義。
- 決定頁面類型：source、concept、comparison、method、glossary、index、log。
- 決定語言：繁體中文（台灣），專有名詞保留英文。
- 決定引用粒度：來源頁 + 章節；簡報每頁 footer 標 wiki 與原始 URL。

### Ingest 紀錄

| 時間 | 來源 ID | 來源類型 | 產出來源頁 | 主要概念頁 |
|---|---|---|---|---|
| 2026-11-13 | week10-lecture | 課程筆記 | [[sources/week10-lecture]] | harness-loop-graph、loop-five-elements、verification、graph-nodes-edges、fallback-edges、information-scoping、state-as-files、human-in-the-loop、stop-conditions、prompt-loop-graph、llm-wiki、teaching-deck-pipeline |
| 2026-11-13 | agentic-workflow-humaneval | 文章整理 | [[sources/agentic-workflow-humaneval]] | harness-loop-graph、verification、stop-conditions、fallback-edges |
| 2026-11-13 | building-effective-ai-agents | 工程文章 | [[sources/building-effective-ai-agents]] | harness-loop-graph、verification、information-scoping、stop-conditions、prompt-loop-graph |
| 2026-11-13 | langgraph-agents-course | 課程整理 | [[sources/langgraph-agents-course]] | graph-nodes-edges、state-as-files、human-in-the-loop、loop-five-elements、stop-conditions |
| 2026-11-13 | agentic-harness-kimi-k3 | 工程長文 | [[sources/agentic-harness-kimi-k3]] | harness-loop-graph、information-scoping、state-as-files、stop-conditions、verification、human-in-the-loop |
| 2026-11-13 | self-improving-coding-loop | 文章整理 | [[sources/self-improving-coding-loop]] | loop-five-elements、verification、stop-conditions、graph-nodes-edges、information-scoping、teaching-deck-pipeline |
| 2026-11-13 | ai-agent-system-design-course | 課程整理 | [[sources/ai-agent-system-design-course]] | harness-loop-graph、prompt-loop-graph、graph-nodes-edges、state-as-files、verification |

### 建立的頁面

- 概念頁 9 篇：`harness-loop-graph`、`loop-five-elements`、`verification`、`graph-nodes-edges`、`fallback-edges`、`information-scoping`、`state-as-files`、`human-in-the-loop`、`stop-conditions`。
- 比較頁 1 篇：`prompt-loop-graph`。
- 方法頁 2 篇：`llm-wiki`、`teaching-deck-pipeline`。
- 來源頁 7 篇。
- 索引、日誌、術語表各 1 篇。

### 檢查

- `python scripts/check_wiki.py`：PASS（22 頁、7 來源、0 error、0 warning）。
- `python scripts/check_deck.py`：PASS（13 頁、每頁有 Wiki 與原始來源、0 error）。
- `python scripts/render_check.py --shots`：PASS（0 overflow、0 缺引用、13 張截圖）。
- 獨立 AI 審查：PASS（忠實度、覆蓋率、教學結構、引用完整性、版面可讀性）。

以上結果取自最後一次完整執行。

## 變更紀錄

| 日期 | 變更 | 原因 |
|---|---|---|
| 2026-11-13 | 建立 Wiki 骨架與 7 篇來源頁 | week 10 作業要求 |
| 2026-11-13 | 建立 9 篇概念頁、1 篇比較頁、2 篇方法頁 | 綜整跨來源知識 |
| 2026-11-13 | 建立專案手冊、簡報 Skill 與 Graph workflow | 先討論、後生成 |
