import streamlit as st
import pandas as pd
from src.config import PAGE_CONFIG, CUSTOM_CSS
from src.utils import parse_ingredient_list, get_ingredient_info, recommend_products

# Page configuration
st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("🔍 Ingredient Analysis")
st.caption("Understand what's in your skincare products")

st.info(
    "📝 **How to use:** Copy the ingredient list from your product (usually found on the label or website) "
    "and paste it below. We'll analyze each ingredient and show you what it does!"
)

# Initialize session state for ingredient text
if 'ingredient_text' not in st.session_state:
    st.session_state.ingredient_text = ""

# Example
with st.expander("💡 See an example"):
    example_text = "Aqua, Glycerin, Niacinamide, Hyaluronic Acid, Tocopherol, Cetearyl Alcohol, Parfum"
    st.code(example_text)
    if st.button("Use this example"):
        st.session_state.ingredient_text = example_text
        st.rerun()

# Ingredient input
ingredient_text = st.text_area(
    "Ingredient List (INCI names, comma or semicolon separated)",
    value=st.session_state.ingredient_text,
    placeholder="Example: Aqua, Glycerin, Niacinamide, Hyaluronic Acid, Tocopherol, Parfum...",
    height=150,
    help="Paste the full ingredient list exactly as it appears on the product"
)

# Update session state with current value
if ingredient_text != st.session_state.ingredient_text:
    st.session_state.ingredient_text = ingredient_text

col_analyze, col_clear = st.columns([3, 1])

with col_analyze:
    analyze_btn = st.button("🔬 Analyze Ingredients", use_container_width=True, type="primary")

with col_clear:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.ingredient_text = ""
        st.rerun()

