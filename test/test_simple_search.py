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

import sys,os
baile_path=os.path.abspath(os.path.join("..","src"))
if not baile_path in sys.path:
    sys.path.append(baile_path)
import SimpleSearch as ss
import unittest

def successor8Puzzle(a):
    board=a.state # current state
     #find the 0
    i,j=[(i,j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j]==0][0]
        # postions
    left,right=(i,j-1,"left"),(i,j+1,"right")
    up,down=(i+1,j,"down"),(i-1,j,"up")
    successors=[]
    for x,y,op in [up,down,left,right]: 
        if  0<=y<len(board[0]) and 0<=x<len(board): # test for boundaries
            nboard=[list(bx[:]) for bx in board] # make a copy
            nboard[x][y],nboard[i][j]=board[i][j],board[x][y] # swap 
            nboard=tuple([tuple(row) for row in nboard]) # make inmutable
            successors.append(ss.node(nboard,op=op,depth=a.depth+1,parent=a))# create a node
    return successors # list of successors

def goal8Puzzle(*states):  # goal8Puzzle(start,final)
    a=states[0] # start state is the firts argument
    b=states[1] # final state is the second...
    return a.state==b.state # test if a==b (returns a boolean)

def manhattan(*states):
    cs,gs=states[0].state,states[1].state
    cs_pos=[(cs[i][j],(i,j)) for i in range(len(cs)) for j in range(len(cs[0]))]
    gs_pos=[(gs[i][j],(i,j)) for i in range(len(gs)) for j in range(len(gs[0]))]
    cs_pos.sort(),gs_pos.sort()
    res=[abs(a[1][0]-b[1][0])+abs(a[1][1]-b[1][1]) for a,b in zip(cs_pos[1:],gs_pos[1:])] 
    return sum(res)

class EightPuzzle(unittest.TestCase):                  
    
    start=ss.node(((7,2,4),(5,0,6),(8,3,1)),op="start")
    final=ss.node(((0,1,2),(3,4,5),(6,7,8)),op="final")
    wrong_start=ss.node(((2,7,4),(5,0,6),(8,3,1)),op="wrong_start")
    not_found=ss.node('Solution not found', op="not_found")
    
    def test_eight_puzzle_bfs(self):    
       bfs=ss.BlindSearch(self.start,successor8Puzzle,goal8Puzzle,goal_state=self.final,strategy="bfs")
       result=bfs.find()
       self.assertTupleEqual(result.state, self.final.state)

    def test_eight_puzzle_dfs(self):    
       dfs=ss.BlindSearch(self.start,successor8Puzzle,goal8Puzzle,goal_state=self.final,strategy="dfs")
       result=dfs.find()
       self.assertTupleEqual(result.state, self.final.state)

    def test_eight_puzzle_astar(self):    
       ass=ss.BlindSearch(self.start,successor8Puzzle,goal8Puzzle,goal_state=self.final,strategy="a*",
                          heuristic=manhattan)
       result=ass.find()
       self.assertTupleEqual(result.state, self.final.state)

    def test_eight_puzzle_not_found(self):    
       bfs=ss.BlindSearch(self.wrong_start,successor8Puzzle,goal8Puzzle,goal_state=self.final,strategy="bfs")
       result=bfs.find(max_iter=1000)
       self.assertEqual(result.state, self.not_found.state)

    def test_path(self):    
       dfs=ss.BlindSearch(self.start,successor8Puzzle,goal8Puzzle,goal_state=self.final,strategy="dfs")
       result=dfs.find()
       root=result.getPath()[0]
       self.assertTupleEqual(root[0], self.start.state)


#

def countAttacks(*nodes):
    a=nodes[0]
    board=a.state
    fboard=[(i,j) for j,i in enumerate(board)]
    n=len(board)
    attacks=0
    for x in range(n-1):
        for y in range(x+1,n):
            il,jl=fboard[x]
            ir,jr=fboard[y]
            if il==ir:
                attacks+=1
            elif abs(ir-il)==abs(jr-jl):
                attacks+=1
    return attacks

def goalNQueens(*nodes):
    attacks=countAttacks(nodes[0])
    return attacks==0

def successorNQueens(a):
    board=a.state
    n,res=len(board),[]
    for i in range(n):
        if a.state[i]+1<n:
            t=list(a.state)
            t[i]=a.state[i]+1
            res.append(ss.node(tuple(t)))
    return res

class NQueens(unittest.TestCase):
    start=ss.node((0,0,0,0,0),op="start")

    def test_n_queens_bfs(self):    
       bfs=ss.BlindSearch(self.start,successorNQueens,goalNQueens,strategy="bfs")
       result=bfs.find()
       self.assertEqual(countAttacks(result),0)

    def test_n_queens_dfs(self): 
       dfs=ss.BlindSearch(self.start,successorNQueens,goalNQueens,strategy="dfs")
       result=dfs.find()
       self.assertEqual(countAttacks(result),0)   

    def test_n_queens_astar(self): 
       ass=ss.BlindSearch(self.start,successorNQueens,goalNQueens,strategy="a*",heuristic=countAttacks)
       result=ass.find()
       self.assertEqual(countAttacks(result),0)   
    

if __name__ == '__main__':
    unittest.main()
