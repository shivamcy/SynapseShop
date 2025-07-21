
# import streamlit as st
# import pandas as pd
# from backend import scrape_and_clean, ask_llm_fixed_schema, parse_json_response
# import time

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="SynapseShop | AI Product Comparison", 
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Custom CSS for Enhanced UI ---
# st.markdown("""
# <style>
#     /* Main App Body */
#     .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#         max-width: 1200px;
#     }
    
#     /* Headers */
#     .main-header {
#         text-align: center;
#         font-size: 3.5rem;
#         font-weight: 700;
#         color: #2c3e50;
#         margin-bottom: 0.5rem;
#     }
#     .sub-header {
#         text-align: center;
#         color: #7f8c8d;
#         font-size: 1.25rem;
#         margin-bottom: 3rem;
#     }

#     /* Input & Control Panel */
#     .control-panel {
#         background-color: #ffffff;
#         padding: 2rem;
#         border-radius: 15px;
#         box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
#         border: 1px solid #e0e0e0;
#         margin-bottom: 2rem;
#     }

#     /* Product Comparison Cards */
#     .product-card {
#         background: #ffffff;
#         padding: 1.5rem;
#         border-radius: 15px;
#         margin: 1rem 0;
#         height: 100%;
#         box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
#         border: 1px solid #e0e0e0;
#         display: flex;
#         flex-direction: column;
#     }
#     .product-title {
#         font-size: 1.4rem;
#         font-weight: 600;
#         color: #2c3e50;
#         margin-bottom: 1rem;
#         border-bottom: 2px solid #3498db;
#         padding-bottom: 0.5rem;
#     }
#     .product-section-header {
#         font-weight: bold;
#         color: #3498db;
#         margin-top: 1rem;
#         margin-bottom: 0.5rem;
#         font-size: 1rem;
#     }
#     .feature-item-pro {
#         font-size: 0.9rem;
#         background: rgba(46, 204, 113, 0.1);
#         padding: 0.5rem;
#         margin: 0.3rem 0;
#         border-radius: 5px;
#         border-left: 3px solid #2ecc71;
#     }
#     .feature-item-con {
#         font-size: 0.9rem;
#         background: rgba(231, 76, 60, 0.1);
#         padding: 0.5rem;
#         margin: 0.3rem 0;
#         border-radius: 5px;
#         border-left: 3px solid #e74c3c;
#     }
#     .feature-item-spec {
#         font-size: 0.9rem;
#         background: rgba(236, 240, 241, 0.7);
#         padding: 0.5rem;
#         margin: 0.3rem 0;
#         border-radius: 5px;
#     }

#     /* Summary & Status Boxes */
#     .comparison-summary {
#         background: linear-gradient(135deg, #3498db, #2980b9);
#         padding: 2rem;
#         border-radius: 15px;
#         color: white;
#         margin-top: 2rem;
#     }
#     .status-box {
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 1rem 0;
#         text-align: center;
#         font-weight: 500;
#     }
#     .error-box {
#         background: #fbebeb; color: #c0392b; border: 1px solid #e74c3c;
#     }
#     .success-box {
#         background: #eafaf1; color: #27ae60; border: 1px solid #2ecc71;
#     }
    
#     /* Footer */
#     .footer {
#         text-align: center;
#         color: #95a5a6;
#         padding: 2rem;
#         font-size: 0.9rem;
#     }
#     .footer a {
#         color: #3498db;
#         text-decoration: none;
#         font-weight: 600;
#     }
# </style>
# """, unsafe_allow_html=True)

# # --- Header ---
# st.markdown('<h1 class="main-header">SynapseShop 🤖</h1>', unsafe_allow_html=True)
# st.markdown('<p class="sub-header">Paste URLs to compare products with AI-powered analysis.</p>', unsafe_allow_html=True)

# # --- Session State Initialization ---
# if 'comparison_results' not in st.session_state:
#     st.session_state.comparison_results = None
# if 'scraped_products' not in st.session_state:
#     st.session_state.scraped_products = 0
# if 'sample_question' not in st.session_state:
#     st.session_state.sample_question = "Which product is best overall and why? Consider features, price, and reviews."

