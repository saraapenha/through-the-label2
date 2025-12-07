import streamlit as st
from src.config import PAGE_CONFIG, CUSTOM_CSS

# Configuração da página
st.set_page_config(**PAGE_CONFIG)

# Aplicar CSS customizado
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Hero Section
st.title("Through the Label 🧴✨")
st.caption("Make data-driven skincare choices")

# Introdução
col1, col2 = st.columns([3, 2], gap="large")
with col1:
    st.markdown("### Your customized skincare companion 💧")
    st.write(
        "Understand the ingredients in your skincare products and discover "
        "perfect matches for your skin type. Make smarter, more informed choices."
    )
    st.write("")
    
    # Botões de ação principais
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🧬 Create Your Profile", use_container_width=True):
            st.switch_page("pages/1_Profile.py")
    with btn_col2:
        if st.button("🔍 Analyze Ingredients", use_container_width=True):
            st.switch_page("pages/3_IngredientAnalysis.py")

with col2:
    st.info("💡 **Quick Start**\n\n1. Create your profile\n2. Analyze product ingredients\n3. Get personalized recommendations")

st.divider()

# Features Section
st.markdown("## 🌟 How It Works")

feature_col1, feature_col2, feature_col3 = st.columns(3, gap="medium")

with feature_col1:
    st.markdown("### 🧬 Profile")
    st.write("Tell us about your skin type, concerns, and preferences to get personalized recommendations.")
    if st.button("Setup Profile →", key="feature_profile", use_container_width=True):
        st.switch_page("pages/1_Profile.py")

with feature_col2:
    st.markdown("### 🔍 Ingredient Analysis")
    st.write("Paste any ingredient list and discover what each component does for your skin.")
    if st.button("Analyze Now →", key="feature_analysis", use_container_width=True):
        st.switch_page("pages/3_IngredientAnalysis.py")

with feature_col3:
    st.markdown("### 🧴 Product Discovery")
    st.write("Browse our curated database of skincare products and find your perfect match.")
    if st.button("Browse Products →", key="feature_products", use_container_width=True):
        st.switch_page("pages/2_Products.py")

st.divider()

# Footer com informações adicionais
st.markdown("### 📊 Why Trust Our Analysis?")
info_col1, info_col2, info_col3, info_col4 = st.columns(4)

with info_col1:
    st.metric("Ingredients Database", "1000+", help="Comprehensive ingredient information")

with info_col2:
    st.metric("Product Catalog", "500+", help="Curated skincare products")

with info_col3:
    st.metric("Skin Types Supported", "5", help="Covers all major skin types")

with info_col4:
    if st.button("📊 View Dashboard", use_container_width=True, type="secondary"):
        st.switch_page("pages/4_Dashboard.py")



