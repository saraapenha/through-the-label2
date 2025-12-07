import pandas as pd
import ast
import streamlit as st


@st.cache_data(ttl=3600)
def load_products(path: str = "data/products.csv"):
    """Carrega dados de produtos com cache para melhor performance."""
    try:
        df = pd.read_csv(path)
        
        # Process ingredient column if it exists
        if 'clean_ingreds' in df.columns:
            df["clean_ingreds"] = df["clean_ingreds"].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else []
            )
            df["clean_ingreds"] = df["clean_ingreds"].apply(
                lambda lst: [ing.strip().lower() for ing in lst] if isinstance(lst, list) else []
            )
        
        return df
    except FileNotFoundError:
        st.error(f"Product database not found at {path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading product data: {e}")
        return pd.DataFrame()


def recommend_products(ingredient_list: list, top_k: int = 3) -> pd.DataFrame:
    """Recomenda produtos baseado em similaridade de ingredientes (Jaccard)."""
    if not ingredient_list:
        return pd.DataFrame()
    
    # Load products (with cache)
    df = load_products()
    
    if df.empty or 'clean_ingreds' not in df.columns:
        return pd.DataFrame()
    
    # Normalize input ingredients
    user_set = set([i.strip().lower() for i in ingredient_list if i and i.strip()])
    
    if not user_set:
        return pd.DataFrame()
    
    # Calculate Jaccard similarity
    scores = []
    for _, row in df.iterrows():
        prod_set = set(row["clean_ingreds"]) if row["clean_ingreds"] else set()
        
        if not prod_set:
            scores.append(0.0)
        else:
            intersection = len(user_set & prod_set)
            union = len(user_set | prod_set)
            similarity = intersection / union if union > 0 else 0.0
            scores.append(similarity)
    
    # Add scores to dataframe
    df_copy = df.copy()
    df_copy["similarity"] = scores
    
    # Sort and return top K
    recommendations = df_copy.sort_values(
        by="similarity", 
        ascending=False
    ).head(top_k)
    
    return recommendations
