# Through the Label 🧴✨

A modern skincare analysis application that helps users make data-driven decisions about their skincare products.

## 🌟 Features

### 🧬 Personal Profile
- Create a detailed skin profile with your skin type, concerns, and preferences
- Set your budget and environmental factors
- Get personalized recommendations based on your profile
- **Visual gauges** showing sensitivity levels and budget allocation

### 🔍 Ingredient Analysis
- Paste any product's ingredient list (INCI format)
- Get detailed information about each ingredient
- Understand what ingredients do and who they're good for
- Discover products with similar ingredient profiles
- **Interactive charts** showing ingredient coverage and comparison tables
- **Similarity graphs** for product recommendations

### 🧴 Product Discovery
- Browse a curated database of skincare products
- Filter by product type, brand, or name
- View detailed product information
- Get match scores based on ingredient similarity
- **Bar charts and pie charts** for product type distribution
- **Treemap visualization** for brand and product hierarchy

### 📊 Dashboard & Analytics
- Comprehensive overview of the entire database
- **KPI metrics** for products, ingredients, brands, and categories
- **Interactive visualizations** including:
  - Product distribution charts
  - Top ingredients frequency analysis
  - Brand market share analysis
  - Database completeness indicators
  - Growth projections
- **Gauge charts** for diversity and concentration scores

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kaltrinasalihi/skincare-app.git
cd skincare-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run Frontpage.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 📁 Project Structure

```
skincare-app/
├── Frontpage.py              # Main landing page
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── src/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Centralized configuration and styling
│   └── utils/
│       ├── __init__.py       # Utils package initialization
│       ├── ingredient_utils.py # Ingredient analysis utilities
│       └── product_utils.py  # Product recommendation utilities
├── data/
│   ├── ingredients_dict.csv  # Ingredient database
│   └── products.csv          # Product catalog
├── pages/
    ├── 1_Profile.py          # User profile page
    ├── 2_Products.py         # Product browsing page
    ├── 3_IngredientAnalysis.py # Ingredient analysis page
    └── 4_Dashboard.py        # Analytics dashboard
```

## 🛠️ Technologies

- **Python 3.8+**
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations and charts
- **NumPy** - Numerical computations

## 👥 Team

- Luana Brugger
- Sara Penha
- Michele Natali
- Kaltrina Salihi

## 📝 How to Use

1. **Create Your Profile** - Start by setting up your skin profile with your type, concerns, and preferences
2. **Analyze Ingredients** - Paste ingredient lists from products you're interested in
3. **Discover Products** - Browse the catalog and find products that match your needs

## 🎨 Recent Improvements

- ✅ Centralized configuration for easier maintenance
- ✅ Responsive design with custom CSS
- ✅ Performance optimization with data caching
- ✅ Improved user interface and navigation
- ✅ Better error handling and user feedback
- ✅ Enhanced product filtering and search
- ✅ **Interactive visualizations with Plotly**
- ✅ **Comprehensive analytics dashboard**
- ✅ **Gauge charts for profile metrics**
- ✅ **Dynamic charts and graphs across all pages**
- ✅ **Data tables with comparison features**

## 📄 License

This project is part of an academic project.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ by the Through the Label team






