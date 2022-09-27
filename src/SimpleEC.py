import numpy as np
import sympy as sp
from sympy.combinatorics.graycode import GrayCode, gray_to_bin
from sklearn.preprocessing import normalize


class SimpleEC:
    def _bin_to_real(self,bcode,interval):
        xmin,xmax=interval
        n=len(bcode)
        s=np.sum([int(b)*2**(n-i-1) for i,b in enumerate(bcode)])
        return xmin+(xmax-xmin)/(2**n-1)*s

    def _gray_to_real(self,gcode,interval):
        bcode=gray_to_bin(gcode)
        return self._bin_to_real(bcode,interval)

    def _initialize_population(self):
        population=[]
        if type(self.code_size)==int:
            codes_size=[self.code_size for s in  range(len(self.bounds))]
        X=np.random.choice(list(GrayCode(codes_size[0]).generate_gray()),self.population_size)        
        for s in codes_size[1:]:
            xs=np.random.choice(list(GrayCode(s).generate_gray()),self.population_size)
            X=np.column_stack((X,xs))
        return X
    
    def __init__(self,f,bounds, population_size=100, code_size=10):
        self.n=len(bounds)
        self.bounds=bounds
        self.code_size=code_size
        self.population_size=population_size
        self.population=self._initialize_population()
        self.f=f

    def _evaluation(self,X):
        return self.f(*[self._gray_to_real(x,bounds) for x,bounds in zip(X,self.bounds)])

    def fitness(self):
        data=np.array([self._evaluation(x) for x in self.population])
        return (data - np.min(data)) / (np.max(data) - np.min(data))


def eggholder(x1,x2):
  return -(x2+47)*np.sin(np.sqrt(np.abs(x2+x1/2+47)))-x1*np.sin(np.sqrt(np.abs(x1-(x2+47))))
        
if __name__=='__main__':
    ec=SimpleEC(eggholder, [(-10,10), (-5,5)])
    print(ec.population[:3])
    print(ec.fitness())
    
