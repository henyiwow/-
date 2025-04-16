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
                categories[category].append(f"▾ {title} ({link})")
                matched = True
                break
        if not matched:
            categories.setdefault("其他", []).append(f"▾ {title} ({link})")
    return categories

# 整理訊息內容
def format_message(categories):
    today = datetime.now().strftime("%Y/%m/%d")
    lines = [f"📰【新光金控新聞摘要】{today}\n"]
    for cat, items in categories.items():
        if items:
            lines.append(f"\n📁 {cat}：")
            lines.extend(items[:3])
    return "\n".join(lines)

if __name__ == "__main__":
    news = fetch_news()
    categories = classify_news(news)
    message = format_message(categories)
    send_line_message(message)
