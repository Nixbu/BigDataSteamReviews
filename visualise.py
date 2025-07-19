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
st.set_page_config(page_title="Steam Reviews Dashboard", layout="wide", initial_sidebar_state="expanded")

# Compact CSS styling
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #1a1d23 0%, #2d3748 100%); color: #e2e8f0; }
    .stApp { background: linear-gradient(135deg, #1a1d23 0%, #2d3748 100%); }
    .stSidebar { background: linear-gradient(180deg, #2d3748 0%, #1a1d23 100%); border-right: 1px solid #4a5568; }
    .stMetric { background: linear-gradient(145deg, #2d3748, #1a1d23); padding: 1rem; border-radius: 8px; border: 1px solid #4a5568; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); }
    .stMetric:hover { transform: translateY(-1px); box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); }
    h1 { color: #3182ce !important; font-weight: 600 !important; border-bottom: 2px solid #3182ce; padding-bottom: 0.3rem; margin-bottom: 1rem !important; }
    h2, h3 { color: #63b3ed !important; font-weight: 500 !important; margin-top: 1rem !important; margin-bottom: 0.5rem !important; }
    p, div, span, li, td, th { color: #e2e8f0 !important; line-height: 1.4; }
    .stRadio > label { color: #e2e8f0 !important; font-weight: 500; }
    .stRadio > div { background: rgba(45, 55, 72, 0.6); padding: 0.75rem; border-radius: 6px; border: 1px solid #4a5568; }
    .stSelectbox, .stMultiSelect { background: #2d3748; border-radius: 6px; border: 1px solid #4a5568; }
    .stDataFrame { background: #2d3748; border-radius: 6px; border: 1px solid #4a5568; overflow: hidden; }
    .stInfo { background: rgba(49, 130, 206, 0.15); border: 1px solid #3182ce; border-radius: 6px; color: #e2e8f0 !important; }
    .stButton > button { background: linear-gradient(145deg, #3182ce, #2c5282); color: white; border: none; border-radius: 6px; padding: 0.5rem 1rem; font-weight: 500; }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 2px 6px rgba(49, 130, 206, 0.3); }
    [data-testid="metric-container"] { background: linear-gradient(145deg, #2d3748, #1a1d23); border: 1px solid #4a5568; border-radius: 8px; padding: 1rem; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); }
    [data-testid="metric-container"] > div { color: #e2e8f0 !important; }
    [data-testid="metric-container"] [data-testid="metric-value"] { color: #3182ce !important; font-weight: 700; font-size: 1.5rem !important; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }
    .element-container { margin-bottom: 0.5rem; }
    .stMarkdown { margin-bottom: 0.5rem !important; }
    .row-widget { margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)


def fetch_data(table_name):
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

# App title
st.title("🎮 Steam Reviews Dashboard")
st.markdown("### 📊 *Analyzing 21 Million Gaming Reviews*")

# Create sidebar navigation
nav = st.sidebar.radio("📊 Navigation",
                       ["📖 Story & Insights", "📈 Review Analytics", "🎯 Gaming Addiction", "🌍 Global Markets",
                        "📅 Trending Analysis", "👥 User Demographics"])

if nav == "📖 Story & Insights":
    col1, col2 = st.columns([3, 2])

    with col1:
        st.header("🎮 Project Story and Key Insights")
        st.markdown("**📋 Project Overview**")
        st.write(
            "This project analyzes 21 million Steam reviews to reveal the complex relationships between user satisfaction, game popularity, and consumer behavior.")

        st.markdown("**🔥 Key Findings**")

        st.markdown("**🏆 1. Popularity ≠ Satisfaction**")
        st.markdown(
            "🎯 Popular games like PLAYERUNKNOWN'S BATTLEGROUNDS received mixed reviews (53.91% positive). 💎 Niche games like ULTRAKILL achieved nearly 100% positive reviews but with lower exposure")

        st.markdown("**⚡ 2. Addictive Games & Promising Markets**")
        st.markdown(
            "🕐 Games like Black Desert Online average 5.6 daily playing hours (2021). 🌏 Vietnam and Brazil show high engagement and user loyalty (94% recommendations in Brazil)")

        st.markdown("**🗺️ 3. Localization & Cultural Adaptation Challenges**")
        st.markdown(
            "🏮 China, Taiwan, and Japan: High playtime but lower recommendations (56%-70%). 🎊 Poland and Brazil: Successful cultural adaptation (94%-95% recommendations)")

    with col2:
        st.info("**🧠 Key Insight**: Popularity reflects broad exposure rather than quality or satisfaction")
        st.info("**📈 Key Insight**: Emerging markets show significant growth potential and high user engagement")
        st.info("**🎯 Key Insight**: Cultural adaptation significantly impacts user satisfaction")

        st.markdown("**📊 Key Metrics Overview**")
        metric1, metric2, metric3 = st.columns(3)
        with metric1: st.metric("🎮 Total Reviews", "21M")
        with metric2: st.metric("👍 Avg Recommendation", "53.91%")
        with metric3: st.metric("⏰ Max Daily Playtime", "5.6 hrs")

elif nav == "📈 Review Analytics":
    st.header("📈 Review Analytics")

    q1_1 = fetch_data("question1_1_samples_500")
    q1_2 = fetch_data("question1_2_samples_500")
    q1_3 = fetch_data("question1_3_samples_500")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📊 Q1.1: Total Reviews per Game**")
        st.dataframe(q1_1.head(10), height=200)

        fig, ax = plt.subplots(figsize=(8, 4))
        q1_1.sort_values("total_reviews", ascending=False).head(8).plot(kind="bar", x="app_name", y="total_reviews",
                                                                        ax=ax, color=ACCENT_BLUE)
        ax.set_title("🏆 Top 8 Games by Reviews", fontsize=14, color=ACCENT_BLUE)
        ax.set_xlabel("🎮 Game", fontsize=10)
        ax.set_ylabel("📝 Reviews", fontsize=10)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.markdown("**💯 Q1.2: Positive Reviews and Percentage**")
        st.dataframe(q1_2.head(10), height=200)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.scatter(q1_2["total_reviews"], q1_2["positive_percentage"], color=SUCCESS_GREEN, alpha=0.7, s=30)
        ax.set_title("👍 Positive % vs. Total Reviews", fontsize=14, color=ACCENT_BLUE)
        ax.set_xlabel("📊 Total Reviews", fontsize=10)
        ax.set_ylabel("💚 Positive %", fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)

    st.markdown("**🔥 Q1.3: Games with Over 500,000 Reviews**")
    col3, col4 = st.columns([1, 2])
    with col3:
        st.dataframe(q1_3.head(10), height=300)
    with col4:
        fig, ax = plt.subplots(figsize=(10, 5))
        q1_3_sorted = q1_3.sort_values("total_reviews", ascending=False).head(8)
        ax.bar(q1_3_sorted["app_name"], q1_3_sorted["total_reviews"], color=WARNING_ORANGE, label="📊 Total Reviews")
        ax.bar(q1_3_sorted["app_name"], q1_3_sorted["positive_reviews"], color=SUCCESS_GREEN,
               label="👍 Positive Reviews")
        ax.set_title("🚀 Top 8 Games with Over 500,000 Reviews", fontsize=14, color=ACCENT_BLUE)
        ax.set_xlabel("🎮 Game", fontsize=10)
        ax.set_ylabel("📈 Reviews", fontsize=10)
        ax.legend()
        plt.xticks(rotation=45, ha="right", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

elif nav == "🎯 Gaming Addiction":
    st.header("🎯 Gaming Addiction")

    q2_1 = fetch_data("question2_1_samples_500")
    q2_2 = fetch_data("question2_2_samples_500")
    q2_3 = fetch_data("question2_3_samples_500")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("**👑 Q2.1: Highest Playtime Forever**")
        st.dataframe(q2_1.head(1))

        st.markdown("**📅 Q2.3: Average Playtime per Day**")
        st.dataframe(q2_3.head(15), height=300)

    with col2:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        q2_2.sort_values("total_playtime", ascending=False).head(8).plot(kind="bar", x="app_name", y="total_playtime",
                                                                         ax=ax1, color=ACCENT_BLUE)
        ax1.set_title("⏰ Top 8 Games by Total Playtime", fontsize=14, color=ACCENT_BLUE)
        ax1.set_xlabel("🎮 Game", fontsize=10)
        ax1.set_ylabel("⏱️ Total Playtime (hours)", fontsize=10)
        ax1.tick_params(axis='x', rotation=45, labelsize=8)

        q2_3.sort_values("average_playtime_per_day", ascending=False).head(8).plot(kind="bar", x="app_name",
                                                                                   y="average_playtime_per_day", ax=ax2,
                                                                                   color=SUCCESS_GREEN)
        ax2.set_title("🔥 Top 8 Games by Avg Playtime/Day", fontsize=14, color=ACCENT_BLUE)
        ax2.set_xlabel("🎮 Game", fontsize=10)
        ax2.set_ylabel("📈 Avg Playtime/Day (hours)", fontsize=10)
        ax2.tick_params(axis='x', rotation=45, labelsize=8)

        plt.tight_layout()
        st.pyplot(fig)

elif nav == "🌍 Global Markets":
    st.header("🌍 Global Markets")

    q3_1 = fetch_data("question3_1_samples_500")
    q3_2 = fetch_data("question3_2_samples_500")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🗣️ Q3.1: Reviews by Language**")
        st.dataframe(q3_1.head(15), height=300)

        fig, ax = plt.subplots(figsize=(8, 5))
        q3_1.sort_values("review_count", ascending=False).head(8).plot(kind="bar", x="language", y="review_count",
                                                                       ax=ax, color=ACCENT_BLUE)
        ax.set_title("🌐 Top 8 Languages by Reviews", fontsize=12, color=ACCENT_BLUE)
        ax.set_xlabel("🗣️ Language", fontsize=10)
        ax.set_ylabel("📊 Reviews (k)", fontsize=10)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.markdown("**💰 Q3.2: Purchasing Users by Language**")
        st.dataframe(q3_2.head(15), height=300)

        fig, ax = plt.subplots(figsize=(8, 5))
        q3_2.sort_values("total_users", ascending=False).head(8).plot(kind="bar", x="language", y="total_users", ax=ax,
                                                                      color=SUCCESS_GREEN)
        ax.set_title("🛒 Top 8 Languages by Purchasing Users", fontsize=12, color=ACCENT_BLUE)
        ax.set_xlabel("🌍 Language", fontsize=10)
        ax.set_ylabel("👥 Total Users", fontsize=10)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

elif nav == "📅 Trending Analysis":
    st.header("📅 Trending Analysis")

    q4 = fetch_data("question4_samples_500")
    q4['quarter'] = pd.to_datetime(q4['quarter'])

    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown("**📈 Q4: Top Trending Games**")
        st.dataframe(q4.head(20), height=400)

        unique_games = q4['app_name'].unique().tolist()
        selected_games = st.multiselect("🎮 Select Games", options=unique_games, default=unique_games[:3])

    with col2:
        if selected_games:
            filtered_q4 = q4[q4['app_name'].isin(selected_games)].sort_values('quarter')

            fig, ax = plt.subplots(figsize=(12, 6))
            colors = [ACCENT_BLUE, SUCCESS_GREEN, WARNING_ORANGE, '#ff6b9d', '#c44569', '#f8b500']

            for i, game in enumerate(selected_games):
                game_data = filtered_q4[filtered_q4['app_name'] == game]
                ax.plot(game_data['quarter'], game_data['review_count'], marker='o', linewidth=3, markersize=6,
                        label=game, color=colors[i % len(colors)])

            ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=3))


            def quarter_formatter(x, pos=None):
                date = plt.matplotlib.dates.num2date(x)
                quarter = (date.month - 1) // 3 + 1
                return f"{date.year}-Q{quarter}"


            ax.xaxis.set_major_formatter(plt.FuncFormatter(quarter_formatter))

            plt.xticks(rotation=45, ha='right', fontsize=9)
            plt.title('🚀 Trending Games per Quarter', fontsize=14, color=ACCENT_BLUE)
            plt.xlabel('📅 Quarter', fontsize=10)
            plt.ylabel('📊 Review Count', fontsize=10)
            plt.legend(title='🎮 Games', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
            plt.tight_layout()
            st.pyplot(fig)

elif nav == "👥 User Demographics":
    st.header("👥 User Demographics")

    q5 = fetch_data("question5_samples_500")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("**📊 Q5: User Demographics**")
        st.dataframe(q5.head(20), height=400)

        selected_language = st.selectbox("🌐 Select Language", options=q5["language"].unique(), index=0)

    with col2:
        # Heatmap
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        pivot_table = q5.pivot_table(index="language", columns="user_type", values="unique_users", aggfunc="sum")
        from matplotlib.colors import ListedColormap
        import matplotlib.colors as mcolors

        colors_list = ['#0f1419', '#1a2332', '#2d4a5c', '#3d6b7d', '#4d8ca0', '#63b3d1', '#8cc9e8', '#b3ddf5']
        custom_cmap = ListedColormap(colors_list)

        sns.heatmap(pivot_table, annot=True, cmap=custom_cmap, ax=ax1, fmt=".0f", cbar_kws={'label': '👥 Users'},
                    norm=mcolors.LogNorm(vmin=pivot_table.min().min(), vmax=pivot_table.max().max()))
        ax1.set_title("🌍 User Demographics Heatmap", fontsize=12, color=ACCENT_BLUE)
        ax1.set_xlabel("🎮 User Type", fontsize=10)
        ax1.set_ylabel("🗣️ Language", fontsize=10)

        # Bar chart for selected language
        selected_data = q5[q5["language"] == selected_language]
        bars = ax2.bar(selected_data["user_type"], selected_data["unique_users"],
                       color=[ACCENT_BLUE, SUCCESS_GREEN, WARNING_ORANGE][:len(selected_data)])
        ax2.set_title(f"👥 {selected_language} Demographics", fontsize=12, color=ACCENT_BLUE)
        ax2.set_xlabel("🎮 User Type", fontsize=10)
        ax2.set_ylabel("👤 Unique Users", fontsize=10)

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom',
                     fontweight='bold', fontsize=9)

        plt.tight_layout()
        st.pyplot(fig)