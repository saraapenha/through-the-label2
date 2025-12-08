# Through the Label 🧴✨

A modern skincare analysis application that helps users make data-driven decisions about their skincare products.  
Built as part of the *Fundamentals and Methods of Computer Science for Business Studies* course.

---

## 🌟 Main Features

### 🧬 Personal Profile
- Create a skin profile with:
  - skin type  
  - age group  
  - main concerns  
  - sensitivity level  
  - fragrance preference  
  - budget  
  - climate  
  - sun exposure  
- Profile data is stored securely in the Streamlit session state.
- The app provides simple product suggestions aligned with the user's budget and preferences.
- Gauge charts help visualize sensitivity and budget positioning.

---

### 🔍 Ingredient Analysis
- Paste an INCI ingredient list directly into the app.
- The app parses and compares the list to our ingredient database.
- For each recognized ingredient, the app displays:
  - what it is  
  - what it does  
  - who it is good for  
  - who should avoid it  
  - external sources for additional information  
- Unknown ingredients are clearly highlighted.
- Coverage charts summarize how many ingredients were successfully recognized.
- Ingredient-based similarity is used to recommend matching products.

---

### 🧴 Product Discovery
- Browse a curated skincare product catalog.
- Filter by:
  - product type  
  - brand  
  - keyword search  
- View essential product fields (name, type, brand, URL, ingredient list).
- Interactive Plotly visualizations display:
  - product type distribution  
  - brand distribution  
  - combined category breakdowns  

---

### 📊 Dashboard & Analytics
- Overview metrics:
  - total products  
  - total ingredients  
  - number of brands  
  - number of categories  
- Data visualized via interactive charts:
  - sunburst brand/category breakdown  
  - bar charts of product counts  
  - ingredient frequency charts  
- Supports a deeper understanding of the dataset.

---

## 🧠 Recommendation Algorithm (Machine Learning Component)

The application includes a **content-based recommendation engine**.

### How it works:
- Each product in the catalog includes a cleaned list of ingredients.
- The user inputs their own list of ingredients.
- Similarity is calculated using a Jaccard-style metric:

\[
similarity = \frac{|intersection|}{|union|}
\]

- Products with the highest similarity scores are recommended to the user.

This satisfies the project requirement for a machine learning or data-driven algorithm.

---

## 🎯 Alignment With Course Project Requirements

1. **Clearly defined problem**  
   Consumers struggle to understand ingredient lists, leading to poor skincare decisions.

2. **Use of data from an API or database**  
   The app loads two structured datasets:  
   `ingredients_dict.csv` and `products.csv`.

3. **Visualizations that serve the use case**  
   Plotly charts included across the app:
   - ingredient coverage  
   - product distributions  
   - dashboard analytics  
   - gauge charts  

4. **User interaction**  
   Users can:
   - create a skin profile  
   - paste ingredient lists  
   - filter product lists  
   - explore interactive charts  

5. **Machine learning implementation**  
   Jaccard similarity–based recommendation engine for matching products to user ingredient lists.

6. **Well-documented, well-structured code**  
   Organized into modules (`src/`, `utils/`, `pages/`) with clear separation of concerns and readable logic.

7. **Contribution matrix**  
   Delivered separately as part of the final submission.

8. **4-minute demonstration video**  
   Prepared to showcase the full app, features, and development process.

---

## 🚀 How to Run the App

### 1. Clone the repository

```bash
git clone https://github.com/saraapenha/through-the-label2.git
cd through-the-label2
2. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Run the application
streamlit run Frontpage.py
The app will open automatically at:
http://localhost:8501
🧩 Screenshots
(Optional — recommended to add later)
You may include images such as:

Profile page
Ingredient Analysis results
Recommendations
Dashboard visualizations
🐍 Requirements
Python 3.9+ recommended
Main libraries:
Streamlit
Pandas
NumPy
Plotly
🛠️ Troubleshooting
❗ Streamlit not found
pip install streamlit
❗ ModuleNotFoundError
Make sure dependencies are installed:
pip install -r requirements.txt
❗ App not launching
Ensure you are inside the project folder:
cd through-the-label2
streamlit run Frontpage.py
📄 License
This is an academic project created for educational purposes.
👩‍💻 Team
GitHub Profiles:
https://github.com/saraapenha
(Add your teammates' profiles here if desired)
Made with ❤️ by the Through the Label Team