# # --- Sidebar ---
# with st.sidebar:
#     st.markdown("### 📋 How to Use")
#     st.markdown("""
#     1.  **Enter URLs**: Paste at least 2 product URLs.
#     2.  **Ask Question**: Frame your comparison query.
#     3.  **Compare**: Hit the button to start the analysis.
#     4.  **Review**: Get a detailed, side-by-side breakdown.
#     """)
    
#     st.markdown("---")
#     st.markdown("### 💡 Sample Questions")
#     sample_questions = [
#         "Which product offers the best value for money?",
#         "Compare the key features and specifications.",
#         "Which has better customer reviews and overall sentiment?",
#         "What are the main pros and cons of each product?",
#         "Which is more suitable for a beginner?"
#     ]
    
#     for q in sample_questions:
#         if st.button(f"📝 Use: '{q}'", key=f"sample_{q[:15]}"):
#             st.session_state.sample_question = q
#             st.rerun()

# # --- Main Input & Control Panel ---
# with st.container():
#     st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    
#     urls_input = st.text_area(
#         "**🔗 Enter Product URLs** (one per line or separated by commas)",
#         placeholder="https://www.amazon.in/dp/B0CQ3278V4\nhttps://www.flipkart.com/oneplus-nord-ce4/p/itm1b3924cfc39d8",
#         height=120,
#         help="Enter 2 or more product URLs for comparison."
#     )
    
#     question = st.text_area(
#         "**❓ What do you want to compare?**",
#         value=st.session_state.get('sample_question', ""),
#         placeholder="e.g., 'Compare the camera quality and battery life.'",
#         help="Be specific for the best results."
#     )
    
#     st.write("") # Spacer
#     compare_button = st.button(
#         "🚀 Start AI Comparison", 
#         type="primary",
#         use_container_width=True
#     )
    
#     st.markdown('</div>', unsafe_allow_html=True)

# # --- Processing and Results ---
# if compare_button:
#     urls_list = [u.strip() for u in urls_input.replace(',', '\n').split('\n') if u.strip()]
    
#     if len(urls_list) < 2 or not question.strip():
#         st.markdown('<div class="status-box error-box">⚠️ Please provide at least 2 URLs and a comparison question.</div>', unsafe_allow_html=True)
#     else:
#         progress_bar = st.progress(0, text="Initializing...")
#         status_text = st.empty()
        
#         # Step 1: Scraping
#         contents, failed_urls = [], []
#         for i, url in enumerate(urls_list):
#             progress_value = (i + 1) / (len(urls_list) + 1)
#             progress_bar.progress(progress_value, text=f"🕷️ Scraping product {i+1}/{len(urls_list)}...")
            
#             content = scrape_and_clean(url)
#             if content:
#                 contents.append(content)
#             else:
#                 failed_urls.append(url)
#             time.sleep(0.1)
        
#         st.session_state.scraped_products = len(contents)
        
#         if failed_urls:
#             st.markdown(f'<div class="status-box error-box">Could not scrape {len(failed_urls)} URLs. They might be protected or invalid.</div>', unsafe_allow_html=True)

#         if len(contents) < 2:
#             st.markdown('<div class="status-box error-box">Need at least 2 valid products to compare. Please check URLs and try again.</div>', unsafe_allow_html=True)
#             progress_bar.empty()
#         else:
#             st.markdown(f'<div class="status-box success-box">✅ Successfully scraped {len(contents)} products!</div>', unsafe_allow_html=True)
            
#             # Step 2: AI Analysis
#             progress_bar.progress(0.8, text="🧠 AI is analyzing the products...")
#             response = ask_llm_fixed_schema(question, urls_list[:len(contents)], contents)
#             parsed = parse_json_response(response)
            
#             progress_bar.progress(1.0, text="✅ Analysis Complete!")
#             time.sleep(1)
#             progress_bar.empty()
            
