# python -m streamlit run goat_boat2.py

import streamlit as st
from pyvis.network import Network
from bs4 import BeautifulSoup
import streamlit.components.v1 as st_display

from graphClass import Graph
from MyData import my_data
from navigationEnvironmentClass import NavigationEnvironment
from agents import ProblemSolvingNavAgentBFS

from problemSolvingAgentClass import ProblemSolvingAgent, UCS_program
from PS_environment_class import PS_Environment

# # # FUNCTIONS # # #

def drawBtn(e,a,c):
    option= [e,a,c]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])

def AgentStep(opt):
    e,a,c= opt[0],opt[1],opt[2]
    if not st.session_state["clicked"]:
        st.session_state["env"]=e
        st.session_state["agent"]=a
        st.session_state["nodeColors"]=c    
    
    if e.is_agent_alive(a):
        e.step()
        st.success(" Agent now at : {}.".format(a.state))
        st.info("Current Agent performance {}:".format(a.performance))
        c[a.state]="orange"
        st.info("State of the Environment:")
        updateGraph(e.status, c) 
    else:
        if a.state==a.goal:
            st.success(" Agent now at the goal state: {}.".format(a.state))
        else:
            st.error("Agent in location {} and it is dead.".format(a.state))
        
    st.session_state["clicked"] = True

def updateGraph(network):
    name = 'goat_boat.html'
    network.save_graph(name)
    fix_pyvis_header(name)
    with open(name, 'r') as file: html = file.read()
    st_display.html(html, height=700)

# # # HTML FIX # # #

def fix_pyvis_header(name):
    # Load the HTML file
    with open(name, "r") as file:
        html = file.read()
    # Parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    # Find and remove the duplicate title
    titles = soup.find_all("h1")
    if len(titles) > 1:
        for title in titles[1:]:
            title.decompose()
    # Save the modified HTML
    with open(name, "w") as file:
        file.write(str(soup))

# # # STATE SPACE GENERATION # # #

class Node:

    def __init__(self, name, parent=None, cost=1):
        self.name = name
        self.parent = parent
        self.actions = self.find_adjacent()
        self.cost = cost
        self.path_cost = self.get_path_cost()
        self.depth = self.set_depth()
        self.color = "white"

    def set_color(self,color):
        self.color = color

    def set_depth(self):
        if self.parent :
            return self.parent.depth + 1
        else : return 0

    def get_path_cost(self):
        if self.parent :
            return self.parent.cost + self.cost
        else :
            return self.cost

    def find_adjacent(self):
        adj_list = []
        for x in range(4):
            adjacent = list(self.name)
            if (self.name[0] == 'L') and (self.name[x] == 'L') :
                adjacent[0] = 'R'
                adjacent[x] = 'R'
                adjacent = ''.join(adjacent)
                adj_list.append(adjacent)
            if (self.name[0] == 'R') and (self.name[x] == 'R') :
                adjacent[0] = 'L'
                adjacent[x] = 'L'
                adjacent = ''.join(adjacent)
                adj_list.append(adjacent)
        return adj_list

def create_node_list(initial_node):
    node_list = [initial_node]
    node_names = [initial_node.name]
    for node in node_list:
        for action in node.actions:
            if action not in node_names:
                node_names.append(action)
                new_node = Node(action, node)
                node_list.append(new_node)
    return node_list
        
def get_dead_states(node_list):
    # make a list of names
    state_list = []
    for node in node_list :
        state_list.append(node.name)
    # check list of names for dead states
    dead_states = []
    for state in state_list:
        if (state[1] == state[2]) and (state[0] != state[2]):
            dead_states.append(state)
        elif (state[2] == state[3]) and (state[0] != state[2]):
            dead_states.append(state)
    dead_states = list(set(dead_states))
    # return it
    return dead_states

def makeDefaultColors(dictData):
    return dict.fromkeys(dictData.keys(), "white")


def main():

    if "clicked" not in st.session_state:
        st.session_state["clicked"] = False
        
    if "env" not in st.session_state:
        st.session_state["env"]=None
        
    if "agent" not in st.session_state:
        st.session_state["agent"]=None
        
    if "nodeColors" not in st.session_state:
        st.session_state["nodeColors"]=None

    # INITIAL STATE
    if not st.session_state["clicked"]:

        # Instantiate a Network
        NET = Network(heading="Task 1. Goat in a Boat", 
                        bgcolor = "#242020",
                        font_color = "white",
                        height = "1000px",
                        width = "100%",
                        directed = False, # we have directed graph
                        notebook = False,
                        cdn_resources = "remote")
        
        # Generate Nodes
        initial_node = Node('LLLL', cost=0)
        initial_node.set_color("green")
        node_list = create_node_list(initial_node)
        dead_nodes = get_dead_states(node_list)
        for node in node_list:
            if node.name == 'RRRR' :
                node.set_color('red')
            if node.name in dead_nodes:
                node.set_color('gray')
            NET.add_node(node.name, level=node.depth, color=node.color)

        # Generate Edges
        for node in node_list:
            for action in node.actions:
                NET.add_edge(node.name, action)

        # Save Graph
        name = 'goat_boat.html'
        NET.toggle_physics(True)
        NET.repulsion_node_distance = 500
        NET.layout = "circular"
        NET.save_graph(name)
        fix_pyvis_header(name)

        # Streamlib display html
        with open(name, 'r') as file: html = file.read()
        st_display.html(html, height=700)

        # INITIALIZE ENVIRONMENT, AGENT, PROBLEM
        the_graph = Graph(my_data)
        nodeColors= makeDefaultColors(the_graph.graph_dict)
        the_env = NavigationEnvironment(the_graph)
        BFSnavAgent = ProblemSolvingNavAgentBFS('LLLL',the_graph,'RRRR')
        the_env.add_thing(BFSnavAgent)  

        drawBtn(the_env, BFSnavAgent, nodeColors)
    
    if st.session_state["clicked"]:
        if st.session_state["env"].is_agent_alive(st.session_state["agent"]):
            #st.warning("Agent Step Done!")
            st.success(" Agent is working...")
            drawBtn(st.session_state["env"],st.session_state["agent"], st.session_state["nodeColors"])

main()