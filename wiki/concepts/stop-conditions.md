---
id: stop-conditions
title: "停止條件：沒有剎車的 Loop 只是燒錢"
type: concept
audience: beginner
updated: 2026-11-20
sources: [week10-lecture, agentic-workflow-humaneval, agentic-harness-kimi-k3, self-improving-coding-loop, building-effective-ai-agents]
related: [loop-five-elements, verification, fallback-edges]
---

# 停止條件：沒有剎車的 Loop 只是燒錢

> 一句話：Loop 的品質不只看它會不會改，更看它知不知道什麼時候該停。

## 為什麼停止條件是核心

課程有一句很重的話：「沒人看管的 loop，就是在沒人看管下犯錯（且燒錢）的 loop。」（[[sources/week10-lecture]] §3.2）一個沒有停止條件的 Loop，會在同一個錯誤上無限重試，消耗 token、API 費用與時間，最後還是沒有解決問題。

實證也支持這個風險：IAL-Scan 掃描 6,549 個 agent 倉庫，找到 68 個確定的無限 agentic 迴圈失敗，精準度 91.9%；其中 95.6% 伴隨 API 成本耗盡或模型拒絕服務（[[sources/agentic-workflow-humaneval]] §實證發現）。

## 五種常見剎車

### 1. 硬上限（Hard Cap）

最簡單也最可靠：最多改 3 輪（或 5 輪）。改滿就停，附上報告請人類處理。

課程的建議是：如果改了 3 輪還沒通過，代表問題出在規格或資料，應立即停下來讓人類介入（[[sources/week10-lecture]] §3.2）。3 輪是一條經驗上的界線：超過就不要再自動燒錢。

### 2. 資料不足就停（Stop on Insufficient Data）

如果知識庫裡找不到足夠資料（例如相關頁面少於 3 頁），直接停止並回報，嚴禁 AI 用預訓練知識硬湊（[[sources/week10-lecture]] §3.2）。

這條規則同時防止幻覺與「偷懶」：AI 不會因為想交差而編造內容，也不會只用最前面的 3 篇來源就假裝讀完了 8 篇。

### 3. 成本上限（Token / API / Time）

自我改進迴圈的例子用 `watcher.md` 與 `rewriter.md` 限制程式碼 ≤ 12 行、prompt 增長 ≤ 20%（[[sources/self-improving-coding-loop]] §自我改進編碼循環）。這就是用預算當剎車：如果每一輪都讓 prompt 膨脹 20%，幾輪之後就會失控。

對簡報流程，成本上限可以是：

- 最多 3 輪修改。
- 最多 15 頁。
- 最多 7 篇來源。
- 每次檢查最多 5 分鐘。

### 4. 進展停滯就停（Progress-Gated Detector）

Harness 的文章提出 Detector：用「明確缺乏進展」判斷卡住，而不是只看「有沒有在動」；並且要先寫誤報測試，避免把「正在編譯」誤判為「掛了」（[[sources/agentic-harness-kimi-k3]] §BUILD 09）。

對簡報流程的啟示：如果連續兩輪檢查都報同一個錯誤，而且修改沒有讓錯誤數量下降，就應該停下來檢查「是不是規格寫錯了」，而不是繼續重試。

### 5. Fail Closed

如果檢查腳本自己壞掉，不能默默跳過，而要視為失敗（fail closed）。Harness 的沙箱原則是：任一 canary 探針失敗就拒絕啟動，沒有降級模式（[[sources/agentic-harness-kimi-k3]] §BUILD 05）。

對本專案的啟示：`check_deck.py` 如果 crash，`run_all.py` 必須回傳非零退出碼，不能印出「檢查完成」就當作通過。

## 停止條件與零信任

零信任的五條規則裡，有三條直接跟停止有關（[[sources/agentic-workflow-humaneval]] §零信任五規則）：

- 限制重試次數，否則 swarm 永遠不會停。
- 終止狀態必須是驗證輸出或記錄拒絕，不能是「AI 說完成了」。
- 權限按步驟分配，不是整場會話都開放。

這三條可以寫成一個簡單的停止規格：

```text
停止，若：
  1. 所有檢查通過 → 交件
  2. 修改滿 3 輪 → 停止，附報告
  3. 相關來源 < 3 → 停止，不生成
  4. 連續 2 輪同一個錯誤未改善 → 停止，檢查規格
  5. 檢查腳本 crash → 停止，先修腳本
```

## 停止不是失敗

很多人把「停止」當成失敗，但其實停止是流程設計的一部分。一個好的停止條件會告訴你：

- 是資料不足，還是規格不清？
- 是 AI 不夠努力，還是這個任務不適合自動化？
- 是檢查太嚴，還是成品真的沒過？

停止後留下的報告，比無限重試更有價值。

## 反模式

| 反模式 | 問題 | 替代做法 |
|---|---|---|
| 沒有硬上限 | 無限重試，燒錢 | 設 3 輪上限 |
| 資料不足還硬做 | 幻覺、內容空洞 | 少於 3 篇就停 |
| 只看「有沒有在動」 | 把卡住誤判為有進展 | 用「錯誤數量是否下降」判斷 |
| 檢查腳本壞掉就跳過 | 以為通過，其實沒驗證 | fail closed |
| 停止後沒有報告 | 不知道為什麼停 | 附上機器可讀的檢查結果與錯誤清單 |

## 教學用法

讓學生為自己的 Loop 寫一張「停止卡」：三個停止條件、每個條件的觸發方式、停止後要附什麼報告。學生通常會發現，自己原本只寫了「做到好為止」，這等於沒有停止條件。

## 檢查清單

- [ ] 是否有硬上限（輪數、頁數、時間）？
- [ ] 是否有資料不足的停止條件？
- [ ] 是否有成本上限？
- [ ] 是否用「進展」而不是「動作」判斷卡住？
- [ ] 檢查腳本壞掉時是否 fail closed？
- [ ] 停止後是否附報告？

## 出處

- [[sources/week10-lecture]] §3.2
- [[sources/agentic-workflow-humaneval]] §零信任五規則、§實證發現
- [[sources/agentic-harness-kimi-k3]] §BUILD 05、§BUILD 09
- [[sources/self-improving-coding-loop]] §自我改進編碼循環
- [[sources/building-effective-ai-agents]] §Agents
