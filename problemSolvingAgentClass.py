'''

Welcome to GDB Online.
GDB online is an online compiler and debugger tool for C, C++, Python, Java, PHP, Ruby, Perl,
C#, OCaml, VB, Swift, Pascal, Fortran, Haskell, Objective-C, Assembly, HTML, CSS, JS, SQLite, Prolog.
Code, Compile, Run and Debug online from anywhere in world.

'''

def sort_frontier(frontier):
    return sorted(frontier, key = lambda x : x[1])
    
def get_path(path, node):
    new_path = []
    for item in path:
        new_path.append(item)
    new_path.append(node)
    return new_path

def UCS_program(problem):

      graph = problem.graph
      start = problem.initial
      goal = problem.goal
      dead = problem.dead_states

      frontier = [ (start, 0, [] ) ] # priority queue
      reached = { } # reached dictionary
      
      while len(frontier) > 0 :
            
            # DEBUG print
            print(f"Frontier : {frontier}")
            print(f"Reached : {reached}")
            
            # Get Frontier Node Info
            node = frontier.pop(0)
            name = node[0]
            cost = node[1]
            path = node[2]
            print(f"Current Node : {node}")
            
            # Expand Node
            for neighbor in graph[name]:
                  # Get Neighbors
                  neighbor_name = neighbor[0]
                  neighbor_cost = cost + neighbor[1]
                  neighbor_path = get_path(path,name)
                  
                  if (neighbor_name not in reached) and (neighbor_name not in dead):
                        frontier.append((neighbor_name,neighbor_cost,neighbor_path))
                        print(f"Neighbor ({neighbor}) added to Frontier")
                  else :
                        print(f"Neighbor ({neighbor}) ignored.")

            # Compare Node to Reached & Update Reached
            if name in reached:
                  reached_cost = reached[name][0]
                  if cost < reached_cost :
                        reached[name] = (cost,path)
                        print(f"Reached Updated")
                  else:
                        print(f"Reached NOT updated")
            else :
                  reached[name] = (cost,path)
                  print(f"Reached Updated")
            
            # Check if Goal is reached and optimized    
            if goal in reached:
                  print(f"Goal Reached, culling frontier...")
                  goal_cost = reached[goal][0]
                  for N in frontier:
                        node_cost = N[1]
                        if node_cost > goal_cost :
                              frontier.remove(N)
                        
            # Update Priority Queue
            frontier = sort_frontier(frontier)
            print("Frontier Sorted")
            print("")

      cost, path = reached[goal]
      print(f"The Goal's Optimized Path is : {path}")
      print(f"The Cost of this path is : {cost}")
      print("")
      return reached[goal] # ( cost, path )   
        

class ProblemSolvingAgent():

      def __init__(self, initial_state, goal_state, solving_program):

            """State is an abstract representation of the state
            of the world, and seq is the list of actions required
            to get to a particular state from the initial state(root)."""

            self.initial_state = initial_state
            self.solution = [] 
            self.solution_path = None
            self.solution_cost = None
            self.solution_index = 0
            self.alive = True
            self.goal_state = goal_state
            self.location = None
            self.program = None
            self.solving_program = solving_program
            self.location = initial_state
            self.debug = False

      def run(self):
            pass



      # def __call__(self, percept, curGoal=None):
      #       """Formulate a goal and problem, then
      #       search for a sequence of actions to solve it."""
      #       #4-phase problem-solving process
      #       temp=self.state
      #       self.state = self.update_state(self.state, percept)
            
      #       if not self.seq:
      #             goal = self.formulate_goal(self.state)
                  
      #             if isinstance(goal, list) and len(goal)>1:
      #                   percept=self.state                         
      #                   while len(self.goal)>0:
      #                         #4-phase problem-solving process
      #                         self.state = self.update_state(self.state, percept)
      #                         current_goal=self.goal[0]
      #                         goal = current_goal
      #                         problem = self.formulate_problem(self.state, goal)
      #                         self.seq.extend (self.search(problem))
      #                         percept=current_goal
      #                         self.goal.remove(goal)
      #                   self.state = temp
      #             else:
      #                   problem = self.formulate_problem(self.state, goal)
      #                   self.seq = self.search(problem)                 
                        
                        
                              
      #             if not self.seq:
      #                   return None
      #       else:
      #             print("I have already don my work. Find someone else")
                  
      #       #return self.seq.pop(0)
      #       return None

      def update_state(self, state, percept):
            raise NotImplementedError
  
      def search(self, problem):
            solution = self.solving_program(problem)
            solution[1].append(self.goal_state)
            solution[1].pop(0)
            self.solution = solution[1]
            self.solution_path = solution[1]
            self.solution_cost = solution[0]

      def create_program(self):
            
            def program(self, percept):
                  # ignore percept
                  action = self.solution[self.solution_index]
                  self.solution_index += 1
                  if self.solution_index >= len(self.solution):
                        self.alive = False
                  return action

            self.program = program

'''

      def actions_path(self, p):
            acts=[]
            for n in p:
                  acts.append(n.action)
            return acts[1:]
'''