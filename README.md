# **Steam Reviews Analytics 🎮**

Steam Reviews Analytics is a comprehensive data analysis project that processes and visualizes 21 million Steam game reviews to uncover insights about user behavior, game popularity, and market trends. Built using Python with DuckDB for data processing, SQLite for storage, and Streamlit for interactive visualization, it provides deep insights into gaming communities and user preferences.

## **Table of Contents**
1. [General Functionality](#general-functionality)
2. [Screenshots](#screenshots)
3. [Technologies Used](#technologies-used)
4. [Setup and Installation](#setup-and-installation)
5. [Database Information](#database-information)
6. [Key Insights](#key-insights)
7. [Known Limitations](#known-limitations)
8. [Project Structure](#project-structure)

## **General Functionality**

This project analyzes massive Steam review datasets to reveal patterns in gaming behavior and market dynamics.

### **Data Processing**
* **High-Volume Processing**: Handles 21 million Steam reviews efficiently using DuckDB
* **Data Cleaning**: Processes raw CSV data, excluding review text to focus on metadata
* **Sampling**: Creates manageable 500-row samples for each analysis table
* **Multi-Database Support**: Exports processed data from DuckDB to SQLite for web applications

### **Analytics & Insights**
* **Game Popularity Analysis**: Total reviews, positive review percentages, and trending metrics
* **User Behavior Patterns**: Playtime analysis, addiction indicators, and engagement metrics
* **Market Demographics**: Language-based user analysis and purchasing behavior
* **Temporal Trends**: Quarter-by-quarter game popularity tracking
* **User Segmentation**: Demographics analysis by gaming habits and preferences

### **Interactive Visualization**
* **Web Dashboard**: Streamlit-based interface with multiple analysis sections
* **Graph Database Visualization**: Interactive network graphs showing user-game-review relationships
* **Dynamic Charts**: Bar charts, scatter plots, heatmaps, and time series visualizations
* **Filtering Capabilities**: Interactive dropdowns and multi-select options for data exploration

## **Screenshots**

### **1. Dashboard Overview**
*Main dashboard showing key metrics and navigation*

### **2. Game Popularity Analysis**
*Charts showing total reviews vs. positive review percentages*

### **3. Addictive Games Analysis**
*Visualization of games with highest playtime and daily engagement*

### **4. Demographics Heatmap**
*User demographics broken down by language and user type*

### **5. Interactive Graph Network**
*Network visualization of user-game-review relationships*

### **6. Trending Games Timeline**
*Time series analysis of game popularity by quarter*

## **Technologies Used**

### **Data Processing**
* Python 3.x
* DuckDB (High-performance analytics)
* SQLite (Web application storage)
* Pandas (Data manipulation)
* CSV Processing (21M+ records)

### **Visualization**
* Streamlit (Web dashboard)
* Matplotlib & Seaborn (Statistical plots)
* Plotly (Interactive charts)
* NetworkX (Graph analysis)
* Pyvis (Interactive network visualization)

### **Database**
* DuckDB (OLAP workloads)
* SQLite (OLTP operations)

## **Setup and Installation**

### **Prerequisites**
* Python 3.8+
* pip package manager
* 8GB+ RAM (for processing large datasets)
* Original `steam_reviews.csv` file (21M records)

### **1. Environment Setup**
```bash
pip install duckdb sqlite3 streamlit pandas matplotlib seaborn plotly networkx pyvis
```

### **2. Data Processing**
1. Place your `steam_reviews.csv` file in the project root
2. Run the data processing pipeline:
```bash
python db_queries.py
```
This will:
- Create `steam_reviews_db.duckdb` with analysis tables
- Generate `steam_reviews_samples_500.db` SQLite database
- Export 500-row samples for web visualization

### **3. Launch Visualizations**
**Main Dashboard:**
```bash
streamlit run visualise.py
```

**Graph Network Visualization:**
```bash
streamlit run steam_graph.py
```

Visit: `http://localhost:8501`

## **Database Information**

### **DuckDB Schema**
The main analytics database contains:
- `steam_reviews` - Full 21M record dataset
- `question1_1` through `question5` - Analysis result tables
- Sample tables with `_samples_500` suffix

### **SQLite Schema**
Web application database contains 500-row samples:
```sql
steam_reviews_sample_500
question1_1_samples_500  -- Total reviews per game
question1_2_samples_500  -- Positive review analysis
question1_3_samples_500  -- High-volume games (500k+ reviews)
question2_1_samples_500  -- Highest playtime records
question2_2_samples_500  -- Total playtime per game
question2_3_samples_500  -- Daily average playtime
question3_1_samples_500  -- Reviews by language
question3_2_samples_500  -- Purchasing users by language
question4_samples_500    -- Trending games by quarter
question5_samples_500    -- User demographics analysis
```

## **Key Insights**

### **Major Discoveries**
* **Popularity ≠ Quality**: Popular games like PUBG have mixed reviews (53.91% positive) while niche games achieve near-perfect ratings
* **Addiction Indicators**: Games like Black Desert Online average 5.6 hours of daily playtime
* **Market Opportunities**: Emerging markets (Vietnam, Brazil) show high engagement and 94%+ recommendation rates
* **Cultural Barriers**: East Asian markets show high playtime but lower satisfaction (56-70% recommendations)

### **Business Intelligence**
* **Localization Impact**: Cultural adaptation significantly affects user satisfaction
* **Engagement vs. Satisfaction**: High playtime doesn't guarantee positive reviews
* **Market Segmentation**: User behavior varies dramatically by language and region
* **Trend Analysis**: Quarterly patterns reveal seasonal gaming preferences

## **Known Limitations**

* **Sample Size**: Web visualizations use 500-row samples for performance
* **Memory Requirements**: Full dataset processing requires significant RAM
* **Review Text**: Excluded from analysis due to size and processing complexity
* **Real-time Updates**: Static dataset analysis, not live Steam data
* **Temporal Coverage**: Analysis limited to historical review data timeframe

## **Project Structure**

```
steam-reviews-analytics/
├── db_queries.py              # Main data processing pipeline
├── visualise.py               # Streamlit dashboard application
├── steam_graph.py             # Graph network visualization
├── steam_reviews.csv          # Source data (21M records)
├── steam_reviews_db.duckdb    # DuckDB analytics database
├── steam_reviews_samples_500.db # SQLite web application database
├── steam_reviews_sample.csv   # 500-row sample export
├── graph.html                 # Generated network visualization
└── README.md                  # This file
```

### **Analysis Modules**
```
Question 1: Game Popularity & Review Analysis
Question 2: Gaming Addiction & Engagement Patterns  
Question 3: Market Demographics & Purchase Behavior
Question 4: Trending Games & Temporal Analysis
Question 5: User Segmentation & Demographics
```