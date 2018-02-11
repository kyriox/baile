import numpy as np
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
    
    def __lt__(self, n):
        return  self.cost<n.cost

# Class for performing blin search

class BlindSearch:
   # def bfs(frontier,successors):
   #     for s in successors:
   #         frontier.insert(0,s)
            
    #def dfs(frontier,successors):
    #    for s in successors:
    #        frontier.append(s)
    
    #succesors=[x for x in self.successor(cs) if x.state not in self.visited]
    #        if succesors:
    #            [self.visited.add(x.state) for x in succesors] #extra work, but useful
    #            self.add(self.frontier,succesors)
    
    def pop(self):
        if self.strategy=="a*":
            return heapq.heappop(self.frontier)
        else:
            self.frontier.pop()
    
    def bfs(self,cs):
        successors=[x for x in self.successor(cs) if x.state not in self.visited]
        if successors:
            [self.visited.add(x.state) for x in successors] #extra work, but useful
        for s in successors:
                self.frontier.insert(0,s)
    
    def dfs(self,cs):
        successors=[x for x in self.successor(cs) if x.state not in self.visited]
        if successors:
            [self.visited.add(x.state) for x in successors] #extra work, but useful
        for s in successors:
                self.frontier.append(s)
    
    def astar(self,cs):
        successors=[x for x in self.successor(cs) if x.state not in self.visited]
        if successors:
            [self.visited.add(x.state) for x in successors] #extra work, but useful
        for s in successors:
                s.cost=self.heuristic(s,self.goal_state)
                heapq.heappush(self.frontier, s)
        #self.frontier.append(s)
        #self.frontier.sort(key= lambda x: x.cost)
    
    #def dfs(self,successors):
    #    for s in successors:
    #            self.frontier.append(s)
    
    #def astar(self,succesors):
        
            
    #def dfs(frontier,successors):
    #    for s in successors:
    #        frontier.append(s)
            
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

        
            
        
        

    
    
            
            
        
        
        
