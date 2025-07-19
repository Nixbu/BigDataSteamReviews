import duckdb
import sqlite3

# ========================================== DUCKDB SETUP =============================================

#  Create or connect to the DuckDB database file
conn = duckdb.connect('steam_reviews_db.duckdb')

# Import the CSV into a new table in the database, excluding the 'review' column
# conn.execute("""
#     CREATE TABLE steam_reviews AS
#     SELECT app_id, app_name, review_id, language, timestamp_created, timestamp_updated,
#            recommended, votes_helpful, votes_funny, weighted_vote_score, comment_count,
#            steam_purchase, received_for_free, written_during_early_access, "author.steamid",
#            "author.num_games_owned", "author.num_reviews", "author.playtime_forever",
#            "author.playtime_last_two_weeks", "author.playtime_at_review", "author.last_played"
#     FROM read_csv_auto('steam_reviews.csv', max_line_size=100000000)
# """)

conn.execute("""
    COPY (
        SELECT *
        FROM steam_reviews
        ORDER BY RANDOM()
        LIMIT 500
        
    ) TO 'steam_reviews_sample.csv' (HEADER, DELIMITER ',');
""")

conn.execute(
    """
    CREATE OR REPLACE TABLE steam_reviews_sample_500 AS
    SELECT * FROM read_csv_auto('steam_reviews_sample.csv')
    """
)

# ========================================== QUESTION TABLES ==========================================

print("""======================================= Question 1 =================================================""")
# Analyzing the total reviews, positive reviews, and positive review percentage on each game

