import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('steam_reviews_samples_500.db')
c = conn.cursor()


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


# Set the app title and layout
st.set_page_config(page_title="Steam Reviews Dashboard", layout="wide")
st.title("Steam Reviews Dashboard")

# Create sidebar navigation
nav = st.sidebar.radio("Navigation",
                       ["Story & Insights", "Question 1", "Question 2", "Question 3", "Question 4", "Question 5"])

if nav == "Story & Insights":
    st.header("Project Story and Key Insights")

    # Project Overview
    st.subheader("Project Overview")
    st.write(
        "This project analyzes 21 million Steam reviews to reveal the complex relationships between user satisfaction, game popularity, and consumer behavior.")

    # Key Findings
    st.subheader("Key Findings")

    # 1. Popularity ≠ Satisfaction
    st.markdown("### 1. Popularity ≠ Satisfaction")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - Popular games like PLAYERUNKNOWN'S BATTLEGROUNDS received mixed reviews (53.91% positive)
        - Niche games like ULTRAKILL achieved nearly 100% positive reviews but with lower exposure
        """)
    with col2:
        st.info("**Key Insight**: Popularity reflects broad exposure rather than quality or satisfaction")

    # 2. Addictive Games and Promising Markets
    st.markdown("### 2. Addictive Games & Promising Markets")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        - Games like Black Desert Online average 5.6 daily playing hours (2021)
        - Vietnam and Brazil show high engagement and user loyalty (94% recommendations in Brazil)
        """)
    with col4:
        st.info("**Key Insight**: Emerging markets show significant growth potential and high user engagement")

    # 3. Localization Challenges
    st.markdown("### 3. Localization & Cultural Adaptation Challenges")
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("""
        - China, Taiwan, and Japan: High playtime but lower recommendations (56%-70%)
        - Poland and Brazil: Successful cultural adaptation (94%-95% recommendations)
        """)
    with col6:
        st.info("**Key Insight**: Cultural adaptation significantly impacts user satisfaction")

    # Metrics Dashboard
    st.subheader("Key Metrics Overview")
    metric1, metric2, metric3 = st.columns(3)
    with metric1:
        st.metric(label="Total Reviews Analyzed", value="21M")
    with metric2:
        st.metric(label="Average Recommendation Rate", value="53.91%")
    with metric3:
        st.metric(label="Highest Daily Playtime", value="5.6 hrs")

if nav == "Question 1":
    st.header("Question 1: Analyzing Total and Positive Reviews")

    # Load the data for Q1.1, Q1.2, and Q1.3
    q1_1 = fetch_data("question1_1_samples_500")
    q1_2 = fetch_data("question1_2_samples_500")
    q1_3 = fetch_data("question1_3_samples_500")

    # Display the sample data for Q1.1
    st.subheader("Q1.1: Total Reviews per Game")
    st.write(q1_1.head(500))

    # Create a bar chart for Q1.1
    fig, ax = plt.subplots(figsize=(12, 6))
    q1_1.sort_values("total_reviews", ascending=False).head(10).plot(kind="bar", x="app_name", y="total_reviews", ax=ax)
    ax.set_title("Top 10 Games by Total Reviews")
    ax.set_xlabel("Game")
    ax.set_ylabel("Total Reviews")
    st.pyplot(fig)

    # Display the sample data for Q1.2
    st.subheader("Q1.2: Positive Reviews and Percentage")
    st.write(q1_2.head(500))

    # Create a scatter plot for Q1.2
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(q1_2["total_reviews"], q1_2["positive_percentage"])
    ax.set_title("Positive Review Percentage vs. Total Reviews")
    ax.set_xlabel("Total Reviews")
    ax.set_ylabel("Positive Review Percentage")
    st.pyplot(fig)

    # Display the sample data for Q1.3
    st.subheader("Q1.3: Games with Over 500,000 Reviews")
    st.write(q1_3.head(500))

    # Create a stacked bar chart for Q1.3
    fig, ax = plt.subplots(figsize=(12, 6))

    # Sort the data and select top 10
    q1_3_sorted = q1_3.sort_values("total_reviews", ascending=False).head(10)

    # Plot total reviews (base bar)
    ax.bar(
        q1_3_sorted["app_name"],
        q1_3_sorted["total_reviews"],
        color="#E8D362",
        label="Total Reviews"
    )

    # Overlay positive reviews (colored portion)
    ax.bar(
        q1_3_sorted["app_name"],
        q1_3_sorted["positive_reviews"],
        color="#1f77b4",  # Use any color you prefer
        label="Positive Reviews"
    )

    # Customize the plot
    ax.set_title("Top 10 Games with Over 500,000 Reviews")
    ax.set_xlabel("Game")
    ax.set_ylabel("Number of Reviews")
    ax.legend()
    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for readability

    st.pyplot(fig)

elif nav == "Question 2":
    st.header("Question 2: Finding Addictive Games")

    # Load the data for Q2.1, Q2.2, and Q2.3
    q2_1 = fetch_data("question2_1_samples_500")
    q2_2 = fetch_data("question2_2_samples_500")
    q2_3 = fetch_data("question2_3_samples_500")

    # Display the sample data for Q2.1
    st.subheader("Q2.1: Game with Highest Playtime Forever")
    st.write(q2_1.head(1))

    # Create a bar chart for Q2.2
    fig, ax = plt.subplots(figsize=(12, 6))
    q2_2.sort_values("total_playtime", ascending=False).head(10).plot(kind="bar", x="app_name", y="total_playtime",
                                                                      ax=ax)
    ax.set_title("Top 10 Games by Total Playtime")
    ax.set_xlabel("Game")
    ax.set_ylabel("Total Playtime (hours)")
    st.pyplot(fig)

    # Display the sample data for Q2.3
    st.subheader("Q2.3: Average Playtime per Day")
    st.write(q2_3.head(500))

    # Create a bar chart for Q2.3
    fig, ax = plt.subplots(figsize=(12, 6))
    q2_3.sort_values("average_playtime_per_day", ascending=False).head(10).plot(kind="bar", x="app_name",
                                                                                y="average_playtime_per_day", ax=ax)
    ax.set_title("Top 10 Games by Average Playtime per Day")
    ax.set_xlabel("Game")
    ax.set_ylabel("Average Playtime per Day (hours)")
    st.pyplot(fig)

