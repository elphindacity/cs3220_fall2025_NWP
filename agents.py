# IMPORT
from src.PS_agentPrograms import *

# # #

from src.problemSolvingAgentProgramClass import SimpleProblemSolvingAgentProgram
from src.mazeProblemClass import MazeProblem

class MazeProblemSolvingAgent(SimpleProblemSolvingAgentProgram):
  def __init__(self, initial_state=None, dataGraph=None, goal=None):
    super().__init__(initial_state)
    self.dataGraph=dataGraph
    self.goal=goal
    #instance of Maze ProblemClass
    #self.problem=problem #a description of the states and actions necessary to reach the goal
    #self.goal = self.problem.goal#The agent adopts the goal

  def update_state(self, state, percept):
    return percept

  def formulate_goal(self, state):
    if self.goal is not None:
      return self.goal
    else:
      print("No goal! can't work!")
      return None

  #a description of the states and actions necessary to reach the goal
  def formulate_problem(self, state, goal):
    #instance of Maze ProblemClass
    problem = MazeProblem(state,goal,self.dataGraph)
    return problem

  def search(self, problem):
    pass

# # #

class MazeProblemSolvingAgentSMART(MazeProblemSolvingAgent):
    def __init__(self, initial_state=None, dataGraph=None, goal=None, program=None):
        super().__init__(initial_state, dataGraph, goal)
        self.performance = len(dataGraph.nodes())

        if program is None or not callable(program):
            print("Can't find a valid program for {}, falling back to default.".format(self.__class__.__name__))

            def program(percept):
                return eval(input('Percept={}; action? '.format(percept)))

        self.program = program

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


def ProblemSolvingMazeAgentBFS(initState,mazeWorldGraph,goalState):
    return MazeProblemSolvingAgentSMART(initState,mazeWorldGraph,goalState,BestFirstSearchAgentProgram())