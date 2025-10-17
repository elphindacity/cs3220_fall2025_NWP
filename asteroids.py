
# IMPORTS

from random import choices # make_maze
from pyvis.network import Network # pyvis
from bs4 import BeautifulSoup # fix_pyvis_header
from queue import PriorityQueue # best first search

# UTILITY FUNCTIONS

def make_maze(n):
    population = [0, 1]
    weights = [0.25, 0.75]
    maze = [ ]
    for y in range(n):
        row = []
        for x in range(n):
            cell = choices(population, weights=weights)[0]
            row.append(cell)
        maze.append(row)
    return maze

def print_array(maze):
    for row in maze:
        print(row)
    print("")

def print_dict(actions):
    sorted_keys = sorted(actions.keys(), key=lambda x: (x[1], x[0]))
    for key, value in actions.items():
        print(key, " : ", value)
    print("")

def make_node_colors(maze):
    node_colors = []
    for row in range(len(maze)):
        for col in range(len(maze)):
            x = col
            y = row
            if maze[y][x] == 1:
                node_colors.append("white")
            else:
                node_colors.append("red")
    return node_colors

def fix_pyvis_header(file_name):
    # Load the HTML file
    with open(file_name, "r") as file:
        html = file.read()
    file.close()
    # Parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    # Find and remove the duplicate title
    titles = soup.find_all("h1")
    if len(titles) > 1:
        for title in titles[1:]:
            title.decompose()
    # Save the modified HTML
    with open(file_name, "w") as file:
        file.write(str(soup))
    file.close()

# # # GRAPH CLASS # # #

class MazeGraph:

    def __init__(self, maze):
        self.maze = maze
        self.actions = self.define_actions(maze) # all actions ( used to gen graph_Dict and nodes(keys) )
        self.graph_dict = self.make_transition_model(self.actions) # transition model
        self.nodes = list(self.actions.keys())
        self.all_x_loc = []
        self.all_y_loc = []
        self.locations = self.make_locations(self.nodes)

    def define_actions(self, maze):
        # FORMAT = { '0,1' : ['left', 'right', 'down'] }
        actions = {}
        size = len(maze)
        for y in range(size):
            for x in range(size):
                cell_name = str(x) + ',' + str(y)
                cell_actions = ['left', 'right', 'up', 'down']
                if maze[y][x] == 0:
                    cell_actions = []
                else:
                    if x == 0 or maze[y][x - 1] == 0:
                        cell_actions.remove('left')
                    if x == size - 1 or maze[y][x + 1] == 0:
                        cell_actions.remove('right')
                    if y == 0 or maze[y - 1][x] == 0:
                        cell_actions.remove('up')
                    if y == size - 1 or maze[y + 1][x] == 0:
                        cell_actions.remove('down')
                actions[cell_name] = cell_actions
        return actions

    def make_transition_model(self, actions):
        # FORMAT = {'0,1':{'left':'0,0', 'right':'0,2', 'down':'1,1'}}
        TM = {}
        for key, action_list in actions.items():
            inner_dict = {}
            for action in action_list:
                x = int(key[0])
                y = int(key[2])
                next_cell = ""
                if action == 'left':
                    next_cell = str(x-1) + "," + str(y)
                elif action == 'right':
                    next_cell = str(x+1) + "," + str(y)
                elif action == 'up':
                    next_cell = str(x) + "," + str(y-1)
                elif action == 'down':
                    next_cell = str(x) + "," + str(y+1)
                inner_dict[action] = next_cell
                TM[key] = inner_dict
        return TM

    def get(self, a, b=None):
        # get(a) returns a dictionary of links and distances ( could be empty )
        # get(a,b) returns the distance (or None.)
        if a not in self.graph_dict:
            self.graph_dict[a] = {}
        links = self.graph_dict[a]
        if b is None:
            return links
        else:
            if b in links:
                return links[b]
            else:
                return None

    def get_location(self, a):
        return self.locations.get(a)

    def make_locations(self, key_list):
        x = []
        y = []
        for key in key_list:
            x.append(int(key[0]) * 50)
            y.append(int(key[2]) * 50)
        self.all_x_loc = x
        self.all_y_loc = y
        zipped = zip(x, y)
        return dict(zip(key_list, zipped))

# # # PYVIS # # #

test_maze = [
    [ 1,1,1,1,1,0,1 ],
    [ 0,1,0,0,1,0,1 ],
    [ 1,1,1,0,1,1,1 ],
    [ 1,0,1,0,1,0,1 ],
    [ 1,1,1,0,0,0,1 ],
    [ 0,0,0,0,1,1,1 ],
    [ 1,1,1,1,1,0,1 ]
]

maze_graph = MazeGraph(test_maze)

net_maze = Network(
    heading="Lab4. Asteroid",
    bgcolor ="#242020",
    font_color = "white",
    height = "750px",
    width = "100%"
)

# ADD NODES TO PYVIS
nodes = maze_graph.nodes
node_color_list = make_node_colors(maze_graph.maze)
x_coords = maze_graph.all_x_loc
y_coords = maze_graph.all_y_loc
sizes=[10]*len(nodes)
net_maze.add_nodes(nodes, color=node_color_list, x=x_coords, y=y_coords, size=sizes, title=nodes)

