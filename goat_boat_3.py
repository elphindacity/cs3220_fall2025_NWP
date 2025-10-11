

# IMPORTS


import streamlit as st
import streamlit.components.v1 as components # to display the HTML code
import networkx as nx # Networkx for creating graph data
from pyvis.network import Network # to create the graph as an interactive html object
from src.graphClass import Graph
from MyData import my_data, print_dict, dead_states, my_data2, my_data3
from src.agents import ProblemSolvingNavAgentBFS
from src.naigationEnvironmentClass import NavigationEnvironment


# FUNCTIONS


def drawBtn(e,a,c):
    option= [e,a,c]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    
def AgentStep(opt):
    st.header("Resolving the Goat Boat Problem ...")
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
        buildGraph(e.status, c) 
    else:
        if a.state==a.goal:
            st.success(" Agent now at the goal state: {}.".format(a.state))
        else:
            st.error("Agent in location {} and it is dead.".format(a.state))
        
    st.session_state["clicked"] = True
          
def buildGraph(graphData, nodeColorsDict):
    net = Network(
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%") 
    nodes=graphData.nodes()
    # initialize graph
    g = nx.Graph()
    
    # add the nodes
    for node in nodes:
        g.add_node(node, color=nodeColorsDict[node])
    # add the edges
    edges=[]
    for node_source in graphData.nodes():
        for node_target, dist in graphData.get(node_source).items():
            if set((node_source,node_target)) not in edges:
                edges.append(set((node_source,node_target)))                
    g.add_edges_from(edges)
    
    # add edge labels
    edge_dict = {}
    for start, inner_dict in my_data3.items():
        for end, label in inner_dict.items():
            for u, v, data in g.edges(data=True):
                if u == start and v == end:
                    data['label'] = label

    # generate the graph
    net.from_nx(g)
    net.save_graph('goat_boat.html')
    HtmlFile = open(f'goat_boat.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height = 700,width=1000)
    
    
def makeDefaultColors(dictData):
    nodeColors=dict.fromkeys(dictData.keys(), "white")
    for key, value in nodeColors.items():
        if key in dead_states:
            nodeColors[key] = "gray"
    print("\n\n\n\n\n")
    print_dict(nodeColors)
    print("\n\n\n\n\n")

    return nodeColors


# # # MAIN # # #


def main():  

    # Initialize Session State 
    if "clicked" not in st.session_state:
        st.session_state["clicked"] = False
    if "env" not in st.session_state:
        st.session_state["env"]=None    
    if "agent" not in st.session_state:
        st.session_state["agent"]=None
    if "nodeColors" not in st.session_state:
        st.session_state["nodeColors"]=None

    # FIRST STATE    
    if not st.session_state["clicked"]:
        # Set header title
        st.header("Problem Solving Agents: Goat Boat Problem")
        st.header("_Initial Env._", divider=True)
        # Create Graph, Environment, Agent
        the_graph = Graph(my_data)
        nodeColors = makeDefaultColors(the_graph.graph_dict)
        initState = "LLLL"
        goalState = "RRRR"
        the_env = NavigationEnvironment(the_graph)
        BFSnavAgent = ProblemSolvingNavAgentBFS(initState,the_graph,goalState)              
        the_env.add_thing(BFSnavAgent)
        nodeColors = makeDefaultColors(the_graph.graph_dict)
        nodeColors[BFSnavAgent.state] = "red"
        nodeColors[BFSnavAgent.goal] = "green"
        # Show Environment
        st.header("State of the Environment", divider="red")
        buildGraph(the_graph, nodeColors) 
        st.info(f"The Agent in: {BFSnavAgent.state} with performance {BFSnavAgent.performance}.")
        st.info(f"The Agent goal is: {BFSnavAgent.goal} .")
        # Next Step Button
        drawBtn(the_env,BFSnavAgent,nodeColors)
    
    # EACH STEP
    if st.session_state["clicked"]:
        if st.session_state["env"].is_agent_alive(st.session_state["agent"]):
            st.success(" Agent is working...")
            drawBtn(st.session_state["env"],st.session_state["agent"], st.session_state["nodeColors"])
       
# RUN
if __name__ == '__main__':
    main()
    
    

