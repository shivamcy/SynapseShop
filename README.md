# SynapseShop 

This is an AI-powered product comparison tool built with **Streamlit**, which scrapes product details from e-commerce URLs (like Amazon, Flipkart, etc.) and lets users ask natural language questions like:

> _"Which monitor has the best display quality?"_

## 🚀 Features

- 📦 Accepts multiple product URLs (comma-separated)
- 🧠 Uses an LLM to intelligently compare products based on your query
- 🧽 Web scraping and text cleaning under the hood
- 💬 Conversational interface using OpenAI
- 📊 Outputs structured comparisons in a clean UI

---

## 🖼️ Demo Output


---

## 🔧 Setup Locally

```bash
git clone https://github.com/shivamcy/scraper.git
cd scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Create .env
```bash
FIRECRAWL_API_KEY=your_key
OPENROUTER_API_KEY=your_key
```

## Developer
     Shivam Chaudhary
    GitHub: shivamcy

    “Wearing the straw hat while building Grand Line Exchange ☠️”



