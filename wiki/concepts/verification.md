---
id: verification
title: "雙軌驗證：程式檢查與獨立 AI 審查"
type: concept
audience: beginner
updated: 2026-11-20
sources: [week10-lecture, agentic-workflow-humaneval, building-effective-ai-agents, agentic-harness-kimi-k3, ai-agent-system-design-course]
related: [loop-five-elements, stop-conditions, information-scoping]
---

# 雙軌驗證：程式檢查與獨立 AI 審查

> 一句話：程式檢查負責「有沒有做到」，獨立 AI 審查負責「有沒有做對」；兩者都不能省。

## 為什麼「請 AI 檢查一下」不算驗證

課程有一句很重要的話：「說『檢查一下』不算驗證；說『做好一點』不算規格。」（[[sources/week10-lecture]] §6）因為「檢查一下」沒有定義檢查什麼、用什麼標準、誰來檢查、不通過怎麼辦。這種模糊指令會讓 AI 用「看起來差不多」的標準交差。

更嚴重的是，如果讓生成作品的同一個 AI 自己檢查，它會受到自己的生成脈絡影響，傾向於護航自己的產出。課程因此定下一條鐵則：**獨立 AI 審查必須開啟全新對話，只給成品與原始來源**（[[sources/week10-lecture]] §3.2）。

## 雙軌的分工

| 軌道 | 檢查什麼 | 誰來做 | 通過標準 |
|---|---|---|---|
| **程式檢查** | 頁數、出處、連結、數字、overflow、格式、測試 | Python / 測試腳本 / headless browser | 0 error；每個規則都有明確輸出 |
| **獨立 AI 審查** | 忠實度、覆蓋率、教學結構、語氣、遺漏 | 新上下文的 AI，只看成品與來源 | 每個 fail 都有具體位置與理由 |

這兩軌不能互相替代：程式檢查抓不到「第 6 頁把論文 A 的結論講反」，獨立 AI 審查也無法穩定抓出「第 5 頁文字溢出 3px」。兩者互補，才是完整的驗證（[[sources/week10-lecture]] §3.2、§5.2）。

## 程式檢查：把主觀標準變成可執行規則

程式檢查的原則是：**每一條規則都要能回答「哪裡錯、為什麼錯、怎麼修」**。例如：

- 簡報頁數是否在 8–15 頁之間？
- 每一頁是否都有至少一個 wiki 引用與一個原始來源？
- 引用的 wiki 頁面檔案是否真的存在？
- 簡報上的百分比數字是否能在被引用的 wiki 頁找到？
- 用 headless browser 渲染後，是否有元素超出投影片邊界？
- 是否有外部 JS/CSS 依賴，導致離線或 GitHub Pages 失效？

本專案的 `scripts/check_deck.py` 與 `scripts/render_check.py` 就是這些規則的實作。檢查結果寫成 JSON，失敗時回傳非零退出碼，讓「通過」變成一個可以重跑的結果。

## 獨立 AI 審查：新上下文、只看成品與來源

生成者會護航自己的產出；只有新上下文，才看得到自己的盲點。

獨立審查的流程：

1. 開啟一個全新的對話（fresh context），不帶生成過程的記憶。
2. 只給它「最終成品」與「被引用的 wiki 頁面」。
3. 要求它逐頁檢查忠實度（有沒有講反、腦補、斷章取義）與覆蓋率（相關的重要來源有沒有漏掉）。
4. 要求它輸出結構化的問題清單：頁碼、問題類型、原文依據、建議修法。
5. 審查者不得動手改內容，只能產出報告。

這對應到 Anthropic 的 evaluator-optimizer 模式：生成者與評估者分離，評估者依明確標準給回饋（[[sources/building-effective-ai-agents]] §Workflow: Evaluator-optimizer）。

## 證據式前進：不要相信「我覺得完成了」

零信任的第一條規則是「僅基於證據前進」：程式碼、部署、測試通過才算進展；不要相信 agent 的文字描述，也不要把「執行完畢、退出碼 0」當成有做事（[[sources/agentic-workflow-humaneval]] §零信任五規則）。

這條規則可以拆成三個實作：

- **每個節點都有產出檔案**：沒有檔案就沒有進展。
- **每個檢查都有機器可讀的結果**，例如 `pass: true`。
- **每個失敗都有位置與理由**，例如「第 6 頁的數字 37% 不在來源頁」。

## 驗證也要驗證自己：canary 與 fail closed

Harness 的工程文章提出一個很強的做法：沙箱要在啟動時用 canary 探針證明隔離，任一探針失敗就拒絕啟動，沒有降級模式（[[sources/agentic-harness-kimi-k3]] §BUILD 05）。同樣的道理可以用在簡報檢查：如果檢查腳本自己壞掉，不能默默跳過，而要 fail closed，讓我們知道「這次沒有驗證」。

另一個相關概念是「缺乏內建 eval 是 harness 的弱點」；課程提到 Hermes harness 需要自行整合 LangSmith/Langfuse 等觀測工具（[[sources/ai-agent-system-design-course]] §Agent Harness、記憶體系）。所以驗證要在設計系統時就放進去，事後再補會很難。

## 反模式

| 反模式 | 問題 | 替代做法 |
|---|---|---|
| 生成者自己審自己 | 自我護航、盲點 | 新上下文獨立審查 |
| 只寫「請檢查」 | 沒有標準，無法重跑 | 寫成可執行規則與檢查清單 |
| 只看最終成品 | 錯誤太晚才發現，退回成本高 | 在證據卡、大綱、逐頁稿就設關卡 |
| 檢查腳本壞掉就跳過 | 以為通過，其實沒驗證 | fail closed，腳本錯誤視為失敗 |
| 只檢查格式，不檢查語意 | 版面漂亮但內容講反 | 程式檢查 + 獨立 AI 審查 |

## 本專案的驗證設計

本專案有三道關卡：

1. **`check_wiki.py`**：Wiki 結構、引用、孤兒頁、來源頁欄位。
2. **`check_deck.py`**：頁數、每頁引用、百分比數字可回溯、無外部依賴。
3. **`render_check.py`**：Edge headless 渲染、overflow、缺引用、截圖。

最後再加上一次獨立 AI 審查，並留下審查報告。只有三道程式檢查與獨立審查都通過，才進入交件。

## 檢查清單

- [ ] 每一條完成標準都有對應的檢查方式？
- [ ] 程式檢查是否會回傳非零退出碼？
- [ ] 獨立審查是否使用新上下文，只給成品與來源？
- [ ] 審查報告是否有頁碼、問題類型、原文依據？
- [ ] 檢查腳本壞掉時是否 fail closed？
- [ ] 是否在越早的關卡抓到錯誤越好？

## 出處

- [[sources/week10-lecture]] §3.2、§5.2、§6
- [[sources/agentic-workflow-humaneval]] §零信任五規則
- [[sources/building-effective-ai-agents]] §Workflow: Evaluator-optimizer
- [[sources/agentic-harness-kimi-k3]] §BUILD 05、§BUILD 09
- [[sources/ai-agent-system-design-course]] §Agent Harness、記憶體系
