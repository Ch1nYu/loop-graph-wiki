---
id: agentic-harness-kimi-k3
title: "How to Build An Agentic Harness using Kimi K3"
type: source
source_kind: engineering-essay
original_url: "https://x.com/Av1dlive/status/2085405823782842835"
ingested: 2026-11-13
updated: 2026-11-13
reliability: medium
coverage: [harness, gate, ledger, detector, fail-closed, capability-boundary]
---

# How to Build An Agentic Harness using Kimi K3

## 這篇在說什麼

這是一篇很長的工程文章，主張「模型是商品，Harness 才是資產」。作者把 agent 的控制層拆成 11 個 BUILD 與 7 個原語：Slot、Cell、Run、Thread、Ledger、Gate、Dial。核心訊息是：模型會一直換，但你的工作流、檢查、核准習慣與紀錄不會；因此應該把控制層建在模型之外，讓換模型變成換一個 manifest，而不是重寫整個系統。

對本 Wiki 最重要的是四個概念：**Gate**（在副作用發生處攔截）、**Ledger**（先持久化再廣播，讓每一次執行可重播）、**Detector**（用「缺乏進展」判斷卡住，避免誤報）、**Capability Boundary**（allow-list + deny-list，上限只能降不能升）。這些概念可以直接對應到 Loop/Graph 的停止條件與權限隔離。

## 關鍵主張（可引用）

| # | 主張 | 原文位置 | 本 Wiki 用到的地方 |
|---|---|---|---|
| 1 | 模型是商品，Harness 才是資產；Harness 是針對「工作」裁剪的控制層，不是針對某個模型。 | 前言、五大核心概念 | [[concepts/harness-loop-graph]] |
| 2 | 七大原語：Slot、Cell、Run、Thread、Ledger、Gate、Dial；其中 Gate 必須坐在副作用處，UI 的 gate 只是建議。 | 七大原語表 | [[concepts/information-scoping]]、[[concepts/human-in-the-loop]] |
| 3 | Ledger 是有序、僅追加的事件紀錄；先持久化再廣播，讓執行可重播、可審計。 | BUILD 02 | [[concepts/state-as-files]] |
| 4 | Detector 要用「明確缺乏進展」來判斷卡住，並先寫誤報測試；被忽略的警報等於沒有警報。 | BUILD 09 | [[concepts/stop-conditions]] |
| 5 | 能力邊界用 allow-list 與 deny-list 雙重檢查，上限只能降不能升，升級只能由人類做。 | BUILD 10 | [[concepts/stop-conditions]] |
| 6 | 沙箱要在啟動時用 canary 探針證明隔離；任一探針失敗就拒絕啟動，沒有降級模式（fail closed）。 | BUILD 05 | [[concepts/verification]] |
| 7 | 非法狀態轉移應該是可記錄的值，不是 panic；狀態表讓錯誤可顯示、可持久化。 | BUILD 03 | [[concepts/state-as-files]] |
| 8 | 每個 run 使用獨立 worktree，絕不碰使用者 checkout 的分支；reclaim 只收乾淨的 tree。 | BUILD 04 | [[concepts/information-scoping]] |

## 本 Wiki 用到的地方

- [[concepts/harness-loop-graph]]：Harness 是控制層，不是模型。
- [[concepts/information-scoping]]：Gate、權限與 worktree 隔離。
- [[concepts/state-as-files]]：Ledger 與可重播的狀態。
- [[concepts/stop-conditions]]：Detector、fail closed、能力邊界。
- [[concepts/verification]]：canary 探針與可執行驗證。
- [[concepts/human-in-the-loop]]：Gate 與人工升級。

## 限制與注意

- 這是個人工程文章，包含大量作者自己的架構主張與產品預測；本 Wiki 只引用可操作的設計原則，不把預測當事實。
- 文章中的 K3 基準數字、成本與幻覺率來自作者引用，本 Wiki 沒有獨立驗證。
- 11 個 BUILD 是特定系統的實作，不是所有 agent 都必須照抄；本 Wiki 只抽取與 Loop/Graph 有關的部分。

## 原始出處

- 原文：<https://x.com/Av1dlive/status/2085405823782842835>
- 參考實作：<https://github.com/codejunkie99/autoharness>