# Q1.1: Total reviews per game
conn.execute("""
    CREATE TABLE IF NOT EXISTS question1_1 AS
    SELECT
        app_name,
        COUNT(*) as total_reviews
    FROM steam_reviews
    GROUP BY app_name;
""")
results = conn.execute("SELECT * FROM question1_1 ORDER BY total_reviews DESC;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)

# Q1.2: Positive reviews and percentage
conn.execute("""
    CREATE TABLE IF NOT EXISTS question1_2 AS
    SELECT
        app_name,
        COUNT(*) as total_reviews,
        SUM(CASE WHEN recommended THEN 1 ELSE 0 END) as positive_reviews,
        ROUND(SUM(CASE WHEN recommended THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as positive_percentage
    FROM steam_reviews
    GROUP BY app_name;
""")
results = conn.execute("SELECT * FROM question1_2 ORDER BY positive_percentage DESC;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)

# Q1.3: Games with over 500,000 reviews
conn.execute("""
    CREATE TABLE IF NOT EXISTS question1_3 AS
    SELECT
        app_name,
        COUNT(*) as total_reviews,
        SUM(CASE WHEN recommended THEN 1 ELSE 0 END) as positive_reviews,
        ROUND(SUM(CASE WHEN recommended THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as positive_percentage
    FROM steam_reviews
    GROUP BY app_name
    HAVING COUNT(*) > 500000;
""")
results = conn.execute("SELECT * FROM question1_3 ORDER BY total_reviews DESC;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)


print("""======================================= Question 2 =================================================""")
# Finding out which games are addicting

# Q2.1: Game with the highest playtime_forever
conn.execute("""
    CREATE TABLE IF NOT EXISTS question2_1 AS
    SELECT app_name, "author.playtime_forever"
    FROM steam_reviews
    ORDER BY "author.playtime_forever" DESC
    LIMIT 1;
""")
results = conn.execute("SELECT * FROM question2_1;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)

# Q2.2: Total playtime per game
conn.execute("""
    CREATE TABLE IF NOT EXISTS question2_2 AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY SUM("author.playtime_forever") / 60.0 DESC) AS row_num,
        app_name,
        SUM("author.playtime_forever") / 60.0 AS total_playtime
    FROM steam_reviews
    GROUP BY app_name;
""")
results = conn.execute("SELECT * FROM question2_2 ORDER BY total_playtime DESC;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)

# Q2.3: Average playtime per day
conn.execute("""
    CREATE TABLE IF NOT EXISTS question2_3 AS
    WITH playtime_two_weeks AS (
        SELECT 
            app_name, 
            SUM("author.playtime_last_two_weeks") / 60.0 AS total_playtime_last_two_weeks,
            COUNT(DISTINCT "author.steamid") AS users_per_app
        FROM steam_reviews
        WHERE "author.playtime_last_two_weeks" > 0
        GROUP BY app_name
    )
    SELECT 
        app_name,
        (total_playtime_last_two_weeks * 1.0 / users_per_app) / 14.0 AS average_playtime_per_day
    FROM playtime_two_weeks
    WHERE (total_playtime_last_two_weeks * 1.0 / users_per_app) / 14.0 >= 2.5;
""")
results = conn.execute("SELECT * FROM question2_3 ORDER BY average_playtime_per_day DESC;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)

print("""======================================= Question 3 =================================================""")
# Which population buys the most games?

# Q3.1: Reviews by language
conn.execute("""
    CREATE TABLE IF NOT EXISTS question3_1 AS
    SELECT 
        language,
        COUNT(*) / 1000 as review_count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
    FROM steam_reviews
    GROUP BY language;
""")
results = conn.execute("SELECT * FROM question3_1 ORDER BY review_count DESC;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)

# Q3.2: Users by language who purchased games
conn.execute("""
    CREATE TABLE IF NOT EXISTS question3_2 AS
    SELECT 
        language,
        COUNT(DISTINCT "author.steamid") AS total_users, 
        ROUND(
            COUNT(DISTINCT "author.steamid") * 100.0 / 
            SUM(COUNT(DISTINCT "author.steamid")) OVER(), 
            2
        ) AS percentage
    FROM steam_reviews
    WHERE 
        steam_purchase = TRUE 
        AND received_for_free = FALSE
    GROUP BY language;
""")
results = conn.execute("SELECT * FROM question3_2 ORDER BY total_users DESC;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)

print("""======================================= Question 4 =================================================""")
# Top 10 trending games for each quarter

conn.execute("""
    CREATE TABLE IF NOT EXISTS question4 AS
    WITH monthly_reviews AS (
        SELECT
            app_name,
            DATE_TRUNC('quarter', TIMESTAMP 'epoch' + timestamp_created * INTERVAL '1 second') AS quarter,
            COUNT(*) AS review_count
        FROM steam_reviews
        GROUP BY app_name, quarter
    ),
    top_games_by_quarter AS (
        SELECT
            quarter,
            app_name,
            review_count,
            RANK() OVER (PARTITION BY quarter ORDER BY review_count DESC) AS rank_
        FROM monthly_reviews
    )
    SELECT
        app_name,
        quarter,
        review_count
    FROM top_games_by_quarter
    WHERE rank_ <= 10;
""")
results = conn.execute("SELECT * FROM question4 ORDER BY quarter, review_count DESC;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)

print("""======================================= Question 5 =================================================""")
# User demographics analysis

conn.execute("""
    CREATE TABLE IF NOT EXISTS question5 AS
    SELECT 
        COALESCE(user_type, 'All Users') AS user_type,
        COALESCE(language, 'All Languages') AS language,
        COUNT(DISTINCT "author.steamid") AS unique_users,
        AVG("author.num_games_owned") AS avg_games_owned,
        AVG("author.playtime_forever") AS avg_playtime,
        AVG(CASE WHEN recommended THEN 1.0 ELSE 0.0 END) AS recommendation_rate
    FROM (
        SELECT 
            CASE 
                WHEN "author.num_games_owned" < 3 THEN 'Light Multi-Game'
                WHEN "author.num_games_owned" < 10 THEN 'Casual Multi-Game'
                WHEN "author.num_games_owned" BETWEEN 10 AND 200 THEN 'Hardcore Multi-Game'
            END AS user_type,
            language,
            "author.steamid",
            "author.num_games_owned",
            "author.playtime_forever",
            recommended
        FROM steam_reviews
    ) 
    GROUP BY CUBE(user_type, language);
""")
results = conn.execute("SELECT * FROM question5 ORDER BY language, avg_games_owned, user_type;").fetchall()
print("==================================================================================\nSample Data:")
for result in results:
    print(result)

# ========================================== QUESTION SAMPLE TABLES ==========================================
# Loop to create a randomized sample table for each question table
question_tables = [
    "question1_1", "question1_2", "question1_3",
    "question2_1", "question2_2", "question2_3",
    "question3_1", "question3_2",
    "question4", "question5"
]

for table in question_tables:
    sample_table_name = f"{table}_samples_500"
    conn.execute(f"""
        CREATE OR REPLACE TABLE {sample_table_name} AS 
        SELECT * FROM {table}
        ORDER BY RANDOM()
        LIMIT 500;
    """)

    # Show the results
    results = conn.execute(f"SELECT * FROM {sample_table_name};").fetchall()
    print(f"Sample Data for {table} (500 random rows):")
    for result in results:
        print(result)
# ========================================== EXPORT TO SQLITE ==========================================
print("""======================================= Exporting to SQLite =======================================""")

# Create SQLite connection
sqlite_conn = sqlite3.connect('steam_reviews_samples_500.db')

# List of tables to transfer
tables = [
    'steam_reviews_sample_500',
    'question1_1_samples_500', 'question1_2_samples_500', 'question1_3_samples_500',
    'question2_1_samples_500', 'question2_2_samples_500', 'question2_3_samples_500',
    'question3_1_samples_500', 'question3_2_samples_500',
    'question4_samples_500', 'question5_samples_500'
]

# Copy each table
for table in tables:
    # Read from DuckDB
    df = conn.execute(f"SELECT * FROM {table}").fetchdf()

    # Write to SQLite
    df.to_sql(
        name=table,
        con=sqlite_conn,
        if_exists='replace',
        index=False
    )
    print(f"Exported {table} to SQLite ({len(df)} rows)")

# Clean up
sqlite_conn.commit()
sqlite_conn.close()
conn.close()

print("""======================================= Export Complete =======================================""")