elif nav == "Question 3":
    st.header("Question 3: Which Population Buys the Most Games?")

    # Load the data for Q3.1 and Q3.2
    q3_1 = fetch_data("question3_1_samples_500")
    q3_2 = fetch_data("question3_2_samples_500")

    # Display the sample data for Q3.1
    st.subheader("Q3.1: Reviews by Language")
    st.write(q3_1.head(500))

    # Create a bar chart for Q3.1
    fig, ax = plt.subplots(figsize=(12, 6))
    q3_1.sort_values("review_count", ascending=False).head(10).plot(kind="bar", x="language", y="review_count", ax=ax)
    ax.set_title("Top 10 Languages by Review Count")
    ax.set_xlabel("Language")
    ax.set_ylabel("Review Count (thousands)")
    st.pyplot(fig)

    # Display the sample data for Q3.2
    st.subheader("Q3.2: Users by Language who Purchased Games")
    st.write(q3_2.head(500))

    # Create a bar chart for Q3.2
    fig, ax = plt.subplots(figsize=(12, 6))
    q3_2.sort_values("total_users", ascending=False).head(10).plot(kind="bar", x="language", y="total_users", ax=ax)
    ax.set_title("Top 10 Languages by Purchasing Users")
    ax.set_xlabel("Language")
    ax.set_ylabel("Total Purchasing Users")
    st.pyplot(fig)

elif nav == "Question 4":
    st.header("Question 4: Top 10 Trending Games per Quarter")

    # Load the data for Q4
    q4 = fetch_data("question4_samples_500")

    # Convert quarter string to datetime
    q4['quarter'] = pd.to_datetime(q4['quarter'])

    # Display the sample data for Q4
    st.subheader("Q4: Top 10 Trending Games per Quarter")
    st.write(q4.head(10))

    # Get unique game names
    unique_games = q4['app_name'].unique().tolist()

    # Multiselect for games
    selected_games = st.multiselect(
        "Select Games to Visualize",
        options=unique_games,
        default=unique_games[:3]  # Default to first 3 games
    )

    # Filter and sort data for selected games
    filtered_q4 = q4[q4['app_name'].isin(selected_games)].sort_values('quarter')

    # Create the plot
    plt.figure(figsize=(15, 8))
    sns.set_style("whitegrid")
    sns.set_palette("husl")

    # Plot each selected game
    for game in selected_games:
        game_data = filtered_q4[filtered_q4['app_name'] == game]
        plt.plot(game_data['quarter'], game_data['review_count'],
                 marker='o', linewidth=2, markersize=8, label=game)

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

    plt.title('Trending Games per Quarter', fontsize=16)
    plt.xlabel('Quarter', fontsize=12)
    plt.ylabel('Review Count', fontsize=12)
    plt.legend(title='Games', title_fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Display the plot
    st.pyplot(plt)

    # Additional insights
    st.subheader("Insights")
    if not filtered_q4.empty:
        max_review_game = filtered_q4.loc[filtered_q4['review_count'].idxmax()]
        quarter = (max_review_game['quarter'].month - 1) // 3 + 1
        st.write(
            f"Highest reviewed game: {max_review_game['app_name']} with "
            f"{max_review_game['review_count']} reviews in "
            f"{max_review_game['quarter'].year}-Q{quarter}"
        )

    # Data table for selected games
    if selected_games:
        st.subheader("Selected Games Data")
        st.dataframe(filtered_q4)

elif nav == "Question 5":
    st.header("Question 5: User Demographics Analysis")

    # Load the data for Q5
    q5 = fetch_data("question5_samples_500")

    # Display the sample data for Q5
    st.subheader("Q5: User Demographics")
    st.write(q5.head(500))

    # Create a heatmap for Q5
    fig, ax = plt.subplots(figsize=(12, 6))
    # Use pivot_table with an aggregation function to handle duplicates
    pivot_table = q5.pivot_table(
        index="language",
        columns="user_type",
        values="unique_users",
        aggfunc="sum"  # Sum duplicates if they exist
    )
    sns.heatmap(pivot_table, annot=True, cmap="YlOrRd", ax=ax, fmt=".0f")
    ax.set_title("User Demographics by Language and User Type")
    ax.set_xlabel("User Type")
    ax.set_ylabel("Language")
    st.pyplot(fig)

    # Create a dropdown for Q5
    st.subheader("Explore User Demographics")

    # Dropdown to select a language
    selected_language = st.selectbox(
        "Select a Language",
        options=q5["language"].unique(),  # List of unique languages
        index=0  # Default to the first language in the list
    )

    # Filter data based on selected language
    selected_data = q5[q5["language"] == selected_language]

    # Plot the bar chart for the selected language
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(selected_data["user_type"], selected_data["unique_users"])
    ax.set_title(f"User Demographics for {selected_language}")
    ax.set_xlabel("User Type")
    ax.set_ylabel("Unique Users")
    st.pyplot(fig)