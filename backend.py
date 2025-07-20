from firecrawl import FirecrawlApp
from bs4 import BeautifulSoup
from openai import OpenAI
import json

# Init
firecrawl_app = FirecrawlApp(api_key="fc-3ffe1575a20a4702bf710dc8ae4a43b0")
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

def scrape_and_clean(url):
    try:
        response = firecrawl_app.scrape_url(url, formats=["html"])
        html_content = response.html
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator=' ', strip=True)[:5000]
    except Exception as e:
        return None

def ask_llm(question, context):
    try:
        prompt = (
            "You are a tech analyst assistant. Respond ONLY with valid JSON format. "
            "Structure your response as a JSON object or array with key-value pairs. "
            "Do not include any text before or after the JSON. "
            f"Context: {context}\n\nQuestion: {question}"
        )
        completion = openrouter_client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            extra_headers={
                "HTTP-Referer": "https://your-site.com",
                "X-Title": "ScraperLLM",
            },
            messages=[
                {"role": "system", "content": "You are a helpful tech assistant who responds ONLY in valid JSON format. No markdown, no explanations, just pure JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return None

def parse_json_response(raw_response):
    try:
        cleaned = raw_response.strip()
        if cleaned.startswith("```json"): cleaned = cleaned[7:]
        if cleaned.endswith("```"): cleaned = cleaned[:-3]
        return json.loads(cleaned)
    except:
        return None
