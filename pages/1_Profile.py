import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.config import (
    PAGE_CONFIG, CUSTOM_CSS, SKIN_TYPES, AGE_GROUPS, SKIN_CONCERNS,
    SENSITIVITY_LEVELS, FRAGRANCE_PREFERENCES, CLIMATE_OPTIONS,
    SUN_EXPOSURE_OPTIONS, BUDGET_MIN, BUDGET_MAX, BUDGET_DEFAULT, DATA_PATHS
)
from src.utils import load_products

# Page configuration
st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("🧬 Your Skin Profile")
st.caption("Tell us about your skin to get personalized recommendations")

# Initialize session state
if "profile" not in st.session_state:
    st.session_state["profile"] = {}

# Show current profile if exists
if st.session_state.get("profile"):
    with st.expander("👤 Current Profile", expanded=False):
        profile = st.session_state["profile"]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Skin Type:** {profile.get('skin_type', 'N/A')}")
            st.markdown(f"**Age Group:** {profile.get('age_group', 'N/A')}")
            st.markdown(f"**Sensitivity:** {profile.get('sensitivity', 'N/A')}")
            st.markdown(f"**Budget:** CHF {profile.get('budget', 'N/A')}")
        with col2:
            st.markdown(f"**Concerns:** {', '.join(profile.get('concerns', [])) or 'None'}")
            st.markdown(f"**Fragrance:** {profile.get('fragrance', 'N/A')}")
            st.markdown(f"**Climate:** {profile.get('climate', 'N/A')}")
            st.markdown(f"**Sun Exposure:** {profile.get('sun', 'N/A')}")
    
    # Visualização do perfil
    st.divider()
    st.markdown("### 📊 Profile Visualization")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # Gauge para sensibilidade
        sensitivity_value = {"Low": 33, "Medium": 66, "High": 100}.get(profile.get('sensitivity', 'Medium'), 50)
        fig_sensitivity = go.Figure(go.Indicator(
            mode="gauge+number",
            value=sensitivity_value,
            title={'text': "Skin Sensitivity Level"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#ef4444"},
                'steps': [
                    {'range': [0, 33], 'color': "#d1fae5"},
                    {'range': [33, 66], 'color': "#fef3c7"},
                    {'range': [66, 100], 'color': "#fee2e2"}
                ],
            }
        ))
        fig_sensitivity.update_layout(height=250)
        st.plotly_chart(fig_sensitivity, use_container_width=True)
    
    with viz_col2:
        # Gauge para budget
        budget_percentage = (profile.get('budget', BUDGET_DEFAULT) / BUDGET_MAX) * 100
        fig_budget = go.Figure(go.Indicator(
            mode="gauge+number",
            value=profile.get('budget', BUDGET_DEFAULT),
            title={'text': "Budget (CHF)"},
            gauge={
                'axis': {'range': [BUDGET_MIN, BUDGET_MAX]},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [BUDGET_MIN, 25], 'color': "#dbeafe"},
                    {'range': [25, 50], 'color': "#93c5fd"},
                    {'range': [50, BUDGET_MAX], 'color': "#60a5fa"}
                ],
            }
        ))
        fig_budget.update_layout(height=250)
        st.plotly_chart(fig_budget, use_container_width=True)
    
    # Gráfico de preocupações
    if profile.get('concerns'):
        concerns_data = {concern: 1 for concern in profile.get('concerns', [])}
        fig_concerns = go.Figure(data=[
            go.Bar(
                x=list(concerns_data.keys()),
                y=list(concerns_data.values()),
                marker_color='#8b5cf6',
                text=list(concerns_data.keys()),
                textposition='auto',
            )
        ])
        fig_concerns.update_layout(
            title="Your Skin Concerns",
            xaxis_title="",
            yaxis_title="Selected",
            height=300,
            showlegend=False,
            yaxis={'visible': False}
        )
        st.plotly_chart(fig_concerns, use_container_width=True)
    
    # Recomendações personalizadas baseadas no perfil
    st.divider()
    st.markdown("### 🎯 Personalized Product Recommendations")
    st.caption("Based on your skin profile and concerns")
    
    try:
        # Carregar produtos
        df_products = load_products(DATA_PATHS["products"])
        
        if not df_products.empty:
            # Filtrar produtos baseado no perfil
            filtered_products = df_products.copy()
            
            # Filtrar por tipo de pele (se houver coluna relevante)
            skin_type = profile.get('skin_type', '').lower()
            concerns = [c.lower() for c in profile.get('concerns', [])]
            budget = profile.get('budget', BUDGET_DEFAULT)
            
            # Filtrar por orçamento
            if 'price' in filtered_products.columns:
                # Converter preços para numérico
                filtered_products['price_numeric'] = filtered_products['price'].str.replace('£', '').str.replace(',', '').astype(float)
                filtered_products = filtered_products[filtered_products['price_numeric'] <= budget]
            
            # Pontuação baseada nas preocupações
            if concerns and 'product_name' in filtered_products.columns:
                def score_product(row):
                    score = 0
                    product_name = str(row.get('product_name', '')).lower()
                    product_type = str(row.get('product_type', '')).lower()
                    
                    # Palavras-chave para cada preocupação
                    concern_keywords = {
                        'acne': ['acne', 'salicylic', 'bha', 'clarifying', 'purifying'],
                        'aging': ['anti-aging', 'retinol', 'peptide', 'collagen', 'wrinkle'],
                        'hyperpigmentation': ['brightening', 'vitamin c', 'niacinamide', 'dark spot', 'pigment'],
                        'redness': ['calming', 'soothing', 'centella', 'redness', 'sensitive'],
                        'dryness': ['hydrating', 'moisturizing', 'hyaluronic', 'ceramide', 'barrier'],
                        'dullness': ['brightening', 'glow', 'vitamin c', 'exfoliat', 'radiance'],
                        'dark circles': ['eye', 'caffeine', 'dark circle', 'under-eye', 'brightening'],
                        'large pores': ['pore', 'refining', 'minimizing', 'niacinamide', 'aha'],
                        'oiliness': ['oil control', 'mattifying', 'sebum', 'balancing', 'clay']
                    }
                    
                    for concern in concerns:
                        keywords = concern_keywords.get(concern, [])
                        for keyword in keywords:
                            if keyword in product_name or keyword in product_type:
                                score += 2
                    
                    # Bonus para tipo de pele
                    if skin_type and skin_type in product_name:
                        score += 1
                    
                    return score
                
                filtered_products['relevance_score'] = filtered_products.apply(score_product, axis=1)
                filtered_products = filtered_products.sort_values('relevance_score', ascending=False)
            
            # Mostrar top 5 recomendações
            top_recommendations = filtered_products.head(5)
            
            if len(top_recommendations) > 0:
                for idx, (_, product) in enumerate(top_recommendations.iterrows(), 1):
                    with st.container():
                        col_img, col_info = st.columns([1, 3])
                        
                        with col_img:
                            st.markdown(f"### #{idx}")
                        
                        with col_info:
                            product_name = product.get('product_name', 'Unknown Product')
                            product_type = product.get('product_type', 'N/A')
                            price = product.get('price', 'N/A')
                            
                            st.markdown(f"**{product_name}**")
                            st.markdown(f"*Type:* {product_type} | *Price:* {price}")
                            
                            # Mostrar por que foi recomendado
                            if 'relevance_score' in product and product['relevance_score'] > 0:
                                st.markdown(f"✨ *Match score:* {int(product['relevance_score'])} points")
                            
                            if 'product_url' in product and product['product_url']:
                                st.markdown(f"[View Product]({product['product_url']})")
                        
                        st.divider()
            else:
                st.info("💡 No products found matching your profile. Try adjusting your budget or check the Products page for more options.")
        else:
            st.warning("Product database is currently empty.")
    
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")

