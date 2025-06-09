📚 **Personal Reading Analytics Dashboard**
A full-stack data science project analyzing 10 years of personal reading data from Goodreads. As an avid reader, I’ve noticed my reading habits decline year-over-year, so I decided to let the data speak for itself and uncover trends, preferences, and insights into my own reading journey.

🔗 **Live Demo:** [View the deployed dashboard](https://croweigibson-goodreads-reading-project-app-veaciy.streamlit.app/)

---

## 🎯 Project Highlights

This project demonstrates end-to-end data science skills by building a complete pipeline from web scraping to insights generation. I analyzed 616 books spanning a decade (March 2015 – April 2025) to uncover personal reading patterns and trends.

**Key Achievements**

* 🕷️ **Web Scraping**: Automated data collection from personal Goodreads profile using BeautifulSoup (`main.py`).
* 🧹 **Data Engineering**: Comprehensive cleaning and transformation pipeline in `books_EDA.ipynb`, including mapping ratings, parsing dates, and standardizing text.
* 📊 **Exploratory Data Analysis**: Statistical analysis revealing reading behavior insights across genres, authors, and time.
* 🎨 **Data Visualization**: Created interactive charts and dashboards using Streamlit (`app.py`), matplotlib, and seaborn.

---

## 🛠 Technical Skills Demonstrated

| Category        | Technologies                                      |
| --------------- | ------------------------------------------------- |
| Web Scraping    | Python, Requests, BeautifulSoup, HTML parsing     |
| Data Processing | Pandas, NumPy, Data cleaning, ETL pipelines       |
| Analysis        | Statistical analysis, Trend analysis, Correlation |
| Visualization   | Streamlit, Matplotlib, Seaborn                    |
| Tools           | Jupyter Notebooks, Git, CSV handling              |

---

## 📊 Project Results & Insights

**Dataset Overview**

* **616 books** analyzed from **March 2015 – April 2025**
* **8 key features**: Title, Author, Personal Rating, Community Rating, Genre, Page Count, Date Added, URL

**Key Findings**

* 📈 **Seasonal Reading Patterns**: Identified peaks in summer and winter months.
* ⭐ **Rating Analysis**: Compared personal ratings with community averages to spot rating biases.
* 📚 **Genre Preferences**: Fantasy dominates, but insights reveal growth in variety over time.
* 📖 **Length vs. Rating**: Moderate-length books (200–400 pages) tend to receive higher personal ratings.
* 👨‍💼 **Author Insights**: Top-read authors and correlation between repeat reads and ratings.

---

## 🔧 Technical Implementation

1. **Data Collection Pipeline** (`main.py`)

   * Multi-page scraping with pagination until no more books.
   * Rate limiting (`time.sleep` with random intervals) to respect server resources.
   * Robust error handling for missing or malformed entries.

2. **Data Cleaning & EDA** (`books_EDA.ipynb`)

   * Renamed and standardized columns.
   * Mapped textual ratings (e.g., "it was amazing") to numeric scale (1–5).
   * Parsed dates, extracted year/month, and handled missing values.
   * Standardized author names and genre labels.

3. **Interactive Dashboard** (`app.py`)

   * Streamlit app with sidebar filters for time period and genre.
   * KPI cards for total books, pages, 5★ count, and below-3★ count.
   * On-demand insights: top/least read genres, highest/lowest rated books, author and page-length metrics.
   * Visualizations: rating distributions, books per year (with average line), and rating vs. page-count bins.

---

---

## 💡 Business Value & Applications

This methodology can be applied to:

* **E-commerce**: Customer purchase pattern analysis.
* **Content Platforms**: User engagement tracking and recommendations.
* **Market Research**: Consumer preference and trend analysis.
* **Product Analytics**: Usage pattern identification.

---

## 🎓 Learning Outcomes

* **Data Pipeline Architecture**: Built scalable ETL processes.
* **API & Scraping Management**: Handled rate limits and errors.
* **Statistical Analysis**: Extracted actionable insights.
* **Data Storytelling**: Presented findings via interactive dashboards.
* **Code Quality**: Maintained modular, documented code.

---

## 🔍 Code Quality Features

* ✅ **Error Handling**: Comprehensive exception management.
* ✅ **Documentation**: Clear comments and docstrings.
* ✅ **Modularity**: Reusable functions and clean structure.
* ✅ **Best Practices**: PEP 8 compliance.
* ✅ **Version Control**: Organized Git commits and branching.

---

## 📈 Future Enhancements

* **Machine Learning**: Recommendation engine for next reads.
* **Sentiment Analysis**: Analyze review text sentiment.
* **Real-time Updates**: Automated daily/weekly data refresh.
* **Comparative Analysis**: Multi-user or community-wide trends.
* **Automated Profile Sync**: Implement a service to detect changes in your Goodreads profile and automatically re-scrape and update the dashboard.
* **Scraping Optimization**: Parallelize and cache requests, tune delays, and use async requests to significantly speed up data collection.
* **Genre Extraction Improvement**: Research alternative methods (e.g., headless browser scraping, robust HTML parsing, or reliable API integrations) to fetch genres more accurately and consistently.
* **Filter & Visualization Enhancements**: Convert month filters from numeric (1–12) to names (Jan–Dec) and implement dynamic aggregation—when filtering by month, switch the “Books Read Per Year” chart to “Books Read By Month” for clearer insights.

---

## 🏆 Project Impact

This project showcases my ability to:

* Transform raw web data into meaningful insights.
* Build end-to-end data science workflows from scratch.
* Communicate complex findings through visualization.
* Deliver production-ready, maintainable code for data projects.
