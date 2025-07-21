import streamlit as st
import pandas as pd
from backend import scrape_and_clean, ask_llm_fixed_schema, parse_json_response
import time

# Page configuration
st.set_page_config(
    page_title="SynapseShop", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .product-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .product-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #fff;
    }
    .feature-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 5px;
        border-left: 3px solid #ffd700;
    }
    .comparison-summary {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .step-indicator {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<h1 class="main-header">SynapseShop</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Paste the URLs and compare products intelligently with AI-powered analysis!</p>', unsafe_allow_html=True)

# Initialize session state
if 'comparison_results' not in st.session_state:
    st.session_state.comparison_results = None
if 'scraped_products' not in st.session_state:
    st.session_state.scraped_products = 0

# Sidebar with instructions
with st.sidebar:
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. **Enter URLs**: Add 2+ product URLs separated by commas
    2. **Ask Question**: Specify what you want to compare
    3. **Get Results**: Review AI-powered comparison
    4. **Select Products**: Choose which ones to compare side-by-side
    """)
    
    st.markdown("### 💡 Sample Questions")
    sample_questions = [
        "Which product offers the best value for money?",
        "Compare features and specifications",
        "Which has better customer reviews?",
        "What are the pros and cons of each?",
        "Which is best for beginners?"
    ]
    
    for q in sample_questions:
        if st.button(f"📝 {q}", key=f"sample_{q[:10]}"):
            st.session_state.sample_question = q

# Main input section
col1, col2 = st.columns([2, 1])

# Define urls_count globally to always show the metric
urls_count = 0

with col1:
    # URL input with validation
    urls_input = st.text_area(
        "🔗 Product URLs",
        placeholder="https://example.com/product1, https://example.com/product2, ...",
        help="Enter 2 or more product URLs separated by commas",
    )
    
    # URL validation and preview
    if urls_input.strip():
        urls = [u.strip() for u in urls_input.split(",") if u.strip()]
        urls_count = len(urls)
        
        if urls_count < 2:
            st.warning("⚠️ Please provide at least 2 URLs for comparison")
        else:
            st.success(f"✅ {urls_count} URLs detected")
            
            # Show URL preview in expander
            with st.expander("🔍 URL Preview", expanded=False):
                for i, url in enumerate(urls, 1):
                    st.write(f"**{i}.** {url}")

with col2:
    # Always show both metrics
  #  st.metric("Products Scraped", st.session_state.scraped_products)
    st.metric("URLs Entered", urls_count)

# Question input
question = st.text_area(
    " Comparison Question",
    value=st.session_state.get('sample_question', "Which product is best overall and why?"),
    placeholder="What would you like to know about these products?",
    help="Be specific about what aspects you want to compare",
)

# Action buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    compare_button = st.button(
        " Start Comparison", 
        type="primary",
    )


# Processing section
if compare_button:
    if not urls_input.strip() or not question.strip():
        st.markdown('<div class="error-box"> Please provide both URLs and a comparison question.</div>', unsafe_allow_html=True)
    else:
        urls = [u.strip() for u in urls_input.split(",") if u.strip()]
        
        if len(urls) < 2:
            st.markdown('<div class="error-box"> Please provide at least 2 URLs for comparison.</div>', unsafe_allow_html=True)
        else:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Scraping
            status_text.text("🕷️ Scraping product information...")
            contents = []
            failed_urls = []
            
            for i, url in enumerate(urls):
                progress_bar.progress((i + 1) / (len(urls) + 1))
                status_text.text(f"🕷️ Scraping product {i+1}/{len(urls)}...")
                
                content = scrape_and_clean(url)
                if content:
                    contents.append(content)
                else:
                    failed_urls.append(url)
                
                time.sleep(0.1)  # Small delay for better UX
            
            st.session_state.scraped_products = len(contents)
            
            # Show scraping results
            if failed_urls:
                st.markdown(f'<div class="error-box">Failed to scrape {len(failed_urls)} URLs:<br>{"<br>".join(failed_urls[:3])}</div>', unsafe_allow_html=True)
            
            if len(contents) >= 2:
                st.markdown(f'<div class="success-box">✅ Successfully scraped {len(contents)} products!</div>', unsafe_allow_html=True)
                
                # Step 2: AI Analysis
                status_text.text("AI is analyzing products...")
                progress_bar.progress(0.8)
                
                response = ask_llm_fixed_schema(question, urls[:len(contents)], contents)
                parsed = parse_json_response(response)
                
                progress_bar.progress(1.0)
                status_text.text("✅ Analysis complete!")
                time.sleep(1)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                if parsed:
                    st.session_state.comparison_results = parsed
                    
                    # Display results
                    st.markdown("---")
                    
                    # Comparison Summary
                    if "comparisonMetadata" in parsed:
                        metadata = parsed["comparisonMetadata"]
                        st.markdown('<div class="comparison-summary">', unsafe_allow_html=True)
                        st.markdown("###  Comparison Summary")
                        
                        summary_cols = st.columns(3)
                        with summary_cols[0]:
                            st.metric("Products Compared", len(parsed.get("products", [])))
                        with summary_cols[1]:
                            st.metric("Analysis Question", "Custom")
                        with summary_cols[2]:
                            st.metric("Confidence", "High")
                        
                        if "summary" in metadata:
                            st.markdown(f"**Summary:** {metadata['summary']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Product Selection
                    st.markdown("### Select Products to Compare")
                    products = parsed["products"]
                    
                    # Create product options with better formatting
                    product_options = []
                    for i, prod in enumerate(products):
                        title = prod.get('title', f'Product {i+1}')[:50]
                        product_options.append(f"{i+1}. {title}")
                    
                    selected_products = st.multiselect(
                        "Choose products for detailed comparison:",
                        options=product_options,
                        default=product_options[:min(3, len(product_options))],  # Default to first 3
                        help="Select 2-4 products for optimal comparison layout"
                    )
                    
                    if selected_products:
                        # Extract selected products
                        selected_indices = [int(item.split(".")[0]) - 1 for item in selected_products]
                        selected_data = [products[i] for i in selected_indices]
                        
                        # Display comparison
                        st.markdown("###  Detailed Comparison")
                        
                        if len(selected_data) <= 4:
                            # Side-by-side comparison for 4 or fewer products
                            cols = st.columns(len(selected_data))
                            
                            for col, product in zip(cols, selected_data):
                                with col:
                                    st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                                    st.markdown(f'<div class="product-title">{product.get("title", "Unnamed Product")}</div>', unsafe_allow_html=True)
                                    
                                    # Display features in organized way
                                    for key, value in product.items():
                                        if key != 'title':  # Skip title as it's already shown
                                            if isinstance(value, dict):
                                                st.markdown(f"**{key.replace('_', ' ').title()}**")
                                                for sub_k, sub_v in value.items():
                                                    st.markdown(f'<div class="feature-item">{sub_k}: {sub_v}</div>', unsafe_allow_html=True)
                                            elif isinstance(value, list):
                                                st.markdown(f"**{key.replace('_', ' ').title()}:** {', '.join(map(str, value))}")
                                            else:
                                                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
                                    
                                    st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            # Table format for many products
                            df_data = []
                            for product in selected_data:
                                row = {}
                                for key, value in product.items():
                                    if isinstance(value, dict):
                                        for sub_k, sub_v in value.items():
                                            row[f"{key}_{sub_k}"] = sub_v
                                    elif isinstance(value, list):
                                        row[key] = ', '.join(map(str, value))
                                    else:
                                        row[key] = value
                                df_data.append(row)
                            
                            df = pd.DataFrame(df_data)
                            st.dataframe(df, use_container_width=True)
                        
                        # Export option
                        st.markdown("### Export Results")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("Download as CSV"):
                                df = pd.json_normalize(selected_data)
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label=" Download CSV",
                                    data=csv,
                                    file_name="product_comparison.csv",
                                    mime="text/csv"
                                )
                        
                        with col2:
                            if st.button("View Raw Data"):
                                st.json(parsed)
                
                else:
                    st.markdown('<div class="error-box">⚠️ Failed to parse AI response. Please try again.</div>', unsafe_allow_html=True)
                    with st.expander("🔍 Raw Response (for debugging)"):
                        st.text(response)
            else:
                st.markdown('<div class="error-box"> Need at least 2 valid products to compare.</div>', unsafe_allow_html=True)

# Footer
# st.markdown("---")
# st.markdown("""
# <div style='text-align: center; color: #666; padding: 1rem;'>
#     <p>🤖 Powered by AI • Built by shivamcy • Made for smart shopping</p>
# </div>
# """, unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p> Built by <a href='https://github.com/shivamcy' target='_blank' style='color: #666; text-decoration: none;'>shivamcy</a> •Powered by AI • Made for smart shopping</p>
</div>
""", unsafe_allow_html=True)