if analyze_btn:
    if not ingredient_text.strip():
        st.warning("⚠️ Please paste an ingredient list first.")
    else:
        with st.spinner("Analyzing ingredients..."):
            # Parse ingredients 
            ingredients = parse_ingredient_list(ingredient_text)
            
            if not ingredients:
                st.error("❌ Could not parse any ingredients. Please check your input.")
                st.stop()
            
            # Statistics
            st.success(f"✅ Found {len(ingredients)} ingredients")
            
            # Show parsed list
            with st.expander("📋 Parsed Ingredients List", expanded=False):
                st.write(", ".join([ing.title() for ing in ingredients]))
            
            st.divider()
            
            # Detailed analysis
            st.markdown("### 📊 Detailed Analysis")
            
            found_count = 0
            not_found = []
            
            for ing in ingredients:
                info = get_ingredient_info(ing)
                
                if info is None:
                    not_found.append(ing.title())
                else:
                    found_count += 1
                    with st.expander(f"✓ {info['name']}", expanded=False):
                        if info.get("short_description"):
                            st.markdown(f"*{info['short_description']}*")
                            st.write("")
                        
                        if info.get("what_is_it"):
                            st.markdown(f"**🔬 What is it?**")
                            st.write(info['what_is_it'])
                        
                        if info.get("what_does_it_do"):
                            st.markdown(f"**✨ What does it do?**")
                            st.write(info['what_does_it_do'])
                        
                        if info.get("who_is_it_good_for"):
                            st.markdown(f"**👍 Good for:**")
                            st.write(info['who_is_it_good_for'])
                        
                        if info.get("who_should_avoid"):
                            st.markdown(f"**⚠️ Who should avoid it:**")
                            st.write(info['who_should_avoid'])
                        
                        if info.get("url"):
                            st.markdown(f"[📖 Learn more]({info['url']})")
            
            # Ingredients not found
            if not_found:
                with st.expander(f"⚠️ Ingredients not in database ({len(not_found)})", expanded=False):
                    st.write("The following ingredients were not found in our database:")
                    st.write(", ".join(not_found))
            
            # Métricas
            st.divider()
            st.markdown("### 📈 Analysis Summary")
            
            met_col1, met_col2, met_col3 = st.columns(3)
            with met_col1:
                st.metric("Total Ingredients", len(ingredients))
            with met_col2:
                st.metric("In Database", found_count)
            with met_col3:
                coverage = (found_count/len(ingredients)*100) if len(ingredients) > 0 else 0
                st.metric("Coverage", f"{coverage:.0f}%")
            
            # Gráfico de cobertura
            coverage_data = {
                'Category': ['Found in Database', 'Not Found'],
                'Count': [found_count, len(not_found)]
            }
            
            import plotly.express as px
            fig_coverage = px.pie(
                coverage_data,
                values='Count',
                names='Category',
                title='Ingredient Database Coverage',
                color='Category',
                color_discrete_map={'Found in Database': '#10b981', 'Not Found': '#ef4444'},
                hole=0.4
            )
            fig_coverage.update_layout(height=400)
            st.plotly_chart(fig_coverage, use_container_width=True)
            
            # Tabela comparativa de ingredientes encontrados
            if found_count > 0:
                st.markdown("### 📋 Ingredient Comparison Table")
                
                ingredient_data = []
                for ing in ingredients:
                    info = get_ingredient_info(ing)
                    if info:
                        ingredient_data.append({
                            'Ingredient': info.get('name', ing),
                            'Category': (info.get('what_is_it', 'N/A')[:40] + '...') if len(info.get('what_is_it', '')) > 40 else info.get('what_is_it', 'N/A'),
                            'Main Benefit': (info.get('what_does_it_do', 'N/A')[:50] + '...') if len(info.get('what_does_it_do', '')) > 50 else info.get('what_does_it_do', 'N/A'),
                            'Good For': (info.get('who_is_it_good_for', 'N/A')[:40] + '...') if len(info.get('who_is_it_good_for', '')) > 40 else info.get('who_is_it_good_for', 'N/A')
                        })
                
                if ingredient_data:
                    import pandas as pd
                    df_ingredients = pd.DataFrame(ingredient_data)
                    st.dataframe(df_ingredients, use_container_width=True, hide_index=True)
            
            # Product Recommendations
            if ingredients:
                st.divider()
                st.markdown("### 🎯 Recommended Products")
                st.caption("Products with similar ingredient profiles")
                
                try:
                    recs = recommend_products(ingredients, top_k=5)
                    
                    if len(recs) == 0:
                        st.info("No similar products found in our database.")
                    else:
                        # Gráfico de similaridade
                        import plotly.graph_objects as go
                        
                        fig_similarity = go.Figure(data=[
                            go.Bar(
                                x=recs['product_name'],
                                y=recs['similarity'] * 100,
                                marker_color='#10b981',
                                text=[f"{val*100:.1f}%" for val in recs['similarity']],
                                textposition='auto',
                            )
                        ])
                        fig_similarity.update_layout(
                            title="Product Match Score",
                            xaxis_title="Product",
                            yaxis_title="Similarity (%)",
                            height=400,
                            xaxis_tickangle=-45,
                            showlegend=False
                        )
                        st.plotly_chart(fig_similarity, use_container_width=True)
                        
                        # Lista de produtos
                        st.markdown("#### Product Details")
                        for idx, row in recs.iterrows():
                            with st.container():
                                col1, col2 = st.columns([4, 1])
                                
                                with col1:
                                    st.markdown(f"**{row['product_name']}**")
                                    st.caption(f"{row['product_type']} | Match: {row['similarity']*100:.1f}%")
                                
                                with col2:
                                    if pd.notna(row.get('product_url')):
                                        st.link_button("View", row['product_url'], use_container_width=True)
                                
                                st.divider()
                except Exception as e:
                    st.warning(f"Could not generate recommendations: {e}")

# Navigation
st.divider()
st.markdown("### 🧭 Navigation")
col_nav1, col_nav2 = st.columns(2)

with col_nav1:
    if st.button("🧬 My Profile", use_container_width=True):
        st.switch_page("pages/1_Profile.py")

with col_nav2:
    if st.button("🧴 Browse Products", use_container_width=True):
        st.switch_page("pages/2_Products.py")
