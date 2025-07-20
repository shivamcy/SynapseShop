from firecrawl import FirecrawlApp
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
import json


FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


firecrawl_app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def scrape_and_clean(url):
    try:
        response = firecrawl_app.scrape_url(url, formats=["html"])
        html_content = response.html
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator=' ', strip=True)[:5000]
    except Exception as e:
        return None

def ask_llm_fixed_schema(question, urls, contents):
    try:
        prompt = f"""
You are an AI assistant comparing Amazon products. Respond strictly in valid JSON format according to the following JSON schema:

```json
{{
  "products": [
    // Extract product info from the following web page texts.
  ],
  "comparisonSummary": {{
    // Include comparison details like bestValue, best dicount.
  }}
}}

Each product must have: asin, title, url, price (amount, currency), rating (average, count). Add features, brand, dimensions, pros, cons, availability, etc., if available.

DO NOT wrap the JSON in code fences.
DO NOT add explanations.
ONLY output pure JSON, conforming to the structure above.
Use the following data:
"""

        for i, (url, content) in enumerate(zip(urls, contents)):
            prompt += f"\n### Product {i+1}: {url}\n{content[:1500]}\n"

        completion = openrouter_client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": "Respond only with a valid JSON object as per the schema."},
                {"role": "user", "content": prompt.strip()}
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
