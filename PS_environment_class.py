# ENVIRONMENT CLASS
from problemSolvingAgentClass import ProblemSolvingAgent, UCS_program
from river_art import create_river

class PS_Environment:
    def __init__(self, problem):

        self.agents = []
        self.problem = problem

    def percept(self, agent):
        #Return the percept that the agent sees at this point. (Implement this in derived classes)
        return agent.location

    def execute_action(self, agent, action):
        #Change the world to reflect this action. (Implement this in derived classes)
        agent.location = action

    def default_location(self, thing):
        #Default location to place a new thing with unspecified location.
        return None

    def is_done(self):
        #By default, we're done when we can't find a live agent.
        return not any(agent.alive for agent in self.agents)

    def step(self): # implementation should be in spec. env. for problem Solving Agents
        # Run the environment for one time step.
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    percept = self.percept(agent)
                    action = agent.program(agent, percept)
                    print(f"Agent percepted being in state : {percept}")
                    print(f"Agent decided to go to state : {action}")
                    actions.append(action)
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
        else:
            print("There is no one here who could work...")

    def run(self, steps=10):
            # Agent finds solution
            for agent in self.agents:
                if agent.solution == [] :
                    agent.create_program()
                    agent.search(self.problem)
            #Run the Environment for given number of time steps.
            for step in range(steps):
                river = create_river(self.agents[0].location)
                for row in river : print(row)
                if self.is_done():
                    return
                print("step {0}:".format(step+1))
                self.step()

    def add_agent(self, agent, location=None):
        if agent in self.agents:
            print("Can't add the same agent twice")
        else:
            if isinstance(agent, ProblemSolvingAgent):
                self.agents.append(agent)