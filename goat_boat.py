# Goat in a Boat

from graphProblemClass import GraphProblem
from problemSolvingAgentClass import ProblemSolvingAgent, UCS_program
from PS_environment_class import PS_Environment

# STATE SPACE

def rules_1(state):
    return 1

def rules_2():
    pass

def get_adj_states(state, rules):
    state_set = []
    for x in range(0,4):
        new_state = list(state)
        if (state[0] == 'L') and (state[x] == 'L') :
            new_state[0] = 'R'
            new_state[x] = 'R'
            new_state = ''.join(new_state)
            state_set.append((new_state,rules(new_state)))
        if (state[0] == 'R') and (state[x] == 'R') :
            new_state[0] = 'L'
            new_state[x] = 'L'
            new_state = ''.join(new_state)
            state_set.append((new_state,rules(new_state)))
    return state_set


def generate_states():
    options = ['L','R']
    state_list = []
    for o in options:
        str1 = o
        for o in options:
            str2 = str1 + o 
            for o in options:
                str3 = str2 + o
                for o in options:
                    str4 = str3 + o
                    state_list.append(str4)
    return state_list

def generate_states_with_levels():
    state_list = ['LLLL']


def create_graph_dict(state_list):
    graph_dict = {}
    for state in state_list:
        graph_dict[state] = get_adj_states(state, rules_1)
    return graph_dict
    
def get_dead_states(state_list):
    dead_states = []
    for state in state_list:
        if (state[1] == state[2]) and (state[0] != state[2]):
            dead_states.append(state)
        elif (state[2] == state[3]) and (state[0] != state[2]):
            dead_states.append(state)
    dead_states = list(set(dead_states))
    return dead_states

# # # MAIN # # #

def main():

    # STATE SPACE
    initial_state = 'LLLL'
    goal_state = 'RRRR'
    program = UCS_program
    state_list = generate_states() # State Space
    the_graph = create_graph_dict(state_list)
    dead_states = get_dead_states(state_list)

    # INITIALIZE ENVIRONMENT, AGENT, PROBLEM
    the_problem = GraphProblem(initial=initial_state, goal=goal_state, graph=the_graph, dead=dead_states)
    the_agent = ProblemSolvingAgent(initial_state, goal_state, program)
    the_env = PS_Environment(the_problem)
    the_env.add_agent(the_agent)

    # RUN
    the_env.run()

main()
