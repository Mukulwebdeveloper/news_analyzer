import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def analyze_article(article):
    """
    Analyze a single news article using Gemini LLM
    Returns a dict with gist, sentiment, tone
    """
    title = article.get("title", "")
    description = article.get("description", "")
    content = article.get("content", "")

    full_text = f"Title: {title}\nDescription: {description}\nContent: {content}"

    prompt = f"""
    You are a professional news analyst.
    Analyze the following article and return JSON with keys:
    - gist: 1-2 sentence summary
    - sentiment: positive/negative/neutral
    - tone: urgent/analytical/satirical/balanced/other

    Article:
    {full_text}
    """

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        # Attempt to parse as JSON
        import json
        try:
            result = json.loads(result_text)
        except:
            # Fallback: simple extraction
            result = {
                "gist": result_text,
                "sentiment": "neutral",
                "tone": "balanced"
            }
    except Exception as e:
        result = {
            "gist": f"Error: {str(e)}",
            "sentiment": "neutral",
            "tone": "balanced"
        }

    return result
