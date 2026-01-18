import pytest
from llm_analyzer import analyze_article
from llm_validator import validate_analysis

sample_article = {
    "title": "India passes new education reform",
    "description": "The government approves new policy changes",
    "content": "Full text about the education reform policy.",
    "source": {"name": "Times of India"},
    "url": "https://timesofindia.indiatimes.com/..."
}

def test_analyze_article():
    result = analyze_article(sample_article)
    assert "gist" in result
    assert "sentiment" in result
    assert "tone" in result

def test_validate_analysis():
    analysis = {"gist": "Education policy updated", "sentiment": "positive", "tone": "analytical"}
    validation = validate_analysis(sample_article, analysis)
    assert isinstance(validation, str)
    assert len(validation) > 0