#             if parsed:
#                 st.session_state.comparison_results = parsed
#             else:
#                 st.markdown('<div class="status-box error-box">⚠️ Failed to parse AI response. The content might be complex. Please try a different query.</div>', unsafe_allow_html=True)
#                 with st.expander("🔍 Show Raw Response (for debugging)"):
#                     st.text(response)

# # --- Display Results ---
# if st.session_state.comparison_results:
#     results = st.session_state.comparison_results
    
#     # --- Comparison Summary ---
#     if "comparisonMetadata" in results:
#         metadata = results["comparisonMetadata"]
#         st.markdown('<div class="comparison-summary">', unsafe_allow_html=True)
#         st.markdown(f"### 📊 AI Analysis Summary")
#         st.markdown(f"**Overall Recommendation:** {metadata.get('summary', 'No summary provided.')}")
#         st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown("---")
    
#     # --- Detailed Comparison View ---
#     st.markdown("### ⚖️ Side-by-Side Comparison")
#     products = results.get("products", [])
    
#     if products:
#         product_options = [f"{i+1}. {prod.get('title', f'Product {i+1}')[:60]}..." for i, prod in enumerate(products)]
        
#         selected_products_options = st.multiselect(
#             "Choose products to display:",
#             options=product_options,
#             default=product_options[:min(4, len(product_options))],
#             help="Select up to 4 products for the best side-by-side view."
#         )
        
#         if selected_products_options:
#             selected_indices = [int(item.split('.')[0]) - 1 for item in selected_products_options]
#             selected_data = [products[i] for i in selected_indices if i < len(products)]
            
#             # Display logic: Side-by-side for <= 4, table for > 4
#             if len(selected_data) <= 4:
#                 cols = st.columns(len(selected_data))
#                 for col, product in zip(cols, selected_data):
#                     with col:
#                         st.markdown('<div class="product-card">', unsafe_allow_html=True)
#                         st.markdown(f'<div class="product-title">{product.get("title", "Unnamed Product")}</div>', unsafe_allow_html=True)
                        
#                         # Render sections dynamically (Pros, Cons, Specs, etc.)
#                         for key, value in product.items():
#                             if key.lower() == 'title': continue
                            
#                             if isinstance(value, list) and value:
#                                 st.markdown(f"<div class='product-section-header'>{key.replace('_', ' ').title()}</div>", unsafe_allow_html=True)
#                                 item_class = 'feature-item-pro' if 'pro' in key.lower() else 'feature-item-con' if 'con' in key.lower() else 'feature-item-spec'
#                                 for item in value:
#                                     st.markdown(f'<div class="{item_class}">{item}</div>', unsafe_allow_html=True)
                                    
#                             elif isinstance(value, dict) and value:
#                                 st.markdown(f"<div class='product-section-header'>{key.replace('_', ' ').title()}</div>", unsafe_allow_html=True)
#                                 for sub_k, sub_v in value.items():
#                                     st.markdown(f'<div class="feature-item-spec"><b>{sub_k.title()}:</b> {sub_v}</div>', unsafe_allow_html=True)

#                         st.markdown('</div>', unsafe_allow_html=True)
#             else:
#                 # Fallback to DataFrame for more than 4 selections
#                 st.info("ℹ️ More than 4 products selected. Displaying as a table for clarity.")
#                 df_data = pd.json_normalize(selected_data)
#                 st.dataframe(df_data, use_container_width=True)

#             # --- Export Options ---
#             st.markdown("---")
#             st.markdown("### 💾 Export & Data")
#             export_cols = st.columns(3)
#             with export_cols[0]:
#                 df_to_download = pd.json_normalize(selected_data)
#                 st.download_button(
#                     label="📥 Download as CSV",
#                     data=df_to_download.to_csv(index=False).encode('utf-8'),
#                     file_name="product_comparison.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )
#             with export_cols[1]:
#                 if st.button("📄 View Raw JSON", use_container_width=True):
#                     st.json(results)

# # --- Footer ---
# st.markdown("---")
# st.markdown("""
# <div class='footer'>
#     <p>Built by <a href='https://github.com/shivamcy' target='_blank'>shivamcy</a> • Powered by AI for smarter shopping</p>
# </div>
# """, unsafe_allow_html=True)