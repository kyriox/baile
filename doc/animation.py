import sys,os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

baile_path=os.path.abspath(os.path.join("..","src"))
test_path=os.path.abspath(os.path.join("..","test"))
if not baile_path in sys.path:
    sys.path.append(baile_path)
if not test_path in sys.path:
    sys.path.append(test_path)
import SimpleSearch as ss
from test_simple_search import successor8Puzzle,goal8Puzzle

class puzzle8Anim:
    
    def __init__(self,ax):
        self.ax=ax
    
    def update(self,step):
        self.ax.clear()
        self.ax.set_ylim(0,1)
        self.ax.set_xlim(0,1)
        #self.ax.set_aspect(1)
        print(step)
        st=step[0]
        n=len(st)
        par = dict(boxstyle='round', facecolor='silver', alpha=1,pad=0.35)
        impar = dict(boxstyle='round', facecolor='tomato', alpha=1,pad=0.35)
        macro=np.zeros((n,n))
        for j in range(n):
            for i in range(n):
                bc =  st[j][i]%2 and par or impar 
                if st[j][i]!=0:
                     self.ax.text(i/4+0.1,0.78-j/3, " %s " %st[j][i],bbox=bc,fontsize=40,color='white')
        self.ax.set_yticks([])
        self.ax.set_xticks([])
        #print(self.ax.get_ylim(), self.ax.get_xlim())
        
        return self.ax.plot([],[])


start=ss.node(((1,8,4),(3,0,2),(6,5,7)),op="start")
final=ss.node(((1,2,3),(4,5,6),(7,8,0)),op="final")

bfs=ss.BlindSearch(start,successor8Puzzle,goal8Puzzle,goal_state=final,strategy="bfs")
result=bfs.find(max_iter=500000)

steps=result.getPath()


fig, ax = plt.subplots()
#ax.set_ylim(0,3)
#ax.set_xlim(0,3)
anim = puzzle8Anim(ax)

stepsr=steps[:]
stepsr.reverse()
print(steps)


ani = FuncAnimation(fig, anim.update, steps+stepsr,interval=1500)

#pause
ani.event_source.stop()

#unpause
ani.event_source.start()
plt.show()
