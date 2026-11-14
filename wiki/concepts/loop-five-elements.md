---
id: loop-five-elements
title: "Loop 的五個要素：目標、限制、驗證、剎車、觸發"
type: concept
audience: beginner
updated: 2026-11-13
sources: [week10-lecture, agentic-workflow-humaneval, building-effective-ai-agents, self-improving-coding-loop, langgraph-agents-course]
related: [harness-loop-graph, verification, stop-conditions]
---

# Loop 的五個要素：目標、限制、驗證、剎車、觸發

> 一句話：Loop 不是「一直試」，而是「一份會自己判斷下一步的規格」。

## 為什麼需要五個要素

沒有目標，AI 不知道要做什麼；沒有完成標準，AI 不知道什麼時候算做完；沒有停止條件，AI 會無限重試；沒有觸發，這個 Loop 永遠不會開始。課程把這些整理成五個必寫項目，前三項是「當老闆」的三件事，後兩項是讓迴圈安全自動化的關鍵（[[sources/week10-lecture]] §3.2）。

這五個要素也對應到零信任的五條規則：僅基於證據前進、限制重試次數、終止狀態必須是驗證輸出或記錄拒絕、權限按步驟分配、開發者自己掌控圖結構（[[sources/agentic-workflow-humaneval]] §零信任五規則）。

## 五個要素

### 1. 目標（Goal）

**要產出什麼？格式、檔名、存放位置、給誰看？**

目標要具體到可以驗收，例如「產出 13 頁的 `index.html`，每頁至少一個 wiki 引用與一個原始來源，放在專案根目錄」。不要寫「做一份簡報」這種無法驗收的目標。

目標不清楚時，AI 會用最省力的方式交差；例如只讀 3 篇來源就開始寫，或把別人的內容混進來（[[sources/week10-lecture]] §5.1）。

### 2. 限制（Constraints）

**哪些可以做、哪些不能做？**

限制包含：可讀寫的檔案、不可修改的原始資料、不可使用的來源、不可超出的頁數、不可改變的語氣與語言。限制的作用是縮小搜尋空間，讓 AI 不會「自作主張」。

例如本專案的規則規定：原始資料唯讀、只能使用 Wiki 的內容、不得把個人隱私或 API Key 放進公開檔案。

### 3. 完成標準與驗證（Completion Criteria & Verification）

**怎麼知道做完了？誰來檢查？**

完成標準要包含兩軌：

- **程式檢查**：頁數、出處、數字、連結、overflow 等客觀條件，用腳本判斷。
- **獨立 AI 審查**：忠實度、覆蓋率、教學結構等語意品質，用新上下文判斷。

課程的核心鐵則是：**絕對不要叫生出作品的同一個 AI 審自己的作品**；審查必須開啟全新對話，只給成品與原始來源（[[sources/week10-lecture]] §3.2）。

Anthropic 的 evaluator-optimizer 模式也是同一個思路：一個 LLM 生成，另一個 LLM 依標準評估並回饋（[[sources/building-effective-ai-agents]] §Workflow: Evaluator-optimizer）。

### 4. 停止條件／剎車（Stop Conditions）

**做不到或卡住時，什麼時候停？**

常見的剎車有三種：

- **硬上限**：最多改 3 輪；改滿就停，附報告請人類處理。
- **資料不足就停**：相關來源少於 3 篇就停止，不用預訓練知識硬湊。
- **成本上限**：token、API 費用、時間或 prompt 增長幅度的上限。

自我改進迴圈的例子用 `watcher.md` 與 `rewriter.md` 限制程式碼 ≤ 12 行、prompt 增長 ≤ 20%，這就是用預算當剎車（[[sources/self-improving-coding-loop]] §自我改進編碼循環）。

### 5. 觸發條件（Trigger）

**什麼時候開始跑？**

觸發可以是手動指令（`/topic-slides`）、檔案更新、排程或事件。沒有觸發條件，Loop 只是一個躺在資料夾裡的規格。

在 LangGraph 裡，節點之間的邊與條件邊就是觸發機制；狀態改變或條件成立時，控制權才往下一個節點走（[[sources/langgraph-agents-course]] §Agentic Workflow 基礎）。

## 一份可用的 Loop 規格

```text
目標：產出 13 頁教學簡報 index.html，每頁有 wiki 與原始來源引用。
限制：只能使用 Wiki 知識庫；原始資料唯讀；8–15 頁；繁體中文；不得新增事實。
驗證：
  1. python scripts/check_deck.py → 0 error
  2. python scripts/render_check.py → 0 overflow
  3. 獨立 AI 審查 → 忠實度與覆蓋率 pass
停止：
  1. 全過 → 交件
  2. 改滿 3 輪 → 停止，附報告
  3. 相關 wiki 頁 < 3 → 停止，不生成
觸發：/topic-slides "Loop / Graph Engineering"
```

## 常見誤解

| 誤解 | 為什麼錯 | 正確做法 |
|---|---|---|
| 「完成標準就是『看起來不錯』」 | 主觀標準無法自動判斷，也無法累積。 | 把標準拆成可執行的檢查與獨立的語意審查。 |
| 「停止條件會讓 AI 偷懶」 | 沒有停止條件才會讓 AI 無限燒錢。 | 用硬上限與資料不足條件，讓失敗可被看見。 |
| 「Loop 越大越好」 | 大 Loop 每次都要整份重跑，成本高、錯誤定位難。 | 把大 Loop 拆成多個小 Loop，錯在哪裡就修哪裡。 |
| 「AI 自己說做完就是做完」 | 生成者的自我評估有偏見。 | 用程式檢查 + 獨立 AI 審查。 |

## 教學用法

用「請 AI 做一份簡報」當反例，讓學生列出：目標是什麼？限制是什麼？怎麼驗收？什麼時候停？誰來觸發？通常學生會發現自己只寫了目標，其他四項都沒寫。接著把五要素補齊，再比較「有 Loop」與「沒 Loop」的差異。

如果學生寫不出這張表，通常不是 AI 不夠強，而是還沒決定「完成」長什麼樣子。

## 檢查清單

- [ ] 目標是否具體到可以驗收？
- [ ] 限制是否包含可動與不可動的檔案？
- [ ] 驗證是否同時有程式檢查與獨立 AI 審查？
- [ ] 停止條件是否包含硬上限、資料不足、成本？
- [ ] 觸發條件是否明確？
- [ ] 是否避免讓生成者審自己？

## 出處

- [[sources/week10-lecture]] §3.1、§3.2、§5.1、§5.2
- [[sources/agentic-workflow-humaneval]] §零信任五規則
- [[sources/building-effective-ai-agents]] §Workflow: Evaluator-optimizer
- [[sources/self-improving-coding-loop]] §自我改進編碼循環
- [[sources/langgraph-agents-course]] §Agentic Workflow 基礎
