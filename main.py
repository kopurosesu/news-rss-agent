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

    if not today_articles:
        print("今日更新された記事は見つかりませんでした。")
        return

    print("今日更新された記事一覧")
    print()

    for i, article in enumerate(today_articles, start=1):
        print(f"{i}. {article['title']}")
        print(f"   サイト: {article['site']}")
        print(f"   公開日時: {article['published']}")
        print(f"   URL: {article['link']}")
        print()


if __name__ == "__main__":
    main()