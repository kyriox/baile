import numpy as np
class node:

    #Blind search node structure
    def  __init__(self, state, parent=None, depth=0, cost=0, op="",delta=0):
        self.state=state   # problem state (vector, value, string....)
        self.parent=parent # who generates this node?
        self.depth=depth   # its depth?
        self.cost=cost     # current cost
        self.delta=delta   # heuristic value
        self.op=op         # operation name which generated this node

    # setters an getters
    def getParent(self):
        return self.parent
    def getCost(self):
        return self.cost
    def getDepth(self):
        return self.depth
    def getOp(self):
        return self.op
    def setParent(self, parent):
        self.parent=parent
    def setCost(self, cost):
        self.cost=cost
    def setDepth(self, depth):
        self.depth=depth
    def setOp(self, op):
        self.op=op

    # Finding the followed route by iteratively looking at his parent
    def getPath(self):
        aux=self
        path=[]
        while aux!=None:
            path.insert(0,(aux.state,aux.op,aux.depth))
            aux=aux.parent
        return path

# Class for performing blin search

class BlindSearch:
    def bfs(frontier,successors):
        for s in successors:
            frontier.insert(0,s)
            
    def dfs(frontier,successors):
        for s in successors:
            frontier.append(s)
            
    strategies={"bfs":bfs,"dfs":dfs}
    
    def __init__(self,start,successor,goal,strategy="bfs",goal_state=None,add=None):
        self.start=start  # initial state
        self.goal=goal    # function to evaluated the goal
        self.successor=successor # fucntion to generated the succesors
        # function to update de frontier (this deifine the search type, defautl bfs)
        self.add=add
        if add==None:
            self.add=self.strategies[strategy]  # Search strategy (bfs or dfs)
        self.visited=set() # used to mark already visited states (ot avoid cycles)
        self.frontier=[] # list o pending nodes
        self.goal_state=goal_state # only necesary if we know the final state and we are looking for a step's squance

    def find(self, max_iter=1000000, debug=False): 
        i=0;
        cs=self.start
        self.frontier=[cs]
        self.visited=set([cs.state])
        while (not self.goal(cs,self.goal_state)) and len(self.frontier)>0 and i<max_iter:
            i+=1
            succesors=[x for x in self.successor(cs) if x.state not in self.visited]
            if succesors:
                [self.visited.add(x.state) for x in succesors] #extra work, but useful
                self.add(self.frontier,succesors)
            if i%1000==0 and debug:
                print("iteration: %s" %i)
                print("Is current state the goal?: %s" %self.goal(cs,self.goal_state))
                print(np.array(cs.state))
            cs=self.frontier.pop()
        print("finished in %s iterations" %i)
        if self.goal(cs,self.goal_state): 
            return cs
        else:
            return node("Solution not found")

        
            
        
        

    
    
            
            
        
        
        
