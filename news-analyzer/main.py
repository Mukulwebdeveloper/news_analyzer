import os
import json
from datetime import datetime

from news_fetcher import fetch_news
from llm_analyzer import analyze_article
from llm_validator import validate_analysis


def main():
    print("\n===== Starting News Analyzer =====\n")

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Step 1: Fetch news
    print("Fetching latest articles...")
    articles = fetch_news(query="India politics", page_size=10)

    if not articles:
        print("No articles fetched. Exiting.")
        return

    analysis_results = []

    # Step 2: Analyze + Validate each article
    for idx, article in enumerate(articles, 1):
        title = article.get("title", "No Title")
        print(f"\nAnalyzing Article {idx}: {title}")

        try:
            analysis = analyze_article(article)
        except Exception as e:
            print(f"Error in analysis: {e}")
            analysis = {
                "gist": "Analysis failed",
                "sentiment": "unknown",
                "tone": "unknown"
            }

        try:
            validation = validate_analysis(article, analysis)
        except Exception as e:
            print(f"Error in validation: {e}")
            validation = f"Validation failed: {str(e)}"

        analysis_results.append({
            "title": title,
            "url": article.get("url", ""),
            "source": article.get("source", {}).get("name", "Unknown"),
            "gist": analysis.get("gist", ""),
            "sentiment": analysis.get("sentiment", ""),
            "tone": analysis.get("tone", ""),
            "validation": validation
        })

    # Step 3: Save JSON results
    results_file = "output/analysis_results.json"

    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=4)

    print(f"\nAnalysis results saved to: {results_file}")

    # Step 4: Generate Markdown Report
    report_file = "output/final_report.md"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# News Analysis Report\n\n")

        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Articles Analyzed:** {len(analysis_results)}\n")
        f.write("**Source:** NewsAPI\n\n")

        # Sentiment summary
        positive = sum(1 for a in analysis_results if a["sentiment"].lower() == "positive")
        negative = sum(1 for a in analysis_results if a["sentiment"].lower() == "negative")
        neutral = sum(1 for a in analysis_results if a["sentiment"].lower() == "neutral")

        f.write("## Summary\n")
        f.write(f"- Positive: {positive} articles\n")
        f.write(f"- Negative: {negative} articles\n")
        f.write(f"- Neutral: {neutral} articles\n\n")

        f.write("## Detailed Analysis\n\n")

        for idx, a in enumerate(analysis_results, 1):
            f.write(f"### Article {idx}: \"{a['title']}\"\n")
            f.write(f"- **Source:** [{a['source']}]({a['url']})\n")
            f.write(f"- **Gist:** {a['gist']}\n")
            f.write(f"- **LLM#1 Sentiment:** {a['sentiment']}\n")
            f.write(f"- **LLM#2 Validation:** {a['validation']}\n")
            f.write(f"- **Tone:** {a['tone']}\n\n")

    print(f"Final report generated at: {report_file}")
    print("\n===== Process Completed Successfully =====\n")


if __name__ == "__main__":
    main()
