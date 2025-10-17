
# IMPORTS

import numpy as np
import streamlit as st
from pyvis.network import Network
import networkx as nx
from streamlit import components as st_display
from src.mazeData import defineMazeAvailableActions
from src.mazeData import makeMazeTransformationModel
from src.maze2025GraphClass import mazeGraph
from src.mazeData import mazeStatesLocations
from src.mazeData import intTupleTostr
from src.mazeProblemClass import MazeProblem
from src.PS_agentPrograms import BestFirstSearchAgentProgram
from src.agents import ProblemSolvingMazeAgentBFS
from src.naigationEnvironmentClass import MazeNavigationEnvironment

# MAKE MAZE, ACTIONS, TRANSITION MODEL & GRAPH

n=7
def makeMaze(n):
    size = (n,n)
    proba_0 =0.25 # resulting array will have 30% of zeros
    arrMaze=np.random.choice([0, 1], size=size, p=[proba_0, 1-proba_0])
    return arrMaze
maze1 = makeMaze(n)
print(maze1)
mazeAvalActs=defineMazeAvailableActions(maze1)
maze1TM=makeMazeTransformationModel(mazeAvalActs)
mazeWorldGraph = mazeGraph(maze1TM, mazeStatesLocations(list(maze1TM.keys())))

# PYVIS

net_maze = Network( heading="Lab4. Examples of Maze World Problem",
                bgcolor ="#242020",
                font_color = "white",
                height = "750px",
                width = "100%"
)
net_maze.toggle_physics(False)
nodeColors={
    "wall" : "red",
    "path" : "white"
}
nodeColorsList=[]
for node in mazeWorldGraph.origin.keys():
    if maze1[node[0],node[1]]==1:
        nodeColorsList.append(nodeColors["path"])
    else:
        nodeColorsList.append(nodeColors["wall"])
nodes=["-".join(str(item) for item in el) for el in mazeWorldGraph.origin.keys()]
x_coords = []
y_coords = []
for node in mazeWorldGraph.origin.keys():
    x,y=mazeWorldGraph.getLocation(node)
    x_coords.append(x)
    y_coords.append(y)
sizes=[10]*len(nodes)
# PYVIS NODES
net_maze.add_nodes(nodes, color=nodeColorsList, x=x_coords, y=y_coords, size=sizes, title=nodes)
# PYVIS EDGES
edge_weights = {(intTupleTostr(k), intTupleTostr(v2)) : k2 for k, v in mazeWorldGraph.origin.items() for k2, v2 in v.items()}
edges=[]
for node_source in mazeWorldGraph.nodes():
    for node_target, action in mazeWorldGraph.get(node_source).items():
        if (intTupleTostr(node_source),intTupleTostr(node_target)) not in edges and (intTupleTostr(node_target), intTupleTostr(node_source)):
            net_maze.add_edge(intTupleTostr(node_source),intTupleTostr(node_target), label=edge_weights[(intTupleTostr(node_source),intTupleTostr(node_target))])
            edges.append((intTupleTostr(node_source),intTupleTostr(node_target)))

# MAZE PROBLEM, AGENT ENVIRONMENT

initState, goalState=(0,1),(0,3)
mp1=MazeProblem(initState,goalState,mazeWorldGraph)
BFSAP1=BestFirstSearchAgentProgram()
seq=BFSAP1(mp1)
BFS_MazeAgent1=ProblemSolvingMazeAgentBFS(initState,mazeWorldGraph,goalState)
maze_Env1=MazeNavigationEnvironment(mazeWorldGraph)

# NODE COLORS
nodeColors.setdefault('goal', "green")
nodeColors.setdefault('init', "gold")
for node in net_maze.nodes:
    if node['id']==intTupleTostr(goalState):
        node['color']=nodeColors['goal']
    elif node['id']==intTupleTostr(initState):
        node['color']=nodeColors['init']

# net_maze.show("graphMaze1.html", notebook=False)
# maze_Env1.add_thing(BFS_MazeAgent1)
# maze_Env1.run()

# STREAM LIB

def drawBtn(e,a,c):
    option= [e,a,c]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])

