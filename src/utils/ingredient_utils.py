import pandas as pd
import re
import streamlit as st


@st.cache_data(ttl=3600)
def load_ingredient_data(path: str = "data/ingredients_dict.csv"):
    """Carrega dados de ingredientes com cache para melhor performance."""
    try:
        df = pd.read_csv(path)
        # Normalize column names
        df.columns = [col.lower() for col in df.columns]
        # Create normalized search column
        df["name_clean"] = df["name"].str.strip().str.lower()
        return df
    except FileNotFoundError:
        st.error(f"Ingredient database not found at {path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading ingredient data: {e}")
        return pd.DataFrame()


def parse_ingredient_list(text: str) -> list:
    """Parse uma lista de ingredientes separada por vírgulas ou ponto-e-vírgula."""
    if not text or not isinstance(text, str):
        return []
    
    # Split by comma or semicolon
    parts = re.split(r",|;", text)
    
    # Clean and normalize
    ingredients = []
    for p in parts:
        cleaned = p.strip().lower()
        if cleaned:  # Ignore empty strings
            ingredients.append(cleaned)
    
    return ingredients


def get_ingredient_info(name: str) -> dict:
    """Busca informações sobre um ingrediente específico."""
    if not name or not isinstance(name, str):
        return None
    
    # Load data (with cache)
    df = load_ingredient_data()
    
    if df.empty:
        return None
    
    name_clean = name.strip().lower()
    
    # Exact match
    match = df[df["name_clean"] == name_clean]
    
    # If not found, partial match
    if match.empty:
        mask = df["name_clean"].str.contains(name_clean, na=False, regex=False)
        match = df[mask]
    
    # If still not found, try common ingredient fallbacks
    if match.empty:
        fallback_info = get_common_ingredient_fallback(name_clean)
        if fallback_info:
            return fallback_info
        return None
    
    # Get first match
    row = match.iloc[0]
    
    return {
        "name": row.get("name", name.title()),
        "short_description": row.get("short_description", ""),
        "what_is_it": row.get("what_is_it", ""),
        "what_does_it_do": row.get("what_does_it_do", ""),
        "who_is_it_good_for": row.get("who_is_it_good_for", ""),
        "who_should_avoid": row.get("who_should_avoid", ""),
        "url": row.get("url", "")
    }


