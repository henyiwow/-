### main.py
import os
from line_helper import send_line_message
from datetime import datetime
import requests

# 分類關鍵字
CATEGORY_KEYWORDS = {
    "金控": ["金控", "控股"],
    "人壽": ["人壽", "壽險"],
    "投信": ["投信", "基金"],
    "銀行": ["銀行"],
    "不動產": ["房地產", "不動產", "建案"]
}

# 抓新聞（Google News RSS）
def fetch_news():
    url = "https://news.google.com/rss/search?q=%E6%96%B0%E5%85%89%E9%87%91%E6%8E%A7&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.content)
    items = root.findall(".//item")
    news = []
    for item in items:
        title = item.find("title").text
        link = item.find("link").text
        news.append((title, link))
    return news

# 分類新聞
def classify_news(news_list):
    categories = {k: [] for k in CATEGORY_KEYWORDS}
    for title, link in news_list:
        matched = False
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in title for kw in keywords):
                categories[category].append(f"\u25fe {title} ({link})")
                matched = True
                break
        if not matched:
            categories.setdefault("其他", []).append(f"\u25fe {title} ({link})")
    return categories

# 整理訊息內容
def format_message(categories):
    today = datetime.now().strftime("%Y/%m/%d")
    lines = [f"\ud83d\udcf0【新光金控新聞摘要】{today}\n"]
    for cat, items in categories.items():
        if items:
            lines.append(f"\n\ud83d\udcc1 {cat}：")
            lines.extend(items[:3])
    return "\n".join(lines)

if __name__ == "__main__":
    news = fetch_news()
    categories = classify_news(news)
    message = format_message(categories)
    send_line_message(message)


### line_helper.py
import os
import requests

LINE_API_URL = "https://api.line.me/v2/bot/message/push"

LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_TO = os.getenv("LINE_TO")

def send_line_message(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": LINE_TO,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    response = requests.post(LINE_API_URL, headers=headers, json=data)
    print("LINE API 回應:", response.status_code, response.text)


### .github/workflows/news.yml
name: Daily News Push

on:
  schedule:
    - cron: '0 1 * * *' # UTC時間，每日台灣早上9點
  workflow_dispatch:

jobs:
  push-news:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests

      - name: Run News Bot
        env:
          LINE_ACCESS_TOKEN: ${{ secrets.LINE_ACCESS_TOKEN }}
          LINE_TO: ${{ secrets.LINE_TO }}
        run: python main.py


### README.md
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
```

---
🎉 有任何客製需求都可以擴充，例如：分類加入 GPT 協助、寄 Email 等！
