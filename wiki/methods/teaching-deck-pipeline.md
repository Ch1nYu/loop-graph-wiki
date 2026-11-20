---
id: teaching-deck-pipeline
title: "本專案的 Graph：從 Wiki 到 13 頁教學簡報"
type: method
audience: intermediate
updated: 2026-11-20
sources: [week10-lecture, agentic-workflow-humaneval, langgraph-agents-course, agentic-harness-kimi-k3]
related: [graph-nodes-edges, fallback-edges, verification, state-as-files]
---

# 本專案的 Graph：從 Wiki 到 13 頁教學簡報

> 一句話：這份簡報經過 7 個節點、5 個關卡、3 輪檢查才完成。

## 為什麼不用一句話 Prompt

一句話 Prompt 也能生出 HTML，但常見的結果是：排版爆版、數字沒出處、只讀了部分來源、把結論講反（[[sources/week10-lecture]] §5.1）。原因是流程裡沒有寫進「檢索、整理、檢查、退回」這幾步。

因此本專案採用 Graph 版：先把 Wiki 建好，再用 7 個節點生成簡報；每個節點都有明確的輸入、輸出與檢查。

## 七個節點

| 節點 | 做什麼 | 產出 | 檢查 | 退回 |
|---|---|---|---|---|
| **N1 檢索** | 依主題查 Wiki 索引，列出相關頁面與覆蓋率 | 檢索結果與覆蓋率 | 相關頁 ≥ 3 | 不足 → 停止 |
| **N2 證據卡** | 每篇來源抽一張卡，只放該篇的原文與位置 | 每篇來源一張證據卡 | 每卡有 URL、≥ 2 條原文 | 卡錯 → 重抽該篇 |
| **N3 大綱** | 排教學順序，標記每頁要用的 Wiki 頁 | 大綱與人類確認紀錄 | 人類確認；每頁 ≥ 1 個 Wiki 頁 | 缺子題 → 回 N1/N3 |
| **N4 逐頁稿** | 一頁一稿，寫標題、主張、例子、出處 | 每頁一份逐頁稿 | 每頁有出處；數字可回溯 | 某頁錯 → 只改該頁 |
| **N5 渲染** | 由 `deck/slides.json` 產生 `index.html` | `index.html` | 8–15 頁；無外部依賴；headless 渲染無 overflow | 版面錯 → 回 N4 刪字 |
| **N6 獨立審查** | 開新對話，只看成品與被引用的來源 | 獨立審查報告 | 忠實度、覆蓋率全過 | fail → 退回 N2 補卡或 N4 改該頁 |
| **N7 交件** | 整理報告、部署 | 檢查報告、繳交文字 | 人類最終驗收 | — |

## 五個關卡

```text
G1 覆蓋率：相關 wiki 頁 < 3 → 停止
G2 大綱：人類確認教學順序與取捨
G3 忠實度：每頁主張與數字可回溯
G4 版面：headless 渲染無 overflow、每頁有引用
G5 獨立審查：新上下文檢查忠實度與覆蓋率
```

## 狀態檔

```text
run/
├── sources.md
├── cards/
├── outline.md
├── drafts/
├── report.md
└── review.md
```

這些檔案是流程的記憶體：每一關的產出都留著，可以 diff、可以重跑、可以只退回某一關（[[sources/week10-lecture]] §5.3(4)）。

## 為什麼這樣設計

### 1. 大圈很少轉，小圈快轉

只有 G5 失敗且問題在源頭時，才退回 N1/N2；大部分錯誤在 N4 或 N5 的小圈內修掉。逐頁稿與渲染各自有 2–3 輪上限，錯誤在離源頭最近的地方被抓到（[[sources/week10-lecture]] §3.3）。

### 2. 權限隔離

證據卡不能看別篇、逐頁稿不能看卡片外、渲染不能改字、審查不能動手。這樣可以避免後面階段偷改前面的事實（[[sources/week10-lecture]] §5.3(2)）。

### 3. 雙軌驗證

程式檢查負責客觀條件（頁數、出處、數字、overflow），獨立 AI 審查負責語意品質（忠實度、覆蓋率）。生成者不審自己（[[sources/week10-lecture]] §3.2）。

### 4. 停止條件

修改滿 3 輪、相關來源 < 3、數字找不到來源、overflow 修不好、檢查腳本 crash，都會停止並附報告（[[sources/week10-lecture]] §3.2）。

## 本次執行結果

| 項目 | 結果 |
|---|---|
| 來源數 | 7 篇（week 10 課程筆記 + week 9 的 6 篇 AI 閱讀筆記） |
| Wiki 頁面 | 22 頁（7 來源、9 概念、1 比較、2 方法、index、log、glossary） |
| 簡報頁數 | 13 頁 |
| 程式檢查 | `check_wiki.py`、`check_deck.py`、`render_check.py` 全數通過 |
| 渲染檢查 | 13 頁，0 overflow，0 缺引用 |
| 獨立審查 | 忠實度、覆蓋率、教學結構、引用完整性、版面可讀性通過 |
| 修改輪數 | 3 輪（第 1 輪 2 個 overflow、第 2 輪 2 個視覺重疊、第 3 輪 0 個） |

> 這張表會在實際執行後更新；若數字與機器可讀的檢查結果不一致，以檢查結果為準。

## 實際抓到的錯誤（摘要）

1. 第 1 輪：封面 overflow 10px、Loop 頁 overflow 63px；0 頁缺引用。渲染之前，Wiki 檢查已先抓出並修掉 16 個結構問題（2 個簡體字、7 個來源頁缺 `updated`、3 個範例連結誤判、1 個方法頁來源數不足、2 個佔位標記）。
2. 第 2 輪：overflow 歸零；視覺檢查抓到 HUD 覆蓋引用 chips、pipeline 退回標籤壓到節點。
3. 第 3 輪：程式檢查與渲染檢查全過；進入獨立審查。

完整的錯誤、修正與驗證紀錄保留在執行報告。

## 與 Loop 版的差別

| 維度 | Loop 版 | 本專案 Graph 版 |
|---|---|---|
| 修正範圍 | 整份簡報重跑 | 只退回出錯的節點 |
| 檢查位置 | 主要在成品端 | 證據卡、大綱、逐頁稿、渲染都有 |
| 人類介入 | 最後看報告 | 大綱與最終驗收 |
| 成本 | 較低，但大圈很貴 | 設計成本較高，但小圈便宜 |
| 適合 | 標準明確的重複性任務 | 多階段、需精準退回的教學簡報 |

## 限制

- 本專案沒有使用 LangGraph 等框架，而是用 Python 腳本與資料夾實作 Graph；這是「Workflow Prototype」，不是生產級系統。
- 獨立 AI 審查仍然可能漏掉細微的語意問題；它不能取代人類的最終驗收。
- 7 篇來源中有 6 篇是二手整理，因此本 Wiki 的「忠實度」是對來源頁忠實，不是對原始論文逐字驗證。

## 檢查清單

- [ ] 每個節點是否有明確的輸入與輸出檔案？
- [ ] 每個關卡是否有可執行的檢查？
- [ ] 是否有退回邊與次數上限？
- [ ] 是否有獨立 AI 審查？
- [ ] 是否有實際執行紀錄與修正？

## 出處

- [[sources/week10-lecture]] §3.2、§3.3、§5.1、§5.2、§5.3
- [[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph
- [[sources/langgraph-agents-course]] §Agentic Workflow 基礎
- [[sources/agentic-harness-kimi-k3]] §BUILD 02、§BUILD 09
