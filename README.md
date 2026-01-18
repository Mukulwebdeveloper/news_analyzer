# DEVELOPMENT PROCESS

## Objective
Create a dual-LLM news analysis system:
- Fetch recent news on Indian politics.
- Analyze each article for gist, sentiment, and tone using LLM#1 (Gemini).
- Validate results using LLM#2 (OpenRouter/GPT).
- Save results in JSON and human-readable Markdown.

## AI-assisted Development Philosophy
1. **LLM#1 (Gemini)**: Summarizes articles and extracts sentiment and tone.
2. **LLM#2 (OpenRouter/GPT)**: Validates the analysis to reduce errors.
3. **Modular Code**: Separation of concerns for fetching, analyzing, validating.
4. **JSON + Markdown Output**: Machine-readable + human-readable formats.
5. **No API keys in code**: Environment variables via `.env`.

## Key Design Choices
- Fallback parsing in case LLM JSON fails.
- Graceful error handling for API failures.
- Folder structure separates code, output, and tests.
- Scalable: page_size parameter controls number of articles.

## Prompts
- **Analysis Prompt**: Ask Gemini for structured JSON with gist, sentiment, and tone.
- **Validation Prompt**: Ask OpenRouter if the analysis is correct and provide corrections.

## Next Steps / Improvements
- Add caching to avoid repeated API calls.
- Use multiple LLMs in parallel for faster validation.
- Add tests for edge cases in articles (empty content, very long text).