# ADD EDGES
current_node = '0,0'
for node in net_maze.nodes:
    if node['id'] == current_node:
        node['color'] = 'lightgreen'
        # node['shape'] = 'image'
        # node['image'] = 'https://cdn2.iconfinder.com/data/icons/circle-icons-1/64/rocket-512.png'
data = maze_graph.graph_dict[current_node]
print(data)
edge_weights = {}
for action,node in data.items():
    edge_weights[(current_node, node)] = action
    # EDGE WEIGHT FORMAT { ('0-0', '0-1'): 'right', ... }
edges=[]
for action, target in maze_graph.get(current_node).items():
    if (current_node,target) not in edges:
        net_maze.add_edge(current_node,target,label=edge_weights[(current_node,target)])
        edges.append((current_node,target))

# DISABLE PHYSICS, SAVE GRAPH ( AND SHOW )
net_maze.toggle_physics(False)
file_name = 'asteroids.html'
net_maze.save_graph(file_name)
fix_pyvis_header(file_name)
#net_maze.show(file_name, notebook=False)

# # # MAZE PROBLEM CLASS # # #

class MazeProblem:

    def __init__(self, initial, goal, graph):
        self.initial = initial
        self.goal = goal
        self.graph = graph # State space = {state1:{action1:state2}}

    def actions(self, state):
        actions = []
        for key, val in self.graph.graph_dict[state].items():
            actions.append(key)
        return actions

    def result(self, state, action):
        # Returns the state that results from executing given action in given state.
        return self.graph.graph_dict[state][action]

    def goal_test(self, state):
        # Returns True if the given state is the goal.
        return state == self.goal

    def path_cost(self, cost_so_far, state_a, action, state_b):
        cost_of_step = self.graph.get(state_a,state_b)
        if (cost_of_step == 0) or (cost_of_step is None) :
            cost_of_step = 1
        return cost_so_far + cost_of_step

initial = '0,0'
goal = '0,6'
maze_problem = MazeProblem(initial,goal,maze_graph)
a = maze_problem.actions(initial)

# # # NODE CLASS # # #

