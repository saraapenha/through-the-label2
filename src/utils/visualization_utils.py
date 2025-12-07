"""
Utilitários para criação de visualizações e gráficos
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


def create_skin_type_distribution(df: pd.DataFrame, column: str = 'skin_type') -> go.Figure:
    """Cria gráfico de distribuição de tipos de pele."""
    if df.empty or column not in df.columns:
        return None
    
    counts = df[column].value_counts()
    
    fig = px.pie(
        values=counts.values,
        names=counts.index,
        title="Distribuição de Tipos de Pele",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400, showlegend=True)
    
    return fig


def create_product_type_chart(df: pd.DataFrame) -> go.Figure:
    """Cria gráfico de barras para tipos de produtos."""
    if df.empty or 'product_type' not in df.columns:
        return None
    
    counts = df['product_type'].value_counts().head(10)
    
    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation='h',
        title="Top 10 Tipos de Produtos",
        labels={'x': 'Quantidade', 'y': 'Tipo de Produto'},
        color=counts.values,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=500, showlegend=False)
    
    return fig


def create_brand_distribution(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Cria gráfico de distribuição de marcas."""
    if df.empty or 'brand_name' not in df.columns:
        return None
    
    counts = df['brand_name'].value_counts().head(top_n)
    
    fig = px.bar(
        x=counts.index,
        y=counts.values,
        title=f"Top {top_n} Marcas",
        labels={'x': 'Marca', 'y': 'Número de Produtos'},
        color=counts.values,
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=500,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig


def create_ingredient_frequency_chart(ingredients_list: list, top_n: int = 20) -> go.Figure:
    """Cria gráfico de ingredientes mais comuns."""
    if not ingredients_list:
        return None
    
    # Flatten lista de ingredientes
    all_ingredients = []
    for ing_list in ingredients_list:
        if isinstance(ing_list, list):
            all_ingredients.extend(ing_list)
    
    if not all_ingredients:
        return None
    
    # Contar frequência
    ingredient_counts = pd.Series(all_ingredients).value_counts().head(top_n)
    
    fig = px.bar(
        x=ingredient_counts.values,
        y=ingredient_counts.index,
        orientation='h',
        title=f"Top {top_n} Ingredientes Mais Comuns",
        labels={'x': 'Frequência', 'y': 'Ingrediente'},
        color=ingredient_counts.values,
        color_continuous_scale='Teal'
    )
    
    fig.update_layout(height=600, showlegend=False)
    
    return fig


def create_concern_distribution(concerns_data: list) -> go.Figure:
    """Cria gráfico de preocupações de pele mais comuns."""
    if not concerns_data:
        return None
    
    # Flatten lista de concerns
    all_concerns = []
    for concern_list in concerns_data:
        if isinstance(concern_list, list):
            all_concerns.extend(concern_list)
        elif isinstance(concern_list, str):
            all_concerns.append(concern_list)
    
    if not all_concerns:
        return None
    
    concern_counts = pd.Series(all_concerns).value_counts()
    
    fig = px.bar(
        x=concern_counts.index,
        y=concern_counts.values,
        title="Preocupações de Pele Mais Comuns",
        labels={'x': 'Preocupação', 'y': 'Frequência'},
        color=concern_counts.values,
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(height=400, showlegend=False)
    
    return fig


def create_ingredient_category_pie(categories: dict) -> go.Figure:
    """Cria gráfico de pizza para categorias de ingredientes."""
    if not categories:
        return None
    
    fig = go.Figure(data=[go.Pie(
        labels=list(categories.keys()),
        values=list(categories.values()),
        hole=0.3
    )])
    
    fig.update_layout(
        title="Categorias de Ingredientes",
        height=400
    )
    
    return fig


def create_similarity_comparison(products_df: pd.DataFrame) -> go.Figure:
    """Cria gráfico de comparação de similaridade de produtos."""
    if products_df.empty or 'similarity' not in products_df.columns:
        return None
    
    fig = px.bar(
        products_df,
        x='product_name',
        y='similarity',
        title="Comparação de Similaridade de Produtos",
        labels={'product_name': 'Produto', 'similarity': 'Similaridade (%)'},
        color='similarity',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig


def create_price_distribution(df: pd.DataFrame, price_column: str = 'price') -> go.Figure:
    """Cria histograma de distribuição de preços."""
    if df.empty or price_column not in df.columns:
        return None
    
    # Remover valores nulos
    prices = df[price_column].dropna()
    
    if prices.empty:
        return None
    
    fig = px.histogram(
        prices,
        nbins=30,
        title="Distribuição de Preços",
        labels={'value': 'Preço (CHF)', 'count': 'Frequência'},
        color_discrete_sequence=['#3b82f6']
    )
    
    fig.update_layout(height=400, showlegend=False)
    
    return fig


def create_summary_metrics_table(data: dict) -> pd.DataFrame:
    """Cria tabela de métricas resumidas."""
    df = pd.DataFrame(list(data.items()), columns=['Métrica', 'Valor'])
    return df


def create_ingredient_comparison_table(ingredients: list, info_list: list) -> pd.DataFrame:
    """Cria tabela comparativa de ingredientes."""
    if not ingredients or not info_list:
        return pd.DataFrame()
    
    data = {
        'Ingrediente': [],
        'Categoria': [],
        'Benefício Principal': [],
        'Bom Para': []
    }
    
    for ing, info in zip(ingredients, info_list):
        if info:
            data['Ingrediente'].append(info.get('name', ing))
            data['Categoria'].append(info.get('what_is_it', 'N/A')[:50] + '...' if info.get('what_is_it') else 'N/A')
            data['Benefício Principal'].append(info.get('what_does_it_do', 'N/A')[:50] + '...' if info.get('what_does_it_do') else 'N/A')
            data['Bom Para'].append(info.get('who_is_it_good_for', 'N/A')[:50] + '...' if info.get('who_is_it_good_for') else 'N/A')
    
    return pd.DataFrame(data)


def create_gauge_chart(value: float, title: str, max_value: float = 100) -> go.Figure:
    """Cria gráfico de gauge (medidor)."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title},
        delta={'reference': max_value * 0.5},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "#3b82f6"},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "#fee2e2"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "#fef3c7"},
                {'range': [max_value * 0.66, max_value], 'color': "#d1fae5"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    return fig
