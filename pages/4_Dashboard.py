import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.config import PAGE_CONFIG, CUSTOM_CSS, DATA_PATHS
from src.utils import load_products
from src.utils.ingredient_utils import load_ingredient_data
import ast

# Page configuration
st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("📊 Dashboard & Statistics")
st.caption("Comprehensive overview of the skincare database")

# Load data
@st.cache_data
def load_all_data():
    products_df = load_products()
    ingredients_df = load_ingredient_data()
    return products_df, ingredients_df

products_df, ingredients_df = load_all_data()

# KPIs principais
st.markdown("### 🎯 Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    total_products = len(products_df) if not products_df.empty else 0
    st.metric("Total Products", f"{total_products:,}")

with kpi_col2:
    total_ingredients = len(ingredients_df) if not ingredients_df.empty else 0
    st.metric("Ingredients Database", f"{total_ingredients:,}")

with kpi_col3:
    if not products_df.empty and 'brand_name' in products_df.columns:
        total_brands = products_df['brand_name'].nunique()
        st.metric("Unique Brands", f"{total_brands:,}")
    else:
        st.metric("Unique Brands", "N/A")

with kpi_col4:
    if not products_df.empty and 'product_type' in products_df.columns:
        total_types = products_df['product_type'].nunique()
        st.metric("Product Categories", f"{total_types:,}")
    else:
        st.metric("Product Categories", "N/A")

st.divider()

# Tabs para diferentes visualizações
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Products Overview",
    "🧪 Ingredients Insights",
    "🏢 Brand Analysis",
    "📈 Advanced Analytics"
])

