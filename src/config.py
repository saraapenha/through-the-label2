"""
Configurações centralizadas para o app Through the Label
"""

# Configurações de página
PAGE_CONFIG = {
    "page_title": "Through the Label",
    "page_icon": "🧴",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Paths de dados
DATA_PATHS = {
    "ingredients": "data/ingredients_dict.csv",
    "products": "data/products.csv"
}

# Opções de perfil
SKIN_TYPES = ["Oily", "Dry", "Combination", "Normal", "Sensitive"]

AGE_GROUPS = [
    "Teen (13-19 years)",
    "Young Adult (20-29 years)",
    "Adult (30-44 years)",
    "Mature (45+ years)"
]

SKIN_CONCERNS = [
    "Acne",
    "Redness",
    "Hyperpigmentation",
    "Wrinkles",
    "Oiliness",
    "Dehydration"
]

SENSITIVITY_LEVELS = ["Low", "Medium", "High"]

FRAGRANCE_PREFERENCES = [
    "No preference",
    "Fragrance-free",
    "Light fragrance OK"
]

CLIMATE_OPTIONS = ["Cold", "Moderate", "Hot"]

SUN_EXPOSURE_OPTIONS = ["Mostly indoors", "Mixed", "Mostly outdoors"]

# Configurações de orçamento
BUDGET_MIN = 5
BUDGET_MAX = 80
BUDGET_DEFAULT = 25

# CSS customizado para melhor aparência e responsividade
CUSTOM_CSS = """
<style>
    /* Remove padding extra do topo */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Melhora cards e containers */
    .stExpander {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.5rem;
    }
    
    /* Botões mais bonitos */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Melhora forms */
    .stTextArea textarea, .stTextInput input {
        border-radius: 8px;
    }
    
    /* Headers com melhor espaçamento */
    h1, h2, h3 {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Cards de features */
    .feature-card {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Responsividade para mobile */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        
        .stButton > button {
            height: 2.5rem;
            font-size: 0.9rem;
        }
    }
    
    /* Melhor visualização de JSON */
    .stJson {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
    }
</style>
"""
