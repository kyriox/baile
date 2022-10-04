import numpy as np
import sympy as sp
import numpy.random as rnd
from sympy.combinatorics.graycode import GrayCode, gray_to_bin
from sklearn.preprocessing import normalize


class Chromosome:
    def __init__(self, code, fit=None, nfit=None, prob=None):
        self.code=code
        self.fit=fit
        self.nfit=nfit
        self.prob=prob
    def __str__(self):
        return f"Genotype: {self.code} Fitness: {self.fit} Probability: {self.prob}"


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
        xmin,xmax=self.bounds[0]
        if self.coding in ['g','b']:
            if type(self.code_size)==int:
                self.codes_size=[self.code_size for s in  range(len(self.bounds))]
            self.c_size=sum(self.codes_size)
            csize=self.codes_size[0]
            population=np.array([''.join([str(i) for i in rnd.randint(0,2,csize)])
                                 for i in range(self.population_size)]).reshape(-1,1)
            for csize in self.codes_size[1:]:
                codes=np.array([''.join([str(i) for i in rnd.randint(0,2,csize)])
                                for i in range(self.population_size)]).reshape(-1,1)
                population=np.hstack((population,codes))
        else:
            population=xmin + (xmax-xmin)*rnd.rand(self.population_size).reshape(-1,1)
            for xmin,xmax in self.bounds[1:]:
                codes=xmin + (xmax-xmin)*rnd.rand(self.population_size).reshape(-1,1)
                population=np.hstack((population,codes))
        population=[Chromosome(code,self._fitness(code)) for code in population]
        self.population=population
        self._norm_fitness()

    
    def __init__(self,f,bounds, population_size=100, code_size=10, coding='g', opt=-1):
        self.f=f
        self.n=len(bounds)
        self.bounds=bounds
        self.code_size=code_size
        self.coding=coding
        self.population_size=population_size
        self.opt=opt
        self._initialize_population()

    def _norm_fitness(self):
        data=np.array([gn.fit for gn in self.population])
        self.fit=data
        data=(data - np.min(data)) / (np.max(data) - np.min(data))
        prob=data/np.sum(data)
        self.prob=prob
        for gn,v,p in zip(self.population,data,prob):
            gn.nfit,gn.prob=v,p

    def _fitness(self, code):
        if self.coding=='g':
            optv=self.f(*[self._gray_to_real(x,bounds) for x,bounds in zip(code,self.bounds)])
        elif self.coding=='b':
            optv=self.f(*[self._bin_to_real(x,bounds) for x,bounds in zip(code,self.bounds)])
        else:
            optv=self.f(*code)
        return optv
    
    def _proportional_selection(self, k=0):
        if not k:
            k=self.population_size
        return [self.population[i] for i in [rnd.choice(len(self.population), p=self.prob) for i in range(k)]]

    def _uniform_crossover(self,p1,p2):
        h1=["".join([rnd.rand()>0.5 and x1[i] or x2[i] for  i in range(len(x1))]) for x1,x2 in (p1.code,p2.code)]
        return h1
    
    def _offspring(self, l=50):
        childs=[0 for i in range(l)]
        for i in range(l):
            x1,x2=self._proportional_selection(k=2)
            code=self._uniform_crossover(x1,x2)
            childs[i]=Chromosome(code,fit=self._fitness(code))
        self.population+=childs
        self._norm_fitness()
        self.population=self._proportional_selection()
        self._norm_fitness()

    def evolve(self, t=100):
        avg,best=[],[]
        for gen in range(t):
            fs=np.sort(-self.fit)
            avg.append(np.mean(-self.fit))
            best.append(fs[0])
            self._offspring(100)
        return avg, best
        
def eggholder(x1,x2):
  return -(x2+47)*np.sin(np.sqrt(np.abs(x2+x1/2+47)))-x1*np.sin(np.sqrt(np.abs(x1-(x2+47))))
        
if __name__=='__main__':
    ec=SimpleEC(eggholder, [(-512,512), (-512,512)], code_size=10, coding='g')
    ec.evolve(100)
    
    
