import streamlit as st
import pandas as pd
from backend import scrape_and_clean, ask_llm_fixed_schema, parse_json_response

st.set_page_config(page_title=" Product Comparator", layout="wide")
st.title("🛍️ Product Comparison AI")

urls_input = st.text_input("🔗 Enter  Product URLs (comma-separated):")
question = st.text_area(" What would you like to compare?", value="Which is best overall?")

if st.button("Compare Now"):
    if not urls_input.strip() or not question.strip():
        st.warning("Please provide URLs and a comparison question.")
    else:
        urls = [u.strip() for u in urls_input.split(",") if u.strip()]
        contents = []
        failed_urls = []

        with st.spinner("Scraping product pages..."):
            for url in urls:
                content = scrape_and_clean(url)
                if content:
                    contents.append(content)
                else:
                    failed_urls.append(url)

        if failed_urls:
            st.error(f"❌ Failed to scrape: {', '.join(failed_urls)}")

        if len(contents) >= 2:
            with st.spinner("Asking LLM to compare products..."):
                response = ask_llm_fixed_schema(question, urls, contents)
                parsed = parse_json_response(response)
                if parsed:
                    # Comparison Metadata
                    # st.subheader("📄 Metadata")
                    # st.json(parsed.get("comparisonMetadata", {}))

                    # Products Table
                    # st.subheader("📦 Products")
                    # df = pd.json_normalize(parsed["products"])
                    # st.dataframe(df)
                    
                    st.subheader("The Comparison Table")

                    products = parsed["products"]

                    # Pick how many products to compare side by side (max 3–4 is ideal for layout)
                    num_to_compare = (len(products))

                    # Choose products to compare
                    selected_products = st.multiselect(
                        "Select products to compare:", 
                        options=[f"{i+1}: {prod.get('title', 'No Title')}" for i, prod in enumerate(products)],
                        default=[f"{i+1}: {products[i].get('title', 'No Title')}" for i in range(num_to_compare)]
                    )


                    # Extract selected products based on user selection
                    selected_indices = [int(item.split(":")[0]) - 1 for item in selected_products]
                    selected_data = [products[i] for i in selected_indices]

                    # Side-by-side columns
                    cols = st.columns(len(selected_data))

                    for col, product in zip(cols, selected_data):
                        with col:
                            st.markdown(f"### {product.get('title', 'Unnamed')}")
                            for key, value in product.items():
                                if isinstance(value, dict):
                                    for sub_k, sub_v in value.items():
                                        st.write(f"**{key}.{sub_k}:** {sub_v}")
                                elif isinstance(value, list):
                                    st.write(f"**{key}:** {', '.join(map(str, value))}")
                                else:
                                    st.write(f"**{key}:** {value}")

                else:
                    st.error("⚠️ Failed to parse LLM response. Check logs or try again.")
                    st.text(response)
        else:
            st.warning("Need at least two valid products to compare.")
