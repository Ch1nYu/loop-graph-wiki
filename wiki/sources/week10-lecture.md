---
id: week10-lecture
title: "Week 10 課程筆記：把你的工作拆成 AI 能做的流程"
type: source
source_kind: lecture-notes
original_url: "https://www.youtube.com/live/pEmuTl9vTf8"
ingested: 2026-11-13
updated: 2026-11-13
reliability: high
coverage: [harness, loop, graph, verification, llm-wiki, teaching-deck]
---

# Week 10 課程筆記：把你的工作拆成 AI 能做的流程

## 這篇在說什麼

這是政大蔡炎龍老師「生成式 AI：文字與圖像生成的原理與實務」第 10 週的完整課程筆記，主題是 Loop、Graph 與 Workflow Prototype。課程從「老闆不能只出一張嘴」出發，說明為什麼人類親自盯場會變成人工迴圈，接著依序介紹 Harness、Loop、Graph 三層工程，最後示範如何用 LLM Wiki 與 Graph 工作流生成 HTML 簡報。

這篇是本站最主要的概念來源：Loop 的五要素、雙軌驗證、Graph 的節點與退回邊、權限隔離、State as Files，以及 Prompt / Loop / Graph 的選擇指南，都出自這份筆記。

## 關鍵主張（可引用）

| # | 主張 | 原文位置 | 本 Wiki 用到的地方 |
|---|---|---|---|
| 1 | Prompt、Loop、Graph 三者在結構上都是圖：Prompt 是單一節點，Loop 是節點加一條回到自己的邊，Graph 是多節點加條件分支與退回邊。 | §3.3「從圖論視角看三種模式」 | [[concepts/harness-loop-graph]]、[[comparisons/prompt-loop-graph]] |
| 2 | 一個完整的 Loop 必須寫清楚五件事：目標、限制、完成標準與驗證、停止條件、觸發條件。 | §3.2「設計一個 Loop 必須寫清楚的五件事」 | [[concepts/loop-five-elements]]、[[concepts/stop-conditions]] |
| 3 | 驗證必須雙軌：程式檢查負責客觀條件，獨立 AI 審查負責語意品質；絕對不要讓生成作品的同一個 AI 審自己。 | §3.2、§5.2 | [[concepts/verification]] |
| 4 | Graph 的黃金設計原則是「大圈很少轉，小圈轉得很快」；錯誤必須在離源頭最近的地方被抓到。 | §3.3「好 Graph 的黃金設計原則」 | [[concepts/fallback-edges]] |
| 5 | Graph 版簡報流程包含：檢索 → 覆蓋率關卡 → 證據卡 → 大綱 → 人類確認 → 逐頁稿 → 忠實度關卡 → 渲染 → 版面關卡 → 交件。 | §5.3(1) | [[methods/teaching-deck-pipeline]] |
| 6 | 每個節點要有資訊與權限隔離：證據卡只看單篇、逐頁稿只看大綱與卡片、渲染不能改字、檢查員不能動手改內容。 | §5.3(2) | [[concepts/information-scoping]] |
| 7 | 精準退回：某頁講錯只退回該頁、卡片錯只重抽該篇、字太多溢出要退回逐頁稿刪字，不是縮字硬塞。 | §5.3(3) | [[concepts/fallback-edges]] |
| 8 | State as Files：每個節點的狀態與產出都是實體檔案，可打開、可 diff、可單獨重跑。 | §5.3(4) | [[concepts/state-as-files]] |
| 9 | 結構選擇指南：一次性任務先用 Prompt；重複性標準任務用 Loop；多階段、需精準退回的複雜任務才拆 Graph。 | §3.3「結構選擇指南」 | [[comparisons/prompt-loop-graph]] |
| 10 | 「說『檢查一下』不算驗證；說『做好一點』不算規格。先寫好完成的定義，再決定要不要加上 loop 或 graph。」 | §6 金句 | [[concepts/verification]]、[[concepts/loop-five-elements]] |
| 11 | 一句話 Prompt 的常見慘況包含：排版爆版、數字沒有出處（課程舉例「準確率提升 37%」）、只讀了 8 篇中的 3 篇、把結論講反。 | §5.1「一句話 Prompt 版」 | [[concepts/verification]]、[[methods/teaching-deck-pipeline]] |

## 本 Wiki 用到的地方

- [[concepts/harness-loop-graph]]：三層工程的分工。
- [[concepts/loop-five-elements]]：Loop 的五個要素。
- [[concepts/verification]]：程式檢查與獨立 AI 審查。
- [[concepts/graph-nodes-edges]]：節點、邊、條件邊與狀態。
- [[concepts/fallback-edges]]：小圈與大圈、精準退回。
- [[concepts/information-scoping]]：每個節點只能看什麼。
- [[concepts/state-as-files]]：資料夾就是流程的記憶體。
- [[concepts/human-in-the-loop]]：人類在大綱與需求摘要把關。
- [[concepts/stop-conditions]]：硬上限、資料不足、成本。
- [[comparisons/prompt-loop-graph]]：三種結構的選擇。
- [[methods/llm-wiki]]：LLM Wiki 的建置與 lint。
- [[methods/teaching-deck-pipeline]]：本作業實際使用的 Graph。

## 限制與注意

- 這是課程筆記，不是同儕審查論文；講義中的數字與案例應視為教學示例，不是獨立實驗結果。
- 筆記包含講師的綜整與比喻，引用時應保留「課程認為」的語氣，不要寫成普遍定律。
- 影片時間戳與講義頁碼來自原筆記；本 Wiki 沒有逐格重看影片，因此只在必要時引用章節，不引用精確秒數。

## 原始出處

- 課程影片：<https://www.youtube.com/live/pEmuTl9vTf8>
- 第 10 週講義：<https://drive.google.com/file/d/15qN58f28Hxfl0v32z_Nbw2C3F6sEEjr8/view>
- 前導講義：<https://drive.google.com/file/d/1AbrgG4TOrNCFhvKWFABzjfwV1KXXR0yB/view>
