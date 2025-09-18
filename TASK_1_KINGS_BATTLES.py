import pandas as pd
from pyvis.network import Network
from bs4 import BeautifulSoup
#   .\venv\Scripts\activate
  

# Loading the data
data = pd.read_csv("data/game-of-thrones-battles.csv")

# Selecting Relevant Data
battles_df=data.loc[:,['name','attacker_king','defender_king','attacker_size','defender_size']]

# Remove rows with any missing values (NaN)
battles_df=battles_df.dropna()

# Instantiate a Network object from pyvis.network.
net5kings = Network(heading="Task 1. Building Interactive Network of battles of the War of 5", 
                    bgcolor = "#242020",
                    font_color = "white",
                    height = "1000px",
                    width = "100%",
                    directed = True, # we have directed graph
                    notebook = False,
                    cdn_resources = "remote")



# Get all kings for nodes
attackers = set(battles_df['attacker_king'].unique())
defenders = set(battles_df['defender_king'].unique())
all_kings = list(attackers.union(defenders))
net5kings.add_nodes(all_kings)

# Map all battle names ( for edge titles )
map_battle_names = battles_df.groupby(['attacker_king', 'defender_king'])['name'].apply(list).to_dict()

# Group by attacker_king and defender_king, then count the number of battles ( for edge weight )
battle_counts = battles_df.groupby(['attacker_king', 'defender_king']).size().reset_index(name='# of battles')

# Add edges between kings
for index, row in battle_counts.iterrows():
    atk_king = row['attacker_king']
    def_king = row['defender_king']
    num_battles = row['# of battles']
    name_battles = ", ".join(map_battle_names[(atk_king, def_king)])
    net5kings.add_edge(atk_king, def_king, width=num_battles, title=name_battles)

# Color values
nodeColors = {
    0:"blue",
    1:"green",
    2:"orange",
    3:"purple",
    4:"gold",
    5:"red"}

# Add value to nodes, where value = N+1 and N is number of kings.
neighbour_map = net5kings.get_adj_list()
for node in net5kings.nodes:
    node["value"] = len(neighbour_map[node["id"]])
    node["color"] = nodeColors[node["value"]+1]

net5kings.toggle_physics(True)
net5kings.save_graph('NET5KINGS.html')

# Fix header issue
# Load the HTML file
with open('NET5KINGS.html', "r") as file:
    html = file.read()
# Parse the HTML
soup = BeautifulSoup(html, "html.parser")
# Find and remove the duplicate title
titles = soup.find_all("h1")
if len(titles) > 1:
    for title in titles[1:]:
        title.decompose()
# Save the modified HTML
with open('NET5KINGS.html', "w") as file:
    file.write(str(soup))

