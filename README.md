# Through the Label 🧴✨

A modern skincare analysis application that helps users make data-driven decisions about their skincare products.
Built as part of the *Fundamentals and Methods of Computer Science for Business Studies* course.

---

## 🌟 Main Features

### 🧬 Personal Profile

* Create a skin profile with:

  * skin type
  * age group
  * main concerns
  * sensitivity level
  * fragrance preference
  * budget
  * climate
  * sun exposure
* Profile data is stored securely in the Streamlit session state.
* The app provides simple product suggestions aligned with the user’s profile.
* Gauge charts help visualize sensitivity and budget positioning.

---

### 🔍 Ingredient Analysis

* Paste an INCI ingredient list directly into the app.
* The app parses and compares the list to the ingredient database.
* For each recognized ingredient, the app displays:

  * what it is
  * what it does
  * who it is good for
  * who should avoid it
  * an external link for further reading
* Unknown ingredients are clearly highlighted.
* Coverage charts summarize how many ingredients were recognized.
* Ingredient-based similarity is used to recommend matching products.

---

### 🧴 Product Discovery

* Browse a curated skincare product catalog.
* Filter by:

  * product type
  * brand
  * keyword search
* View product fields (name, type, brand, URL, ingredient list).
* Interactive charts show:

  * product type distribution
  * brand distribution
  * combined category breakdowns

---

### 📊 Dashboard & Analytics

* Overview metrics:

  * total products
  * total ingredients
  * number of brands
  * number of categories
* Interactive visualizations:

  * sunburst charts
  * bar charts
  * ingredient frequency analysis

---

## 🧠 Recommendation Algorithm (Machine Learning Component)

The application includes a content-based recommendation engine using a Jaccard-style similarity score.

**How it works:**

* Each product contains a cleaned list of ingredients.
* The user input list is parsed and normalized.
* Similarity is computed as:

similarity = |intersection| / |union|

* Products with highest similarity scores are recommended.

This satisfies the machine learning requirement for the course project.

---

## 🎯 Alignment With Course Project Requirements

1. **Clearly defined problem**
   Consumers struggle to understand skincare ingredient lists.

2. **Use of data from API/database**
   The app loads structured CSV datasets:
   `ingredients_dict.csv` and `products.csv`.

3. **Meaningful data visualizations**
   Used across all pages (Plotly): coverage, brand/type distribution, dashboards, gauges.

4. **User interaction**
   Includes profile form, ingredient input, search and filter controls, interactive charts.

5. **Machine learning**
   Similarity-based recommendation algorithm.

6. **Documented, well-structured code**
   Organized into `src/`, `utils/`, `pages/`, with readable logic.

7. **Contribution matrix**
   Submitted separately.

8. **4-minute video presentation**
   Demonstrates full app workflow.

---

## 🚀 How to Run the App

### 1. Clone the repository

git clone [https://github.com/saraapenha/through-the-label2.git](https://github.com/saraapenha/through-the-label2.git)
cd through-the-label2

### 2. (Optional) Create a virtual environment

python3 -m venv venv
source venv/bin/activate     *(Windows: venv\Scripts\activate)*

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the application

streamlit run Frontpage.py

The app will open at **[http://localhost:8501](http://localhost:8501)**

---

## 🧩 Screenshots

*(Optional — recommended to add later)*

Examples to include:

* Profile page
* Ingredient Analysis
* Recommendations
* Dashboard

---

## 🐍 Requirements

* **Python 3.9+ recommended**
* Main libraries:

  * Streamlit
  * Pandas
  * NumPy
  * Plotly

---

## 🛠️ Troubleshooting

**Streamlit not found:**
pip install streamlit

**ModuleNotFoundError:**
pip install -r requirements.txt

**App not launching:**
cd through-the-label2
streamlit run Frontpage.py

---

## 📄 License

This is an academic project for educational purposes.

---

## 👩‍💻 Team

GitHub Profiles:

* [https://github.com/saraapenha](https://github.com/saraapenha)

(Add additional team members if desired)

---

Made with ❤️ by the Through the Label Team
