def get_adj_states(state, rules, dead_states):
    state_dict = {}
    for x in range(0,4):
        new_state = list(state)
        if (state[0] == 'L') and (state[x] == 'L') :
            new_state[0] = 'R'
            new_state[x] = 'R'
            new_state = ''.join(new_state)
            state_dict[new_state] = rules(new_state, dead_states)
        if (state[0] == 'R') and (state[x] == 'R') :
            new_state[0] = 'L'
            new_state[x] = 'L'
            new_state = ''.join(new_state)
            state_dict[new_state] = rules(new_state, dead_states)
    return state_dict

def get_actions(state):
    action_dict = {}
    for x in range(0,4):
        new_state = list(state)
        action = "Boat"
        if (state[0] == 'L') and (state[x] == 'L') :
            action += " Right"
            new_state[0] = 'R'
            if state[x] == 'L' and x != 0:
                if x == 1 : action += " with Wolf"
                elif x == 2 : action += " with Goat"
                elif x == 3 : action += " with Cabbage"
            new_state[x] = 'R'
            new_state = ''.join(new_state)
            action_dict[action] = new_state
        if (state[0] == 'R') and (state[x] == 'R') :
            action += " Left"
            new_state[0] = 'L'
            if state[x] == 'R' and x != 0:
                if x == 1 : action += " with Wolf"
                elif x == 2 : action += " with Goat"
                elif x == 3 : action += " with Cabbage"
            new_state[x] = 'L'
            new_state = ''.join(new_state)
            action_dict[action] = new_state
    return action_dict

def get_actions2(state):
    action_dict = {}
    for x in range(0,4):
        new_state = list(state)
        action = "Boat"
        if (state[0] == 'L') and (state[x] == 'L') :
            action += " Right"
            new_state[0] = 'R'
            if state[x] == 'L' and x != 0:
                if x == 1 : action += " with Wolf"
                elif x == 2 : action += " with Goat"
                elif x == 3 : action += " with Cabbage"
            new_state[x] = 'R'
            new_state = ''.join(new_state)
            action_dict[new_state] = action
        if (state[0] == 'R') and (state[x] == 'R') :
            action += " Left"
            new_state[0] = 'L'
            if state[x] == 'R' and x != 0:
                if x == 1 : action += " with Wolf"
                elif x == 2 : action += " with Goat"
                elif x == 3 : action += " with Cabbage"
            new_state[x] = 'L'
            new_state = ''.join(new_state)
            action_dict[new_state] = action
    return action_dict

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

def create_graph_dict(state_list, dead_states):
    graph_dict = {}
    for state in state_list:
        graph_dict[state] = get_adj_states(state, rules_1, dead_states)
    return graph_dict

def create_graph_dict2(state_list):
    graph_dict = {}
    for state in state_list:
        graph_dict[state] = get_actions(state)
    return graph_dict

def create_graph_dict3(state_list):
    graph_dict = {}
    for state in state_list:
        graph_dict[state] = get_actions2(state)
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

def rules_1(state, dead_states):
    infinity = float('inf')
    if state in dead_states:
        return infinity
    else : 
        return 1

    
def print_dict(dict):
    for key, val in dict.items():
        print(f"{key} : {val}")
    print("")

state_list = generate_states()
dead_states = get_dead_states(state_list)
my_data = create_graph_dict(state_list, dead_states)
my_data2 = create_graph_dict2(state_list)
my_data3 = create_graph_dict3(state_list)

print_dict(my_data3)




