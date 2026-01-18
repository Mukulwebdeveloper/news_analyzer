import os
import json
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found in environment variables")

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def fetch_news(query="India politics", page_size=10):
    """
    Fetch latest news articles from NewsAPI
    """
    articles = newsapi.get_everything(
        q=query,
        language="en",
        sort_by="publishedAt",
        page_size=page_size
    )["articles"]

    output_file = "output/raw_articles.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    print(f"Fetched {len(articles)} articles. Saved to {output_file}")
    return articles