st.divider()

# Profile Form
with st.form("profile_form", clear_on_submit=False):
    st.markdown("### 📋 Basic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        skin_type = st.selectbox(
            "Skin Type *",
            SKIN_TYPES,
            help="Select your primary skin type"
        )
    
    with col2:
        age_group = st.selectbox(
            "Age Group",
            AGE_GROUPS,
            help="Your age range helps us recommend appropriate products"
        )

    st.markdown("### 🎯 Skin Concerns")
    concerns = st.multiselect(
        "Select up to 3 main concerns",
        SKIN_CONCERNS,
        help="Choose the skin issues you'd like to address",
        max_selections=3
    )
    
    if len(concerns) > 3:
        st.warning("⚠️ Please select up to 3 concerns for best results.")

    st.markdown("### ⚙️ Preferences")
    col3, col4 = st.columns(2)
    
    with col3:
        sensitivity = st.selectbox(
            "Skin Sensitivity",
            SENSITIVITY_LEVELS,
            help="How reactive is your skin to new products?"
        )
        
        fragrance = st.selectbox(
            "Fragrance Preference",
            FRAGRANCE_PREFERENCES,
            help="Do you prefer fragrance-free products?"
        )
    
    with col4:
        climate = st.selectbox(
            "Your Climate",
            CLIMATE_OPTIONS,
            help="Your local climate affects product needs"
        )
        
        sun = st.selectbox(
            "Sun Exposure",
            SUN_EXPOSURE_OPTIONS,
            help="How much time do you spend outdoors?"
        )

    st.markdown("### 💰 Budget")
    budget = st.slider(
        "Budget per Product (CHF)",
        min_value=BUDGET_MIN,
        max_value=BUDGET_MAX,
        value=BUDGET_DEFAULT,
        help="Set your preferred price range"
    )

    st.write("")  # Spacing
    col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 1])
    
    with col_submit2:
        submit = st.form_submit_button("💾 Save Profile", use_container_width=True)

    if submit:
        if len(concerns) <= 3:
            st.session_state["profile"] = {
                "skin_type": skin_type,
                "age_group": age_group,
                "concerns": concerns,
                "sensitivity": sensitivity,
                "fragrance": fragrance,
                "budget": budget,
                "climate": climate,
                "sun": sun,
            }
            st.success("✅ Profile saved successfully!")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Please select a maximum of 3 concerns.")

# Navigation
st.divider()
st.markdown("### What's Next?")
col_nav1, col_nav2 = st.columns(2)

with col_nav1:
    if st.button("🔍 Analyze Ingredients", use_container_width=True):
        st.switch_page("pages/3_IngredientAnalysis.py")

with col_nav2:
    if st.button("🧴 Browse Products", use_container_width=True):
        st.switch_page("pages/2_Products.py")