class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = self.set_depth()
        self.color = "white"

    def set_depth(self):
        if self.parent : return self.parent.depth + 1
        else : return 0

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def child_node(self, problem, action):
        # using the MazeProblem.result function to see where those actions lead to
        next_state = problem.result(self.state, action)
        # and generating a new node (called a child node)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        '''
        Following the PARENT pointers back from a node allows us to 
        recover the states and actions along the path to that node. 
        Doing this from a goal node gives us the solution
        '''
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

# # # BEST FIRST SEARCH AGENT PROGRAM # # #

def BestFirstSearchAgentProgram(f=None):
    # with BFS we choose a node, n, with minimum value of some evaluation function, f (n).

    def program(problem):

        nodeColors = {
            "start": "red",
            "goal": "green",
            "frontier": "orange",
            "expanded": "pink"
        }

        node = Node(problem.initial)
        # node.color=nodeColors["start"]
        # print(node.state)
        frontier = PriorityQueue()
        frontier.put((1, node))
        print(f"The {node} is being pushed to frontier ...")
        # node.color=nodeColors["frontier"]
        reached = {problem.initial: node}

        while frontier:
            node = frontier.get()[1]
            # node.color=nodeColors["expanded"]
            print(f"The {node} is being extracted from frontier ...")

            if problem.goal_test(node.state):
                #node.color = nodeColors["goal"]
                print(f"We have found our goal:  {node}!")
                return node

            # reached.add(node.state)
            for child in node.expand(problem):
                if child.state not in reached or child.path_cost < reached[child.state].path_cost:
                    frontier.put((1, child))
                    print(f"The child {child} is being pushed to frontier ...")
                    # child.color=nodeColors["frontier"]
                    reached.update({child.state: child})

            # node.color=nodeColors["expanded"]
        return None

    return program

BFS = BestFirstSearchAgentProgram()
sequence = BFS(maze_problem)

# # # MAZE AGENT # # #

class Maze_Agent():
    def __init__(self, initial_state, dataGraph, goal, program):
        self.initial_state = initial_state
        self.dataGraph = dataGraph
        self.goal = goal
        self.program = program
        self.performance = len(dataGraph.nodes)
        self.seq = []  # solution.
        self.alive = True
        self.state = self.initial_state

    def __call__(self, percept, curGoal=None):
        """Formulate a goal and problem, then
        search for a sequence of actions to solve it."""
        # 4-phase problem-solving process
        # print(0)
        temp = self.state
        self.state = self.update_state(self.state, percept)

        if not self.seq:
            goal = self.formulate_goal(self.state)

            if isinstance(goal, list) and len(goal) > 1:
                percept = self.state
                while len(self.goal) > 0:
                    # 4-phase problem-solving process
                    self.state = self.update_state(self.state, percept)
                    current_goal = self.goal[0]
                    goal = current_goal
                    problem = self.formulate_problem(self.state, goal)
                    self.seq.extend(self.search(problem))
                    percept = current_goal
                    self.goal.remove(goal)
                self.state = temp
            else:
                problem = self.formulate_problem(self.state, goal)
                self.seq = self.search(problem)

            if not self.seq:
                return None
        else:
            print("I have already don my work. Find someone else")

        # return self.seq.pop(0)
        return None

    def update_state(self, state, percept):
        return percept

    def formulate_goal(self, state):
        if self.goal is not None:
            return self.goal
        else:
            print("No goal! can't work!")
            return None

    # a description of the states and actions necessary to reach the goal
    def formulate_problem(self, state, goal):
        # instance of Maze ProblemClass
        problem = MazeProblem(state, goal, self.dataGraph)
        return problem

    def search(self, problem):
        seq = self.program(problem)
        solution = self.actions_path(seq.path())
        print("Solution (a sequence of actions) from the initial state to a goal: {}".format(solution))
        return solution

    def actions_path(self, p):
        acts = []
        for n in p:
            acts.append(n.action)
        return acts[1:]

maze_agent = Maze_Agent(initial,maze_graph,goal, BFS)

# # # ENVIRONMENT # # #

class Maze_Environment():
    def __init__(self, navGraph):
        self.status = navGraph
        self.agents = []

    def percept(self, agent):
        # Returns the agent's location, and the location status (Dirty/Clean).
        return agent.state

    def is_agent_alive(self, agent):
        return agent.alive

    def update_agent_alive(self, agent):
        if agent.performance <= 0:
            agent.alive = False
            print("Agent {} is dead.".format(agent))
        elif agent.state == agent.goal or len(agent.seq) == 0:
            agent.alive = False
            if len(agent.seq) == 0:
                print("Agent reached all goals")
            else:
                print(f"Agent reached the goal: {agent.goal}")

    def execute_action(self, agent, action):
        '''Check if agent alive, if so, execute action'''
        if self.is_agent_alive(agent):
            """Change agent's location -> agent's state;
            Track performance.
            -1 for each move."""
            agent.state = agent.update_state(agent.state, action)
            agent.performance -= 1
            print(f"Agent in {agent.state} with performance = {agent.performance}")
            self.update_agent_alive(agent)

            # if action == 'Right':
            #     agent.location = loc_B
            #     agent.performance -= 1
            #     self.update_agent_alive(agent)
            # elif action == 'Left':
            #     agent.location = loc_A
            #     agent.performance -= 1
            #     self.update_agent_alive(agent)
            # elif action == 'Suck':
            #     if self.status[agent.location] == 'Dirty':
            #         agent.performance += 10
            #     self.status[agent.location] = 'Clean'

    # def default_location(self, thing):
    #       """Agents start in either location at random."""
    #       print("Agent is starting in random location...")
    #       return random.choice([loc_A, loc_B])

    def step(self):
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    # with agent.state because for PS Agent we don't need to percive
                    action = agent.seq.pop(0)
                    print("Agent decided to do {}.".format(action))
                    actions.append(action)
                else:
                    actions.append("")

            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
        else:
            print("There is no one here who could work...")

    def is_done(self):
        # By default, we're done when we can't find a live agent.
        return not any(agent.alive for agent in self.agents)

    def run(self, steps=10):
        # Run the Environment for given number of time steps.
        for step in range(steps):
            if self.is_done():
                return
            print("step {0}:".format(step + 1))
            self.step()

    def add_thing(self, thing, location=None):
        # from agentClass import Agent
        from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
        if thing in self.agents:
            print("Can't add the same agent twice")
        else:
            if isinstance(thing, SimpleProblemSolvingAgentProgram):
                thing(thing.state)
                # thing.performance = 0
                # thing.location = location if location is not None else self.default_location(thing)
                print(f"The Agent in {thing.state} with performance {thing.performance}")
                self.agents.append(thing)

    def delete_thing(self, thing):
        if thing in self.agents:
            self.agents.remove(thing)

maze_env = Maze_Environment(maze_graph)

for node in net_maze.nodes:
    if node['id']==goal:
        node['color']='green'
    elif node['id']==initial:
        node['color']='gold'

# # # ADD AGENT TO ENV # # #

maze_env.add_thing(maze_agent)
maze_env.run()

# # # TEST RUN # # #

sequence = maze_agent.search(maze_problem)
print("SEQUENCE : ", sequence)
for action in sequence:
    print("\nCURRENT NODE : ", current_node)
    print("ACTION IN SEQUENCE: ", action)
    TM = maze_graph.get(current_node)
    print("TM : ", TM)

    # UPDATE EDGE LABEL
    target = TM[action]
    print("TARGET : ", target)
    net_maze.add_edge(current_node, target, label=action)

    # UPDATE NODE PATH COLORS
    current_node = TM[action]
    print("CURRENT NODE : ", current_node)
    for node in net_maze.nodes:
        if node['id'] == current_node:
            node['color'] = 'lightgreen'

# # # SAVE HTML # # #

file_name = 'asteroids.html'
net_maze.save_graph(file_name)
fix_pyvis_header(file_name)
net_maze.show(file_name, notebook=False)