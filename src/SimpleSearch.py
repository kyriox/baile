# Copyright 2018 Jose Otiz-Bejar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import heapq

class node:
    #Blind search node structure
    def  __init__(self, state, parent=None, depth=0, cost=0, op="",delta=0):
        self.state=state   # problem state (vector, value, string....)
        self.parent=parent # who generates this node?
        self.depth=depth   # its depth?
        self.cost=cost     # current cost
        self.delta=delta   # heuristic value
        self.op=op         # operation name which generated this node


    # Finding the followed route by iteratively looking at his parent
    def getPath(self):
        aux=self
        path=[]
        while aux!=None:
            path.insert(0,(aux.state,aux.op,aux.depth))
            aux=aux.parent
        return path
    
    #Nodes are compared using itc cost (e.i. less cost goes first)
    def __lt__(self, n):
        return  self.cost<n.cost

# Class for performing blin search

class BlindSearch:
    
    def pop(self):
        if self.strategy=="a*":
            return heapq.heappop(self.frontier)
        else:
            return self.frontier.pop()
    
    def bfs(self,cs):
        successors=[x for x in self.successor(cs) if x.state not in self.visited]
        for s in successors:
                self.visited.add(s.state)
                self.frontier.insert(0,s)
    
    def dfs(self,cs):
        successors=[x for x in self.successor(cs) if x.state not in self.visited]
        for s in successors:
                self.visited.add(s.state)
                self.frontier.append(s)
    
    def astar(self,cs):
        successors=[x for x in self.successor(cs) if x.state not in self.visited]
        for s in successors:
                self.visited.add(s.state)
                s.cost=self.heuristic(s,self.goal_state)
                heapq.heappush(self.frontier, s)
            
    strategies={"bfs":bfs,"dfs":dfs,"a*":astar}
    
    def __init__(self,start,successor,goal,strategy="bfs",goal_state=None,heuristic=None):
        self.start=start  # initial state
        self.goal=goal    # function to evaluated the goal
        self.successor=successor # fucntion to generated the succesors
        self.strategy=strategy
        # function to update de frontier (this deifine the search type, defautl bfs)
        self.add=self.strategies[strategy]  # Search strategy (BFS, DFS or A*)
        self.visited=set() # used to mark already visited states (to avoid cycles)
        self.frontier=[] # list o pending nodes
        self.goal_state=goal_state # only necesary if we know the final state and we are looking for a step's sequence
        self.heuristic=heuristic

    def find(self, max_iter=1000000, debug=False): 
        i=0;
        current=self.start
        self.frontier=[current]
        self.visited=set([current.state])
        while (not self.goal(current,self.goal_state)) and len(self.frontier)>0 and i<max_iter:
            i+=1
            self.add(self,current)
            if i%1000==0 and debug:
                print("iteration: %s, node cost: %s" %(i,current.cost))
                print("Is current state the goal?: %s" %self.goal(current,self.goal_state))
                print(np.array(current.state))
            current=self.pop()
        print("finished in %s iterations" %i)
        if self.goal(current,self.goal_state): 
            return current
        else:
            return node("Solution not found")

        
            
        
        

    
    
            
            
        
        
        
