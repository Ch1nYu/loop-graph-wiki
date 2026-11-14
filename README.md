# Loop / Graph Engineering — LLM Wiki 與教學簡報

這是一個以「Loop / Graph Engineering：把 AI 工作拆成可驗證的流程」為主題的 LLM Wiki，以及由 Wiki 生成的 13 頁教學 HTML 簡報。

## 公開內容

- `index.html`：教學簡報（方向鍵換頁）。
- `wiki.html`：Wiki 的人類可讀鏡像。
- `wiki/`：Wiki 的 Markdown 來源。
- `assets/`：簡報樣式與互動程式。

GitHub Pages 只會發布 `index.html`、`wiki.html` 與 `assets/`。內部工作流程、執行狀態、檢查紀錄、原始資料與繳交草稿不會出現在公開站。

## 本機驗證

```bash
python scripts/build_wiki_html.py
python scripts/run_all.py --shots
python scripts/run_all.py
```
