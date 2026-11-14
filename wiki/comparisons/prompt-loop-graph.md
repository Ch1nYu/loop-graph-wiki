---
id: prompt-loop-graph
title: "Prompt、Loop、Graph 怎麼選？"
type: comparison
audience: beginner
updated: 2026-11-13
sources: [week10-lecture, agentic-workflow-humaneval, building-effective-ai-agents, ai-agent-system-design-course]
related: [harness-loop-graph, loop-five-elements, graph-nodes-edges]
---

# Prompt、Loop、Graph 怎麼選？

> 一句話：不要問「哪個比較高級」，要問「這個任務需要多少結構」。

## 三種結構的比較

| 維度 | Prompt | Loop | Graph |
|---|---|---|---|
| **結構** | 單一節點 `A` | 節點 `A` + 回到自己的邊 `A ↺` | 多節點 `A → B → C` + 條件邊 + 退回邊 |
| **誰決定下一步** | 人類即時決定 | AI 在人類定的規格內決定 | 人類事先畫好的流程決定 |
| **撰寫內容** | 這一輪要做什麼 | 目標、完成標準、驗證、停止規則 | 節點、邊、條件、狀態、退回路線 |
| **撰寫次數** | 每一輪都要寫 | 寫一次，系統自動跑很多輪 | 寫一次流程，可重複使用 |
| **出錯怎麼修** | 人類肉眼發現、手動下指令 | 整份再跑一輪修正 | 錯在哪一關，退回哪一關 |
| **人在哪裡介入** | 全程隨時在場 | 最後驗收看報告 | 事先指定的關鍵關卡（如大綱） |
| **最適合** | 一次性、個人臨時使用 | 標準明確的重複性任務 | 多階段、需精準退回的複雜任務 |
| **成本** | 低（但人類時間高） | 中（token 較高） | 高（設計與維護成本高） |

這張表改寫自課程的「結構選擇指南」（[[sources/week10-lecture]] §3.3），並補上成本與介入點的觀察。

## 決策樹

結構是為了重複與複雜度，不是為了好看。

```text
這個任務會做幾次？
├─ 只做一次，而且我馬上會看結果
│   └─ 先用 Prompt
├─ 會重複做，而且每次的修正指令都差不多
│   └─ 升級成 Loop
└─ 會重複做，而且有多個階段、不同驗收標準、需要精準退回
    └─ 拆成 Graph
```

如果還不確定，先用 Prompt 做一次，觀察自己重複說了哪些修正指令；那些指令就是 Loop 的規格。如果 Loop 每次都要整份重跑，而且不同階段的檢查不一樣，那就是 Graph 的訊號（[[sources/week10-lecture]] §3.3）。

## 三種結構的實際例子

### Prompt 的例子

「幫我把這段文字翻成英文。」這是一次性任務，人類馬上會看結果，不需要 Loop 或 Graph。

### Loop 的例子

「每週把新文章整理成固定格式的筆記，直到通過格式檢查。」這是重複性任務，有明確的完成標準，適合 Loop。

### Graph 的例子

「從 Wiki 檢索 → 抽證據卡 → 寫大綱 → 人類確認 → 寫逐頁稿 → 渲染 → 檢查 → 獨立審查。」這是多階段任務，每個階段有不同的驗收標準，且需要精準退回，適合 Graph（[[sources/week10-lecture]] §5.3）。

## Loop 與 Graph 不是互斥

課程強調：「Graph 決定大流程，Loop 負責每一格內部的反覆修正。」（[[sources/week10-lecture]] §5.3(3)）一個 Graph 裡的每個節點，都可以自帶一個小 Loop。

例如：

- 逐頁稿節點：寫 → 對來源 → 修改（最多 2 輪）。
- 渲染節點：產生 HTML → 截圖 → 修版面（最多 3 輪）。
- 獨立審查節點：審查 → 回報 → 退回（最多 1 輪）。

所以實務上常見的是「Graph 內含 Loop」，而不是二選一。

## 常見錯誤

| 錯誤 | 為什麼會發生 | 怎麼避免 |
|---|---|---|
| 用 Prompt 做重複性任務 | 一開始沒想清楚任務會重複 | 先做一次，觀察重複的修正指令 |
| 用 Loop 做多階段任務 | 以為 Loop 可以處理所有事 | 區分階段的驗收標準，拆成 Graph |
| 用 Graph 做一次性任務 | 為了炫技，過度設計 | 先問「這個任務會做幾次？」 |
| Graph 沒有退回邊 | 只畫了往前，沒有畫往後 | 每個檢查關卡都要有「不通過去哪」 |
| Loop 沒有停止條件 | 只寫了「做到好」 | 補上硬上限、資料不足、成本 |

## 教學用法

給學生三個任務，請他們選 Prompt / Loop / Graph，並說明理由：

1. 把一段文字翻成英文。
2. 每週整理 5 篇論文成固定格式。
3. 從知識庫生成一份 13 頁教學簡報。

通常第 1 題是 Prompt、第 2 題是 Loop、第 3 題是 Graph。追問「如果第 3 題只做一次，還需要 Graph 嗎？」可以帶出「結構是為了重複與複雜度，不是為了好看」。

## 檢查清單

- [ ] 這個任務會做幾次？
- [ ] 修正指令是否每次都差不多？
- [ ] 是否有多個階段、不同驗收標準？
- [ ] 是否需要精準退回？
- [ ] 是否先用最簡單的結構，真的不夠才升級？

## 出處

- [[sources/week10-lecture]] §3.3、§5.3
- [[sources/agentic-workflow-humaneval]] §Harness、Loop 與 Graph
- [[sources/building-effective-ai-agents]] §When (and when not) to use agents
- [[sources/ai-agent-system-design-course]] §第四階段
