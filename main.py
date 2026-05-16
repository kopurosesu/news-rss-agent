import feedparser
from datetime import date
from email.utils import parsedate_to_datetime


def load_feeds(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def is_today(entry):
    if "published" not in entry:
        return False

    try:
        published_dt = parsedate_to_datetime(entry.published)
        return published_dt.date() == date.today()
    except Exception:
        return False


def main():
    feed_urls = load_feeds("feeds.txt")
    today_articles = []

    for url in feed_urls:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            if is_today(entry):
                today_articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                    "site": feed.feed.get("title", "Unknown")
                })

    markdown_text = "# 今日更新されたニュース一覧\n\n"

    if not today_articles:
        markdown_text += "今日更新された記事は見つかりませんでした。\n"
    else:
        for i, article in enumerate(today_articles, start=1):
            markdown_text += f"## {i}. {article['title']}\n\n"
            markdown_text += f"- サイト: {article['site']}\n"
            markdown_text += f"- 公開日時: {article['published']}\n"
            markdown_text += f"- URL: {article['link']}\n\n"

    with open("today_news.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)

    print("today_news.md に保存しました。")


if __name__ == "__main__":
    main()