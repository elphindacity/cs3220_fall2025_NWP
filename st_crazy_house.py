from environmentClass import Environment
from agentClass import Agent
from random import randint, choice
from thingClass import Thing
import os
import streamlit as st

def clear():
    os.system('cls')

def CatAgentProgram(percept):
    # percept = ( agent.location, status[agent.location] )
    location, status = percept
    action = rule_match(location, status)
    return action

def rule_match(location, status):
    actionList = ['MoveRight', 'MoveLeft']
    # Location Modifiers
    if location == 0 : actionList.remove('MoveLeft')
    elif location == 4 : actionList.remove('MoveRight')
    # Status modifiers
    try:
        if "Mouse" in status:
            actionList.append("Eat")
        elif "Milk" in status:
            actionList.append("Drink")
        elif "Dog" in status:
            actionList.append("Fight")
    except:
        st.write("Rule Match Error")
    return choice(actionList)
    
def SimpleReflexAgent(program, name):
    return Agent(program, name)

class CrazyHouseEnvironment(Environment):

    def __init__(self):
        super().__init__()

        self.agents = []

        self.status = [[None],[None],[None],[None],[None]]

        self.mouse_run = False 
        self.mouse_drink = False

    def percept(self, agent):
        # Returns the agent's location, and the location status..
        return agent.location, self.status[agent.location]
    
    def is_agent_alive(self, agent):
        return agent.alive

    def update_agent_alive(self, agent):
        st.write(f"{agent} Performance : {agent.performance}")
        if agent.performance <= 0:
            agent.alive = False
            st.write(f"{agent} is dead.")

    def is_done(self):
        # By default, we're done when we can't find a live agent.
        return not any(agent.is_alive() for agent in self.agents)
    
    def step(self):
        #Run the environment for one time step.
        actions = []
        if not self.is_done():
            for agent in self.agents:
                if agent.alive:
                    percept = self.percept(agent)
                    st.write(f"Agent percepted {percept}.")
                    action = agent.program(percept)
                    st.write("Agent decided to do {}.".format(action))
                    actions.append(action)
                else:
                    st.write("Agent {} is dead.".format(agent))
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
        else:
            st.write("There is no one here who could work...")
        return actions

    def run(self, steps=10):
        #Run the Environment for given number of time steps.
        for step in range(steps):
            if self.is_done():
                st.write("We can't find a live agent")
                return
            st.write("_____")
            st.write(f"*** Crazy House Step {step+1} ***")
            self.display()
            self.mouse_behaviour()
            self.step()

    def mouse_behaviour(self):
        if self.mouse_run :
            st.write("Mouse ran from dog!")
            self.mouse_run = False
        if self.mouse_drink :
            st.write("Mouse drank the milk!")
            self.mouse_drink = False

    def add_thing(self, thing, location=None):
        #from agentClass import Agent
        if thing in self.agents:
            st.write("Can't add the same agent twice")
        else:
            if isinstance(thing, Agent):
                thing.location = location if location is not None else self.default_location(thing)
                self.agents.append(thing)
            else :
                location = self.default_location(thing)
                if self.status[location][0] == None :
                    self.status[location][0] = thing.name
                else :
                    self.status[location].append(thing.name)

    def delete_thing(self, thing):
        if thing in self.agents:
            self.agents.remove(thing)

    def execute_action(self, agent, action):
        #Check if agent alive, if so, execute action
        if self.is_agent_alive(agent):
            # Change agent's location and/or location's status;
            # Track performance.
            if action == 'MoveRight':
                st.write("Cat moves right.")
                agent.location += 1
                agent.performance -= 1
            elif action == 'MoveLeft':
                st.write("Cat moves left.")
                agent.location -= 1
                agent.performance -= 1
            elif action == 'Eat':
                if agent.performance >= 3 :
                    st.write("Cat eats mouse.")
                    agent.performance += 10
                    self.status[agent.location].remove('Mouse')
                    if len(self.status[agent.location]) == 0 : 
                        self.status[agent.location].append(None)
                else :
                    st.write("Mouse evades cat.")
                    agent.performance -= 1
            elif action == 'Drink':
                agent.performance += 10
                self.status[agent.location].remove('Milk')
                if len(self.status[agent.location]) == 0 : 
                        self.status[agent.location].append(None)
            elif action == 'Fight':
                if agent.performance >= 10 :
                    st.write("Cat fights dog and wins!")
                    agent.performance += 20
                else :
                    st.write("Cat fights dog and loses!")
                    agent.performance -= 10
            self.update_agent_alive(agent)

    def default_location(self, thing):
        # Agents start in either location at random.
        location = randint(0,4)
        #st.write(f"{thing} is starting in random room : {location}")
        return location
    
    def display(self):
        for x in range(len(self.status)):
            string = f"--- Room {x} : [ "
            for agent in self.agents:
                if agent.location == x:
                    string += agent.name
                    string += ", "
            for item in self.status[x]:
                string += str(item)
                string += ", "
            string = string[:-2]
            string += " ]"
            if "Mouse" in string : 
                string = string.replace("None, ", "")
            if "Cat" in string :
                string = string.replace(", None","")
            st.write(string)
        

    def display_trash(self):
        st.write("")
        # ROOM NUMBER
        str1 = ""
        for x in range(len(self.status)):
            str1 += (f"   {x}   ")
        st.write(str1)
        st.write("")
        # TOP
        str2 = ""
        for x in range(len(self.status)):
            str2 += (f"._____.")
        st.write(str2)
        # CAT
        str3 = ""
        for x in range(len(self.status)):
            if self.agents[0].location == x : c = "Cat"
            else : c = "..."
            str3 += (f"|.{c}.|")
        st.write(str3)
        # STATUS
        str4 = ""
        for x in range(len(self.status)):
            if self.status[x][0] == None : s = "....."
            else : s = self.status[x][0].ljust(5)
            str4 += (f"|{s}|")
        st.write(str4)
        # STATUS 2
        str5 = ""
        for x in range(len(self.status)):
            if len(self.status[x]) > 1 :
                s = self.status[x][1].ljust(5)
            else : 
                s = "....."
            str5 += (f"|{s}|")
        st.write(str5)
        # BOTTOM
        str6 = ""
        for x in range(len(self.status)):
            str6 += (f"|.....|")
        st.write(str6)
        st.write("")

    def correct_things(self):
        x = 0
        for location in self.status:
            if "Mouse" in location and "Dog" in location:
                location.remove("Mouse")
                if x == 0 : self.status[1].append("Mouse")
                elif x == 4 : self.status[3].append("Mouse")
                else :
                    n = choice([-1,+1])
                    self.status[x + n].append("Mouse")
                self.mouse_run = True
            x += 1
        for location in self.status:
            if "Mouse" in location and "Milk" in location:
                location.remove("Milk") 
                self.mouse_drink = True
            
def main():
    clear()
    TheCat = SimpleReflexAgent(CatAgentProgram, "Cat")
    TheCat.performance += 5
    TheMilk = Thing('Milk')
    TheDog = Thing('Dog')
    TheMouse = Thing('Mouse')
    CrazyHouse = CrazyHouseEnvironment()
    CrazyHouse.add_thing(TheCat)
    CrazyHouse.add_thing(TheMilk)
    CrazyHouse.add_thing(TheDog)
    CrazyHouse.add_thing(TheMouse)
    CrazyHouse.correct_things()
    CrazyHouse.run()

if __name__ == '__main__' :
    main()