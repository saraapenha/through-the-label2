import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.config import PAGE_CONFIG, CUSTOM_CSS, DATA_PATHS

# Page configuration
st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("🧴 Product Catalog")
st.caption("Browse our curated skincare product database")

# Load data with cache
@st.cache_data
def load_products():
    try:
        df = pd.read_csv(DATA_PATHS["products"])
        return df
    except Exception as e:
        st.error(f"Error loading products: {e}")
        return pd.DataFrame()

df = load_products()

if df.empty:
    st.warning("No products found in database.")
    st.stop()

# General statistics
st.markdown("### 📊 Database Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Products", len(df))

with col2:
    if 'product_type' in df.columns:
        st.metric("Product Types", df['product_type'].nunique())
    else:
        st.metric("Product Types", "N/A")

with col3:
    if 'brand_name' in df.columns:
        st.metric("Brands", df['brand_name'].nunique())
    else:
        st.metric("Brands", "N/A")

with col4:
    st.metric("Categories", "Multiple")

# Visualizações do banco de dados
st.divider()
st.markdown("### 📈 Product Analytics")

tab1, tab2, tab3 = st.tabs(["📊 Product Types", "🏢 Brands", "📋 Data Table"])

with tab1:
    if 'product_type' in df.columns:
        type_counts = df['product_type'].value_counts().head(10)
        
        fig_types = px.bar(
            x=type_counts.values,
            y=type_counts.index,
            orientation='h',
            title="Top 10 Product Types",
            labels={'x': 'Quantity', 'y': 'Product Type'},
            color=type_counts.values,
            color_continuous_scale='Blues'
        )
        fig_types.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_types, use_container_width=True)
        
        # Pizza chart
        fig_pie = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="Product Type Distribution",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Product type data not available")

with tab2:
    if 'brand_name' in df.columns:
        brand_counts = df['brand_name'].value_counts().head(15)
        
        fig_brands = px.bar(
            x=brand_counts.index,
            y=brand_counts.values,
            title="Top 15 Brands by Product Count",
            labels={'x': 'Brand', 'y': 'Number of Products'},
            color=brand_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_brands.update_layout(
            height=500,
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig_brands, use_container_width=True)
        
        # Treemap
        fig_tree = px.treemap(
            names=brand_counts.index,
            parents=["" for _ in brand_counts.index],
            values=brand_counts.values,
            title="Brand Distribution (Treemap)"
        )
        fig_tree.update_layout(height=500)
        st.plotly_chart(fig_tree, use_container_width=True)
    else:
        st.info("Brand data not available")

with tab3:
    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# Filters
st.markdown("### 🔍 Filter Products")
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    # Filter by product type
    if 'product_type' in df.columns:
        product_types = ['All'] + sorted(df['product_type'].dropna().unique().tolist())
        selected_type = st.selectbox("Product Type", product_types)
    else:
        selected_type = 'All'

with filter_col2:
    # Filter by brand
    if 'brand_name' in df.columns:
        brands = ['All'] + sorted(df['brand_name'].dropna().unique().tolist())
        selected_brand = st.selectbox("Brand", brands)
    else:
        selected_brand = 'All'

# Search by name
search_query = st.text_input("🔎 Search by product name", placeholder="Enter product name...")

# Apply filters
filtered_df = df.copy()

if selected_type != 'All' and 'product_type' in df.columns:
    filtered_df = filtered_df[filtered_df['product_type'] == selected_type]

if selected_brand != 'All' and 'brand_name' in df.columns:
    filtered_df = filtered_df[filtered_df['brand_name'] == selected_brand]

if search_query and 'product_name' in df.columns:
    filtered_df = filtered_df[filtered_df['product_name'].str.contains(search_query, case=False, na=False)]

st.markdown(f"### 📦 Products ({len(filtered_df)} found)")

# View options
view_mode = st.radio(
    "View Mode",
    ["Card View", "Table View"],
    horizontal=True
)

if len(filtered_df) == 0:
    st.info("No products match your filters. Try adjusting your search criteria.")
else:
    if view_mode == "Table View":
        # Table view
        display_cols = [col for col in ['product_name', 'brand_name', 'product_type', 'product_url'] if col in filtered_df.columns]
        st.dataframe(
            filtered_df[display_cols].head(50),
            use_container_width=True,
            hide_index=True
        )
    else:
        # Card view
        for idx, row in filtered_df.head(20).iterrows():
            with st.container():
                col_a, col_b = st.columns([3, 1])
                
                with col_a:
                    product_name = row.get('product_name', 'Unknown Product')
                    brand_name = row.get('brand_name', 'Unknown Brand')
                    product_type = row.get('product_type', 'N/A')
                    
                    st.markdown(f"**{product_name}**")
                    st.caption(f"Brand: {brand_name} | Type: {product_type}")
                
                with col_b:
                    if 'product_url' in row and pd.notna(row['product_url']):
                        st.link_button("View Product", row['product_url'], use_container_width=True)
                
                st.divider()

# Navigation
st.markdown("### 🧭 Navigation")
col_nav1, col_nav2 = st.columns(2)

with col_nav1:
    if st.button("🧬 My Profile", use_container_width=True):
        st.switch_page("pages/1_Profile.py")

with col_nav2:
    if st.button("🔍 Analyze Ingredients", use_container_width=True):
        st.switch_page("pages/3_IngredientAnalysis.py")