def AgentStep(opt):
    st.header("Resolving the Asteroid Problem ...")
    e, a, c = opt[0], opt[1], opt[2]
    if not st.session_state["clicked"]:
        st.session_state["env"] = e
        st.session_state["agent"] = a
        st.session_state["nodeColors"] = c

    if e.is_agent_alive(a):
        e.step()
        st.success(" Agent now at : {}.".format(a.state))
        st.info("Current Agent performance {}:".format(a.performance))
        c[a.state] = "orange"
        st.info("State of the Environment:")
        buildGraph(e.status, c)
    else:
        if a.state == a.goal:
            st.success(" Agent now at the goal state: {}.".format(a.state))
        else:
            st.error("Agent in location {} and it is dead.".format(a.state))

    st.session_state["clicked"] = True

def buildGraph(graphData, nodeColorsDict):

    net = Network(heading="Lab4. Examples of Maze World Problem",
                       bgcolor="#242020",
                       font_color="white",
                       height="750px",
                       width="100%"
                       )
    net_maze.toggle_physics(False)
    nodes = graphData.nodes()
    g = nx.Graph()

    # NODE COLOR DICT

    # # add the nodes
    for node in nodes:
        g.add_node(node, color=nodeColorsDict[node])

    # add the edges
    edges = []
    for source in graphData.nodes():
        for target, dist in graphData.get(source).items():
            if set((source, target)) not in edges:
                edges.append(set((source, target)))
    g.add_edges_from(edges)

    # # add edge labels
    edge_dict = {}
    # for start, inner_dict in my_data3.items():
    #     for end, label in inner_dict.items():
    #         for u, v, data in g.edges(data=True):
    #             if u == start and v == end:
    #                 data['label'] = label

    # generate the graph
    file_name = 'new_asteroid.html'
    net.from_nx(g)
    net.save_graph(file_name)
    HtmlFile = open(file_name, 'r', encoding='utf-8')
    st_display.html(HtmlFile.read(), height=700, width=1000)

def makeDefaultColors(dictData):
    nodeColors=dict.fromkeys(dictData.keys(), "white")
    for key, value in nodeColors.items():
        print(key)
        print(value)

    return nodeColors

# # # MAIN # # #

def main():
    # Initialize Session State
    if "clicked" not in st.session_state:
        st.session_state["clicked"] = False
    if "env" not in st.session_state:
        st.session_state["env"] = None
    if "agent" not in st.session_state:
        st.session_state["agent"] = None
    if "nodeColors" not in st.session_state:
        st.session_state["nodeColors"] = None

    # FIRST STATE
    if not st.session_state["clicked"]:
        # Set header title
        st.header("Problem Solving Agents: Asteroid")
        st.header("_Initial Env._", divider=True)
        # Create Graph, Environment, Agent
        mazeWorldGraph = mazeGraph(maze1TM, mazeStatesLocations(list(maze1TM.keys())))
        nodeColors = makeDefaultColors(mazeWorldGraph.graph_dict)
        initState = "0,0"
        goalState = "7,7"
        maze_Env1=MazeNavigationEnvironment(mazeWorldGraph)
        BFS_MazeAgent1=ProblemSolvingMazeAgentBFS(initState,mazeWorldGraph,goalState)
        maze_Env1.add_thing(BFS_MazeAgent1)
        nodeColors[BFS_MazeAgent1.state] = "red"
        nodeColors[BFS_MazeAgent1.goal] = "green"
        # Show Environment
        st.header("State of the Environment", divider="red")
        buildGraph(mazeWorldGraph, nodeColors)
        st.info(f"The Agent in: {BFS_MazeAgent1.state} with performance {BFS_MazeAgent1.performance}.")
        st.info(f"The Agent goal is: {BFS_MazeAgent1.goal} .")
        # Next Step Button
        drawBtn(maze_Env1, BFS_MazeAgent1, nodeColors)

    # EACH STEP
    if st.session_state["clicked"]:
        if st.session_state["env"].is_agent_alive(st.session_state["agent"]):
            st.success(" Agent is working...")
            drawBtn(st.session_state["env"], st.session_state["agent"], st.session_state["nodeColors"])


# RUN
if __name__ == '__main__':
    main()
