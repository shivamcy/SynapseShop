import streamlit as st
import pandas as pd
from backend import scrape_and_clean, ask_llm, parse_json_response

st.set_page_config(page_title="ScraperGPT", layout="wide")

st.markdown("# 🔍 Scraper + LLM (ChatGPT UI)")
st.markdown("Enter comma-separated URLs and ask your question!")

urls_input = st.text_input("🔗 Enter URLs (comma-separated)", placeholder="https://example.com, https://example.org")
question = st.text_area("❓ Ask your question about the pages")

if st.button("Run Analysis"):
    if not urls_input or not question:
        st.warning("Please provide both URLs and a question.")
    else:
        urls = [u.strip() for u in urls_input.split(",")]
        for url in urls:
            with st.expander(f"🔎 {url}", expanded=True):
                with st.spinner("Scraping and analyzing..."):
                    content = scrape_and_clean(url)
                    if content:
                        response = ask_llm(question, content)
                        if response:
                            parsed = parse_json_response(response)
                            if parsed:
                                if isinstance(parsed, dict):
                                    for k, v in parsed.items():
                                        st.subheader(k.upper())
                                        if isinstance(v, list) and v and isinstance(v[0], dict):
                                            df = pd.DataFrame(v)
                                            st.dataframe(df)
                                        elif isinstance(v, dict):
                                            st.json(v)
                                        else:
                                            st.write(v)
                                elif isinstance(parsed, list):
                                    st.dataframe(pd.DataFrame(parsed))
                                else:
                                    st.write(parsed)
                            else:
                                st.error("❌ Invalid JSON returned.")
                                st.code(response)
                        else:
                            st.error("❌ LLM failed to respond.")
                    else:
                        st.error("❌ Failed to scrape content.")