def get_common_ingredient_fallback(name_clean: str) -> dict:
    """Retorna informações básicas para ingredientes comuns não encontrados no banco."""
    
    # Dicionário de ingredientes comuns com informações básicas
    common_ingredients = {
        "aqua": {
            "name": "Aqua (Water)",
            "short_description": "Water is the most common cosmetic ingredient and serves as a solvent.",
            "what_is_it": "Water (Aqua) is the universal solvent used in skincare formulations.",
            "what_does_it_do": "Acts as a base for most skincare products, helps dissolve other ingredients, and provides hydration to the skin.",
            "who_is_it_good_for": "All skin types",
            "who_should_avoid": "Generally safe for everyone",
            "url": ""
        },
        "water": {
            "name": "Water (Aqua)",
            "short_description": "Water is the most common cosmetic ingredient and serves as a solvent.",
            "what_is_it": "Water (Aqua) is the universal solvent used in skincare formulations.",
            "what_does_it_do": "Acts as a base for most skincare products, helps dissolve other ingredients, and provides hydration to the skin.",
            "who_is_it_good_for": "All skin types",
            "who_should_avoid": "Generally safe for everyone",
            "url": ""
        },
        "glycerin": {
            "name": "Glycerin",
            "short_description": "A powerful humectant that draws moisture into the skin.",
            "what_is_it": "Glycerin (also called glycerol) is a natural compound derived from vegetable oils or animal fats. It's a humectant, meaning it attracts water.",
            "what_does_it_do": "Attracts and retains moisture in the skin, helps strengthen the skin barrier, provides hydration, and makes skin feel soft and smooth.",
            "who_is_it_good_for": "All skin types, especially dry and dehydrated skin",
            "who_should_avoid": "Generally safe, but in very dry climates without proper occlusive, it may draw moisture from deeper skin layers",
            "url": ""
        },
        "glycerol": {
            "name": "Glycerol (Glycerin)",
            "short_description": "A powerful humectant that draws moisture into the skin.",
            "what_is_it": "Glycerol (also called glycerin) is a natural compound derived from vegetable oils or animal fats. It's a humectant, meaning it attracts water.",
            "what_does_it_do": "Attracts and retains moisture in the skin, helps strengthen the skin barrier, provides hydration, and makes skin feel soft and smooth.",
            "who_is_it_good_for": "All skin types, especially dry and dehydrated skin",
            "who_should_avoid": "Generally safe for all skin types",
            "url": ""
        },
        "niacinamide": {
            "name": "Niacinamide",
            "short_description": "A form of Vitamin B3 that brightens, reduces pores, and strengthens the skin barrier.",
            "what_is_it": "Niacinamide (Vitamin B3) is a water-soluble vitamin that offers multiple benefits for the skin.",
            "what_does_it_do": "Reduces the appearance of pores, regulates oil production, brightens skin tone, reduces hyperpigmentation, strengthens the skin barrier, and has anti-inflammatory properties.",
            "who_is_it_good_for": "All skin types, especially oily, acne-prone, aging, and hyperpigmented skin",
            "who_should_avoid": "Generally safe for all skin types, though some may experience sensitivity at high concentrations",
            "url": ""
        },
        "hyaluronic acid": {
            "name": "Hyaluronic Acid",
            "short_description": "A powerful humectant that can hold up to 1000x its weight in water.",
            "what_is_it": "Hyaluronic acid is a naturally occurring substance in the skin that helps retain moisture and keep skin plump and hydrated.",
            "what_does_it_do": "Provides intense hydration, plumps the skin, reduces the appearance of fine lines and wrinkles, and helps maintain skin elasticity.",
            "who_is_it_good_for": "All skin types, especially dry, dehydrated, and aging skin",
            "who_should_avoid": "Generally safe for all skin types. In very dry climates, use with an occlusive to prevent moisture loss",
            "url": ""
        },
        "tocopherol": {
            "name": "Tocopherol (Vitamin E)",
            "short_description": "A fat-soluble antioxidant that protects skin from environmental damage.",
            "what_is_it": "Tocopherol is the most common form of Vitamin E, a powerful antioxidant naturally found in the skin.",
            "what_does_it_do": "Protects against free radical damage, helps moisturize and heal the skin, reduces inflammation, and can help fade scars and hyperpigmentation.",
            "who_is_it_good_for": "All skin types, especially dry and mature skin",
            "who_should_avoid": "Those with very oily or acne-prone skin may want to use lower concentrations as it can be comedogenic in high amounts",
            "url": ""
        },
        "cetearyl alcohol": {
            "name": "Cetearyl Alcohol",
            "short_description": "A fatty alcohol that acts as an emollient and emulsifier.",
            "what_is_it": "Cetearyl alcohol is a fatty alcohol derived from natural sources like coconut or palm oil. Unlike drying alcohols, it's actually beneficial for skin.",
            "what_does_it_do": "Softens and smooths the skin, helps stabilize formulations, provides texture and consistency to products, and acts as a moisturizing agent.",
            "who_is_it_good_for": "All skin types, especially dry skin",
            "who_should_avoid": "Generally safe, though rarely may cause sensitivity in some individuals",
            "url": ""
        },
        "parfum": {
            "name": "Parfum (Fragrance)",
            "short_description": "Added to products for scent, can be synthetic or natural.",
            "what_is_it": "Parfum or fragrance is a blend of aromatic compounds added to cosmetic products to provide a pleasant smell.",
            "what_does_it_do": "Provides scent to the product. Does not offer skincare benefits but enhances the sensory experience of using the product.",
            "who_is_it_good_for": "Those who enjoy fragranced products and don't have sensitive skin",
            "who_should_avoid": "People with sensitive skin, eczema, rosacea, or fragrance allergies should avoid fragranced products",
            "url": ""
        },
        "fragrance": {
            "name": "Fragrance (Parfum)",
            "short_description": "Added to products for scent, can be synthetic or natural.",
            "what_is_it": "Fragrance or parfum is a blend of aromatic compounds added to cosmetic products to provide a pleasant smell.",
            "what_does_it_do": "Provides scent to the product. Does not offer skincare benefits but enhances the sensory experience of using the product.",
            "who_is_it_good_for": "Those who enjoy fragranced products and don't have sensitive skin",
            "who_should_avoid": "People with sensitive skin, eczema, rosacea, or fragrance allergies should avoid fragranced products",
            "url": ""
        }
    }
    
    return common_ingredients.get(name_clean)
