import streamlit as st
import sqlite3
import networkx as nx
from pyvis.network import Network

# SQLite connection
conn = sqlite3.connect('steam_reviews_samples_500.db')

# 1. Load user, game, and review data
def load_graph_data():
    users = conn.execute('''
        SELECT DISTINCT 
            "author.steamid" as steamid,
            "author.num_games_owned",
            "author.num_reviews",
            "author.playtime_forever"
        FROM steam_reviews_sample_500
        LIMIT 5
    ''').fetchall()

    games = conn.execute('''
        SELECT DISTINCT 
            app_id,
            app_name 
        FROM steam_reviews_sample_500
        LIMIT 5
    ''').fetchall()

    reviews = conn.execute('''
        SELECT 
            review_id,
            recommended,
            language,
            votes_helpful,
            steam_purchase,
            received_for_free,
            "author.steamid",
            app_id
        FROM steam_reviews_sample_500
        LIMIT 5
    ''').fetchall()

    return users, games, reviews


# 2. Build NetworkX graph
def build_graph(users, games, reviews):
    G = nx.DiGraph()

    # Add nodes
    for user in users:
        G.add_node(f'User_{user[0]}', type='user', label=f'User_{user[0]}')

    for game in games:
        G.add_node(f'Game_{game[0]}', type='game', label=f'Game_{game[1]}')

    for review in reviews:
        G.add_node(f'Review_{review[0]}', type='review', label=f'Review_{review[0]}')

    # Add edges
    for review in reviews:
        # Edge: User -> Review
        G.add_edge(
            f'User_{review[6]}',
            f'Review_{review[0]}',
            label='WRITES'
        )
        # Edge: Review -> Game
        G.add_edge(
            f'Review_{review[0]}',
            f'Game_{review[7]}',
            label='FOR'
        )

    return G


# 3. Create interactive Pyvis graph
def create_interactive_graph(G):
    # Create Pyvis network
    net = Network(notebook=True, directed=True, height="600px", width="100%")

    # Add nodes and edges to the network
    for node, data in G.nodes(data=True):
        net.add_node(node, label=data['label'], color=get_node_color(data['type']))

    for edge in G.edges(data=True):
        net.add_edge(edge[0], edge[1], label=edge[2]['label'])

    # Graph options
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "stabilization": {
          "iterations": 100
        }
      },
      "edges": {
        "arrows": {
          "to": {
            "enabled": true,
            "scaleFactor": 1
          }
        },
        "smooth": {
          "type": "dynamic"
        }
      }
    }
    """)

    # Save the graph as an HTML file
    net.save_graph("graph.html")
    return "graph.html"


# Helper function for node color based on type
def get_node_color(node_type):
    colors = {
        'user': '#1f77b4',
        'game': '#ff7f0e',
        'review': '#2ca02c'
    }
    return colors.get(node_type, '#000000')


# Streamlit interface
st.title('🎮 Steam Graph Database Visualization')
st.markdown("""
### Graph DB Schema from SQLite Data:
- **🟦 Users**: Identified by steamid
- **🟩 Reviews**: Contain language and rating
- **🟧 Games**: Identified by app_id
""")

if st.button('Build Graph'):
    users, games, reviews = load_graph_data()
    G = build_graph(users, games, reviews)
    graph_file = create_interactive_graph(G)

    # Display the interactive graph in Streamlit
    with open(graph_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=600)
else:
    st.warning('Click the button to build the graph')

conn.close()
