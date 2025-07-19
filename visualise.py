import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np

# Connect to SQLite database
conn = sqlite3.connect('steam_reviews_samples_500.db')
c = conn.cursor()

# Professional color palette
PRIMARY_DARK = '#1a1d23'
SECONDARY_DARK = '#2d3748'
ACCENT_BLUE = '#3182ce'
SUCCESS_GREEN = '#38a169'
WARNING_ORANGE = '#ed8936'
LIGHT_TEXT = '#e2e8f0'
MUTED_TEXT = '#a0aec0'
CARD_BG = '#2d3748'
BORDER_COLOR = '#4a5568'

# Configure Streamlit theme and styling
st.set_page_config(
    page_title="Steam Reviews Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Main app background */
    .main {
        background: linear-gradient(135deg, #1a1d23 0%, #2d3748 100%);
        color: #e2e8f0;
    }

    .stApp {
        background: linear-gradient(135deg, #1a1d23 0%, #2d3748 100%);
    }

    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, #2d3748 0%, #1a1d23 100%);
        border-right: 1px solid #4a5568;
    }

    /* Card-like containers for metrics */
    .stMetric {
        background: linear-gradient(145deg, #2d3748, #1a1d23);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #4a5568;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.4);
    }

    /* Headers with professional styling */
    h1 {
        color: #3182ce !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #3182ce;
        padding-bottom: 0.5rem;
        margin-bottom: 2rem !important;
    }

    h2, h3 {
        color: #63b3ed !important;
        font-weight: 500 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    /* Text styling */
    p, div, span, li, td, th {
        color: #e2e8f0 !important;
        line-height: 1.6;
    }

    /* Navigation styling */
    .stRadio > label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }

    .stRadio > div {
        background: rgba(45, 55, 72, 0.6);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4a5568;
    }

    /* Select boxes and inputs */
    .stSelectbox, .stMultiSelect {
        background: #2d3748;
        border-radius: 8px;
        border: 1px solid #4a5568;
    }

    /* Data tables */
    .stDataFrame {
        background: #2d3748;
        border-radius: 8px;
        border: 1px solid #4a5568;
        overflow: hidden;
    }

    /* Info boxes */
    .stInfo {
        background: rgba(49, 130, 206, 0.15);
        border: 1px solid #3182ce;
        border-radius: 8px;
        color: #e2e8f0 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(145deg, #3182ce, #2c5282);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(49, 130, 206, 0.3);
    }

    /* Metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #2d3748, #1a1d23);
        border: 1px solid #4a5568;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    [data-testid="metric-container"] > div {
        color: #e2e8f0 !important;
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #3182ce !important;
        font-weight: 700;
    }

    /* Container spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Professional spacing */
    .element-container {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def fetch_data(table_name):
    """
    Fetch data from the specified SQLite table.

    Parameters:
    table_name (str): The name of the SQLite table to fetch data from.

    Returns:
    pandas.DataFrame: The data from the specified table.
    """
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, conn)


# Set professional matplotlib theme
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = PRIMARY_DARK
plt.rcParams['axes.facecolor'] = SECONDARY_DARK
plt.rcParams['axes.edgecolor'] = BORDER_COLOR
plt.rcParams['text.color'] = LIGHT_TEXT
plt.rcParams['axes.labelcolor'] = LIGHT_TEXT
plt.rcParams['xtick.color'] = LIGHT_TEXT
plt.rcParams['ytick.color'] = LIGHT_TEXT
plt.rcParams['grid.color'] = BORDER_COLOR
plt.rcParams['grid.alpha'] = 0.3

# App title with professional styling
st.title("🎮 Steam Reviews Dashboard")
st.markdown("### 📊 *Analyzing 21 Million Gaming Reviews*")

# Create sidebar navigation
nav = st.sidebar.radio(
    "📊 Navigation",
    ["📖 Story & Insights", "📈 Review Analytics", "🎯 Gaming Addiction", "🌍 Global Markets", "📅 Trending Analysis",
     "👥 User Demographics"]
)

if nav == "📖 Story & Insights":
    st.header("🎮 Project Story and Key Insights")

    # Project Overview
    st.subheader("📋 Project Overview")
    st.write(
        "This project analyzes 21 million Steam reviews to reveal the complex relationships between user satisfaction, game popularity, and consumer behavior.")

    # Key Findings
    st.subheader("🔥 Key Findings")

    # 1. Popularity ≠ Satisfaction
    st.markdown("### 🏆 1. Popularity ≠ Satisfaction")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        🎯 Popular games like PLAYERUNKNOWN'S BATTLEGROUNDS received mixed reviews (53.91% positive)

        💎 Niche games like ULTRAKILL achieved nearly 100% positive reviews but with lower exposure
        """)
    with col2:
        st.info("**🧠 Key Insight**: Popularity reflects broad exposure rather than quality or satisfaction")

    # 2. Addictive Games and Promising Markets
    st.markdown("### ⚡ 2. Addictive Games & Promising Markets")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        🕐 Games like Black Desert Online average 5.6 daily playing hours (2021)

        🌏 Vietnam and Brazil show high engagement and user loyalty (94% recommendations in Brazil)
        """)
    with col4:
        st.info("**📈 Key Insight**: Emerging markets show significant growth potential and high user engagement")

    # 3. Localization Challenges
    st.markdown("### 🗺️ 3. Localization & Cultural Adaptation Challenges")
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("""
        🏮 China, Taiwan, and Japan: High playtime but lower recommendations (56%-70%)

        🎊 Poland and Brazil: Successful cultural adaptation (94%-95% recommendations)
        """)
    with col6:
        st.info("**🎯 Key Insight**: Cultural adaptation significantly impacts user satisfaction")

    # Metrics Dashboard
    st.subheader("📊 Key Metrics Overview")
    metric1, metric2, metric3 = st.columns(3)
    with metric1:
        st.metric(label="🎮 Total Reviews Analyzed", value="21M")
    with metric2:
        st.metric(label="👍 Average Recommendation Rate", value="53.91%")
    with metric3:
        st.metric(label="⏰ Highest Daily Playtime", value="5.6 hrs")

if nav == "📈 Review Analytics":
    st.header("📈 Review Analytics: Popularity vs Quality Analysis")

    # Load the data for Q1.1, Q1.2, and Q1.3
    q1_1 = fetch_data("question1_1_samples_500")
    q1_2 = fetch_data("question1_2_samples_500")
    q1_3 = fetch_data("question1_3_samples_500")

    # Display the sample data for Q1.1
    st.subheader("📊 Q1.1: Total Reviews per Game")
    st.write(q1_1.head(500))

    # Create a bar chart for Q1.1
    fig, ax = plt.subplots(figsize=(12, 6))
    q1_1.sort_values("total_reviews", ascending=False).head(10).plot(
        kind="bar", x="app_name", y="total_reviews", ax=ax, color=ACCENT_BLUE
    )
    ax.set_title("🏆 Top 10 Games by Total Reviews", fontsize=16, color=ACCENT_BLUE)
    ax.set_xlabel("🎮 Game", fontsize=12)
    ax.set_ylabel("📝 Total Reviews", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Display the sample data for Q1.2
    st.subheader("💯 Q1.2: Positive Reviews and Percentage")
    st.write(q1_2.head(500))

    # Create a scatter plot for Q1.2
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(q1_2["total_reviews"], q1_2["positive_percentage"],
               color=SUCCESS_GREEN, alpha=0.7, s=50)
    ax.set_title("👍 Positive Review Percentage vs. Total Reviews", fontsize=16, color=ACCENT_BLUE)
    ax.set_xlabel("📊 Total Reviews", fontsize=12)
    ax.set_ylabel("💚 Positive Review Percentage", fontsize=12)
    st.pyplot(fig)

    # Display the sample data for Q1.3
    st.subheader("🔥 Q1.3: Games with Over 500,000 Reviews")
    st.write(q1_3.head(500))

    # Create a stacked bar chart for Q1.3
    fig, ax = plt.subplots(figsize=(12, 6))

    # Sort the data and select top 10
    q1_3_sorted = q1_3.sort_values("total_reviews", ascending=False).head(10)

    # Plot total reviews (base bar)
    ax.bar(
        q1_3_sorted["app_name"],
        q1_3_sorted["total_reviews"],
        color=WARNING_ORANGE,
        label="📊 Total Reviews"
    )

    # Overlay positive reviews (colored portion)
    ax.bar(
        q1_3_sorted["app_name"],
        q1_3_sorted["positive_reviews"],
        color=SUCCESS_GREEN,
        label="👍 Positive Reviews"
    )

    # Customize the plot
    ax.set_title("🚀 Top 10 Games with Over 500,000 Reviews", fontsize=16, color=ACCENT_BLUE)
    ax.set_xlabel("🎮 Game", fontsize=12)
    ax.set_ylabel("📈 Number of Reviews", fontsize=12)
    ax.legend()
    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig)

elif nav == "🎯 Gaming Addiction":
    st.header("🎯 Gaming Addiction: Identifying Most Engaging Games")

    # Load the data for Q2.1, Q2.2, and Q2.3
    q2_1 = fetch_data("question2_1_samples_500")
    q2_2 = fetch_data("question2_2_samples_500")
    q2_3 = fetch_data("question2_3_samples_500")

    # Display the sample data for Q2.1
    st.subheader("👑 Q2.1: Game with Highest Playtime Forever")
    st.write(q2_1.head(1))

    # Create a bar chart for Q2.2
    fig, ax = plt.subplots(figsize=(12, 6))
    q2_2.sort_values("total_playtime", ascending=False).head(10).plot(
        kind="bar", x="app_name", y="total_playtime", ax=ax, color=ACCENT_BLUE
    )
    ax.set_title("⏰ Top 10 Games by Total Playtime", fontsize=16, color=ACCENT_BLUE)
    ax.set_xlabel("🎮 Game", fontsize=12)
    ax.set_ylabel("⏱️ Total Playtime (hours)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Display the sample data for Q2.3
    st.subheader("📅 Q2.3: Average Playtime per Day")
    st.write(q2_3.head(500))

    # Create a bar chart for Q2.3
    fig, ax = plt.subplots(figsize=(12, 6))
    q2_3.sort_values("average_playtime_per_day", ascending=False).head(10).plot(
        kind="bar", x="app_name", y="average_playtime_per_day", ax=ax, color=SUCCESS_GREEN
    )
    ax.set_title("🔥 Top 10 Games by Average Playtime per Day", fontsize=16, color=ACCENT_BLUE)
    ax.set_xlabel("🎮 Game", fontsize=12)
    ax.set_ylabel("📈 Average Playtime per Day (hours)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

elif nav == "🌍 Global Markets":
    st.header("🌍 Global Markets: Worldwide Gaming Demographics")

    # Load the data for Q3.1 and Q3.2
    q3_1 = fetch_data("question3_1_samples_500")
    q3_2 = fetch_data("question3_2_samples_500")

    # Display the sample data for Q3.1
    st.subheader("🗣️ Q3.1: Reviews by Language")
    st.write(q3_1.head(500))

    # Create a bar chart for Q3.1
    fig, ax = plt.subplots(figsize=(12, 6))
    q3_1.sort_values("review_count", ascending=False).head(10).plot(
        kind="bar", x="language", y="review_count", ax=ax, color=ACCENT_BLUE
    )
    ax.set_title("🌐 Top 10 Languages by Review Count", fontsize=16, color=ACCENT_BLUE)
    ax.set_xlabel("🗣️ Language", fontsize=12)
    ax.set_ylabel("📊 Review Count (thousands)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    # Display the sample data for Q3.2
    st.subheader("💰 Q3.2: Users by Language who Purchased Games")
    st.write(q3_2.head(500))

    # Create a bar chart for Q3.2
    fig, ax = plt.subplots(figsize=(12, 6))
    q3_2.sort_values("total_users", ascending=False).head(10).plot(
        kind="bar", x="language", y="total_users", ax=ax, color=SUCCESS_GREEN
    )
    ax.set_title("🛒 Top 10 Languages by Purchasing Users", fontsize=16, color=ACCENT_BLUE)
    ax.set_xlabel("🌍 Language", fontsize=12)
    ax.set_ylabel("👥 Total Purchasing Users", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

elif nav == "📅 Trending Analysis":
    st.header("📅 Trending Analysis: Game Popularity Over Time")

    # Load the data for Q4
    q4 = fetch_data("question4_samples_500")

    # Convert quarter string to datetime
    q4['quarter'] = pd.to_datetime(q4['quarter'])

    # Display the sample data for Q4
    st.subheader("📈 Q4: Top 10 Trending Games per Quarter")
    st.write(q4.head(10))

    # Get unique game names
    unique_games = q4['app_name'].unique().tolist()

    # Multiselect for games
    selected_games = st.multiselect(
        "🎮 Select Games to Visualize",
        options=unique_games,
        default=unique_games[:3]  # Default to first 3 games
    )

    # Filter and sort data for selected games
    filtered_q4 = q4[q4['app_name'].isin(selected_games)].sort_values('quarter')

    # Create the plot
    plt.figure(figsize=(15, 8))

    # Professional color palette for games
    colors = [ACCENT_BLUE, SUCCESS_GREEN, WARNING_ORANGE, '#ff6b9d', '#c44569', '#f8b500']

    # Plot each selected game
    for i, game in enumerate(selected_games):
        game_data = filtered_q4[filtered_q4['app_name'] == game]
        plt.plot(game_data['quarter'], game_data['review_count'],
                 marker='o', linewidth=3, markersize=8,
                 label=game, color=colors[i % len(colors)])

    # Format x-axis dates
    ax = plt.gca()

    # Use MonthLocator for quarterly ticks
    ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=3))


    # Custom formatter for quarter display
    def quarter_formatter(x, pos=None):
        date = plt.matplotlib.dates.num2date(x)
        quarter = (date.month - 1) // 3 + 1
        return f"{date.year}-Q{quarter}"


    ax.xaxis.set_major_formatter(plt.FuncFormatter(quarter_formatter))
    plt.xticks(rotation=45, ha='right', fontsize=10)

    plt.title('🚀 Trending Games per Quarter', fontsize=16, color=ACCENT_BLUE)
    plt.xlabel('📅 Quarter', fontsize=12)
    plt.ylabel('📊 Review Count', fontsize=12)
    plt.legend(title='🎮 Games', title_fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Display the plot
    st.pyplot(plt)

    # Additional insights
    st.subheader("🔍 Insights")
    if not filtered_q4.empty:
        max_review_game = filtered_q4.loc[filtered_q4['review_count'].idxmax()]
        quarter = (max_review_game['quarter'].month - 1) // 3 + 1
        st.write(
            f"🏆 Highest reviewed game: {max_review_game['app_name']} with "
            f"{max_review_game['review_count']} reviews in "
            f"{max_review_game['quarter'].year}-Q{quarter}"
        )

    # Data table for selected games
    if selected_games:
        st.subheader("📋 Selected Games Data")
        st.dataframe(filtered_q4)

elif nav == "👥 User Demographics":
    st.header("👥 User Demographics: Player Behavior Analysis")

    # Load the data for Q5
    q5 = fetch_data("question5_samples_500")

    # Display the sample data for Q5
    st.subheader("📊 Q5: User Demographics")
    st.write(q5.head(500))

    # Create a heatmap for Q5 with improved colors for magnitude distinction
    fig, ax = plt.subplots(figsize=(12, 6))
    # Use pivot_table with an aggregation function to handle duplicates
    pivot_table = q5.pivot_table(
        index="language",
        columns="user_type",
        values="unique_users",
        aggfunc="sum"  # Sum duplicates if they exist
    )

    # Create a custom colormap that emphasizes orders of magnitude
    # Apply log transformation to better show magnitude differences
    pivot_log = np.log2(pivot_table + 1)  # Add 1 to avoid log(0)

    # Create custom discrete color levels based on powers of 2
    from matplotlib.colors import ListedColormap
    import matplotlib.colors as mcolors

    # Define color levels for different magnitudes (powers of 2)
    colors_list = [
        '#0f1419',  # Very low (near 0)
        '#1a2332',  # Low (2-8)
        '#2d4a5c',  # Medium-low (16-64)
        '#3d6b7d',  # Medium (128-512)
        '#4d8ca0',  # Medium-high (1024-4096)
        '#63b3d1',  # High (8192-32768)
        '#8cc9e8',  # Very high (65536+)
        '#b3ddf5'  # Extreme high
    ]

    # Create custom colormap
    custom_cmap = ListedColormap(colors_list)

    # Create heatmap with log-scaled colors
    sns.heatmap(pivot_table,
                annot=True,
                cmap=custom_cmap,
                ax=ax,
                fmt=".0f",
                cbar_kws={'label': '👥 Users (Log Scale)'},
                norm=mcolors.LogNorm(vmin=pivot_table.min().min(), vmax=pivot_table.max().max()))

    ax.set_title("🌍 User Demographics by Language and User Type", fontsize=16, color=ACCENT_BLUE)
    ax.set_xlabel("🎮 User Type", fontsize=12)
    ax.set_ylabel("🗣️ Language", fontsize=12)
    st.pyplot(fig)

    # Create a dropdown for Q5
    st.subheader("🔍 Explore User Demographics")

    # Dropdown to select a language
    selected_language = st.selectbox(
        "🌐 Select a Language",
        options=q5["language"].unique(),  # List of unique languages
        index=0  # Default to the first language in the list
    )

    # Filter data based on selected language
    selected_data = q5[q5["language"] == selected_language]

    # Plot the bar chart for the selected language
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(selected_data["user_type"], selected_data["unique_users"],
                  color=[ACCENT_BLUE, SUCCESS_GREEN, WARNING_ORANGE][:len(selected_data)])
    ax.set_title(f"👥 User Demographics for {selected_language}", fontsize=16, color=ACCENT_BLUE)
    ax.set_xlabel("🎮 User Type", fontsize=12)
    ax.set_ylabel("👤 Unique Users", fontsize=12)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')

    st.pyplot(fig)