# TAB 1: Products Overview
with tab1:
    st.markdown("### Product Distribution")
    
    if not products_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de tipos de produtos
            if 'product_type' in products_df.columns:
                type_counts = products_df['product_type'].value_counts().head(10)
                
                fig_types = px.bar(
                    x=type_counts.values,
                    y=type_counts.index,
                    orientation='h',
                    title="Top 10 Product Types",
                    labels={'x': 'Count', 'y': 'Product Type'},
                    color=type_counts.values,
                    color_continuous_scale='Blues'
                )
                fig_types.update_layout(height=500, showlegend=False)
                st.plotly_chart(fig_types, use_container_width=True)
        
        with col2:
            # Pizza chart de distribuição
            if 'product_type' in products_df.columns:
                top_types = products_df['product_type'].value_counts().head(8)
                
                fig_pie = px.pie(
                    values=top_types.values,
                    names=top_types.index,
                    title="Product Type Distribution (Top 8)",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_layout(height=500)
                st.plotly_chart(fig_pie, use_container_width=True)
        
        # Treemap de produtos por marca e tipo
        if 'brand_name' in products_df.columns and 'product_type' in products_df.columns:
            st.markdown("### Product Hierarchy")
            
            # Preparar dados para treemap
            brand_type_counts = products_df.groupby(['brand_name', 'product_type']).size().reset_index(name='count')
            top_brands = products_df['brand_name'].value_counts().head(10).index
            filtered_data = brand_type_counts[brand_type_counts['brand_name'].isin(top_brands)]
            
            fig_tree = px.treemap(
                filtered_data,
                path=['brand_name', 'product_type'],
                values='count',
                title='Product Distribution by Brand and Type (Top 10 Brands)',
                color='count',
                color_continuous_scale='Viridis'
            )
            fig_tree.update_layout(height=600)
            st.plotly_chart(fig_tree, use_container_width=True)
    else:
        st.info("No product data available")

# TAB 2: Ingredients Insights
with tab2:
    st.markdown("### Ingredient Analysis")
    
    if not products_df.empty and 'clean_ingreds' in products_df.columns:
        # Extrair todos os ingredientes
        all_ingredients = []
        for idx, row in products_df.iterrows():
            try:
                if isinstance(row['clean_ingreds'], str):
                    ingreds = ast.literal_eval(row['clean_ingreds'])
                elif isinstance(row['clean_ingreds'], list):
                    ingreds = row['clean_ingreds']
                else:
                    continue
                
                all_ingredients.extend([ing.lower().strip() for ing in ingreds if ing])
            except:
                continue
        
        if all_ingredients:
            ingredient_counts = pd.Series(all_ingredients).value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top ingredientes
                top_ingredients = ingredient_counts.head(20)
                
                fig_ing = px.bar(
                    x=top_ingredients.values,
                    y=top_ingredients.index,
                    orientation='h',
                    title="Top 20 Most Common Ingredients",
                    labels={'x': 'Frequency', 'y': 'Ingredient'},
                    color=top_ingredients.values,
                    color_continuous_scale='Teal'
                )
                fig_ing.update_layout(height=600, showlegend=False)
                st.plotly_chart(fig_ing, use_container_width=True)
            
            with col2:
                # Estatísticas de ingredientes
                st.markdown("#### 📊 Ingredient Statistics")
                
                st.metric("Total Unique Ingredients", f"{len(ingredient_counts):,}")
                st.metric("Total Ingredient Mentions", f"{len(all_ingredients):,}")
                st.metric("Average per Product", f"{len(all_ingredients)/len(products_df):.1f}")
                
                # Top 10 em tabela
                st.markdown("#### 🏆 Top 10 Ingredients")
                top_10_df = pd.DataFrame({
                    'Ingredient': top_ingredients.head(10).index,
                    'Frequency': top_ingredients.head(10).values
                })
                st.dataframe(top_10_df, use_container_width=True, hide_index=True)
            
            # Wordcloud alternativo - bubble chart
            st.markdown("### Ingredient Frequency Visualization")
            top_30 = ingredient_counts.head(30)
            
            fig_bubble = px.scatter(
                x=range(len(top_30)),
                y=top_30.values,
                size=top_30.values,
                text=top_30.index,
                title="Top 30 Ingredients Bubble Chart",
                labels={'x': '', 'y': 'Frequency'},
                color=top_30.values,
                color_continuous_scale='Viridis'
            )
            fig_bubble.update_traces(textposition='top center')
            fig_bubble.update_layout(height=500, showlegend=False, xaxis={'visible': False})
            st.plotly_chart(fig_bubble, use_container_width=True)
    else:
        st.info("No ingredient data available")

# TAB 3: Brand Analysis
with tab3:
    st.markdown("### Brand Insights")
    
    if not products_df.empty and 'brand_name' in products_df.columns:
        brand_counts = products_df['brand_name'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top marcas
            top_brands = brand_counts.head(20)
            
            fig_brands = px.bar(
                x=top_brands.index,
                y=top_brands.values,
                title="Top 20 Brands by Product Count",
                labels={'x': 'Brand', 'y': 'Number of Products'},
                color=top_brands.values,
                color_continuous_scale='Sunset'
            )
            fig_brands.update_layout(
                height=500,
                xaxis_tickangle=-45,
                showlegend=False
            )
            st.plotly_chart(fig_brands, use_container_width=True)
        
        with col2:
            # Distribuição de marcas
            st.markdown("#### 📈 Brand Distribution")
            
            st.metric("Total Brands", f"{len(brand_counts):,}")
            st.metric("Largest Brand", f"{brand_counts.index[0]} ({brand_counts.values[0]} products)")
            st.metric("Average Products/Brand", f"{brand_counts.mean():.1f}")
            
            # Percentual das top 10
            top_10_percentage = (brand_counts.head(10).sum() / brand_counts.sum()) * 100
            st.metric("Top 10 Brands Share", f"{top_10_percentage:.1f}%")
        
        # Sunburst chart
        if 'product_type' in products_df.columns:
            st.markdown("### Brand-Product Relationship")
            
            brand_type = products_df.groupby(['brand_name', 'product_type']).size().reset_index(name='count')
            top_brands_list = brand_counts.head(15).index
            filtered_bt = brand_type[brand_type['brand_name'].isin(top_brands_list)]
            
            fig_sun = px.sunburst(
                filtered_bt,
                path=['brand_name', 'product_type'],
                values='count',
                title='Product Categories by Brand (Top 15 Brands)',
                color='count',
                color_continuous_scale='RdYlGn'
            )
            fig_sun.update_layout(height=700)
            st.plotly_chart(fig_sun, use_container_width=True)
    else:
        st.info("No brand data available")

# TAB 4: Advanced Analytics
with tab4:
    st.markdown("### Advanced Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Database Completeness")
        
        if not products_df.empty:
            completeness_data = {}
            for col in products_df.columns:
                non_null = products_df[col].notna().sum()
                completeness = (non_null / len(products_df)) * 100
                completeness_data[col] = completeness
            
            # Top 10 colunas mais completas
            sorted_completeness = dict(sorted(completeness_data.items(), key=lambda x: x[1], reverse=True)[:10])
            
            fig_complete = px.bar(
                x=list(sorted_completeness.values()),
                y=list(sorted_completeness.keys()),
                orientation='h',
                title="Data Completeness by Field (Top 10)",
                labels={'x': 'Completeness (%)', 'y': 'Field'},
                color=list(sorted_completeness.values()),
                color_continuous_scale='RdYlGn'
            )
            fig_complete.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_complete, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Growth Simulation")
        
        # Criar dados simulados de crescimento
        import numpy as np
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        products_growth = [total_products * (1 + i*0.05) for i in range(6)]
        ingredients_growth = [total_ingredients * (1 + i*0.03) for i in range(6)]
        
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Scatter(
            x=months, y=products_growth,
            mode='lines+markers',
            name='Products',
            line=dict(color='#3b82f6', width=3)
        ))
        fig_growth.add_trace(go.Scatter(
            x=months, y=ingredients_growth,
            mode='lines+markers',
            name='Ingredients',
            line=dict(color='#10b981', width=3)
        ))
        
        fig_growth.update_layout(
            title="Database Growth Projection",
            xaxis_title="Month",
            yaxis_title="Count",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_growth, use_container_width=True)
    
    # Correlation heatmap (se houver dados numéricos)
    st.markdown("### 🔥 Data Insights")
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        if not products_df.empty and 'product_type' in products_df.columns:
            diversity_score = products_df['product_type'].nunique() / len(products_df) * 100
            fig_diversity = go.Figure(go.Indicator(
                mode="gauge+number",
                value=diversity_score,
                title={'text': "Product Diversity Score"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#8b5cf6"},
                    'steps': [
                        {'range': [0, 33], 'color': "#fee2e2"},
                        {'range': [33, 66], 'color': "#fef3c7"},
                        {'range': [66, 100], 'color': "#d1fae5"}
                    ],
                }
            ))
            fig_diversity.update_layout(height=300)
            st.plotly_chart(fig_diversity, use_container_width=True)
    
    with insight_col2:
        if not products_df.empty and 'brand_name' in products_df.columns:
            brand_concentration = (brand_counts.head(5).sum() / brand_counts.sum()) * 100
            fig_concentration = go.Figure(go.Indicator(
                mode="gauge+number",
                value=brand_concentration,
                title={'text': "Top 5 Brand Concentration (%)"},
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
            fig_concentration.update_layout(height=300)
            st.plotly_chart(fig_concentration, use_container_width=True)
    
    with insight_col3:
        if not ingredients_df.empty:
            coverage_score = (len(ingredients_df) / 5000) * 100  # Assumindo 5000 como meta
            fig_coverage = go.Figure(go.Indicator(
                mode="gauge+number",
                value=min(coverage_score, 100),
                title={'text': "Ingredient Coverage (%)"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#10b981"},
                    'steps': [
                        {'range': [0, 33], 'color': "#fee2e2"},
                        {'range': [33, 66], 'color': "#fef3c7"},
                        {'range': [66, 100], 'color': "#d1fae5"}
                    ],
                }
            ))
            fig_coverage.update_layout(height=300)
            st.plotly_chart(fig_coverage, use_container_width=True)

# Footer
st.divider()
st.markdown("### 🧭 Quick Navigation")
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("🧬 My Profile", use_container_width=True):
        st.switch_page("pages/1_Profile.py")

with col_nav2:
    if st.button("🧴 Browse Products", use_container_width=True):
        st.switch_page("pages/2_Products.py")

with col_nav3:
    if st.button("🔍 Analyze Ingredients", use_container_width=True):
        st.switch_page("pages/3_IngredientAnalysis.py")
