# LINE News Bot - 新光金控每日推播

此專案會每天早上 9 點（台灣時間）自動抓取新光金控相關新聞，分類並推播到你的 LINE Bot。

## ✅ 功能說明
- 擷取來源：Google News RSS
- 分類標籤：金控、人壽、投信、銀行、不動產
- 自動推播 LINE Bot 給指定用戶或群組

## 🔧 使用教學
### 1. Fork 專案到你自己的 GitHub 帳號

### 2. 建立 LINE Bot 並取得：
- Channel access token
- 使用者 ID（LINE 內找 Webhook bot 的 ID，或用 curl 發送取得）

### 3. 到 GitHub Repo 設定 Secrets：
在「Settings > Secrets and variables > Actions > New repository secret」新增：
- `LINE_ACCESS_TOKEN`: 你的 Channel Access Token
- `LINE_TO`: 你的 LINE 使用者 ID（或群組 ID）

### 4. 開啟 GitHub Actions，等待自動執行

## ⏱ 預設排程
- 每天早上 9 點自動執行（UTC 1:00）
- 你也可以手動執行（workflow_dispatch）

## 🧪 本機測試（可選）
```bash
LINE_ACCESS_TOKEN=xxx LINE_TO=xxx python main.py
