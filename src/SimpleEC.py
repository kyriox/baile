import numpy as np
import sympy as sp
import numpy.random as rnd
from sympy.combinatorics.graycode import GrayCode, gray_to_bin
from sklearn.preprocessing import normalize
from src.operators import *


#def undx()


class Chromosome:
    def __init__(self, code, fit=None, nfit=None, prob=None):
        self.code=code #genotipo
        self.fit=fit # fitness
        self.nfit=nfit # fitness normalizado
        self.prob=prob # probabilidad
    def __str__(self):
        stcode='|'.join([str(x) for x in self.code])
        return f"Genotype: {stcode} Fitness: {self.fit} Probability: {self.prob}"


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
            else:
                self.codes_size=self.code_size
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
        self.population=np.array(population)
        self._norm_fitness()


    def _norm_fitness(self):
        datax=np.array([gn.fit for gn in self.population])
        datax=np.nan_to_num(datax,nan=1e-6)
        self.fit=datax
        data=(datax - np.min(datax)) / (np.max(datax) - np.min(datax))
        self.prob=data/np.sum(data)
        for gn,v,p in zip(self.population,data,self.prob):
            gn.nfit,gn.prob=v,p
        idx=np.argsort(self.prob)[::-1][:len(self.prob)]
        self.fit=self.fit[idx]
        self.prob=self.prob[idx]
        self.population=self.population[idx]
        

    def _fitness(self, code):
        if self.coding=='g':
            optv=self.f(*[self._gray_to_real(x,bounds) for x,bounds in zip(code,self.bounds)], **self.kwargs)
        elif self.coding=='b':
            optv=self.f(*[self._bin_to_real(x,bounds) for x,bounds in zip(code,self.bounds)], **self.kwargs)
        else:
            #print(code)
            optv=self.f(*code,**self.kwargs)
        return optv*self.opt
    

    def _offspring(self, l=100):
        childs=[0 for i in range(l)]
        kwargs=dict(population=self.population,prob=self.prob,
                    sample_size=self.np)
        for i in range(l):
            parents=self._get_parents(**kwargs) # quienes se reproduces
            code=self._crossover(parents)
            childs[i]=Chromosome(code,fit=self._fitness(code))
        self.population=np.append(self.population,childs)
        self._norm_fitness()
        kwargs['sample_size']=self.population_size
        kwargs['prob']=self.prob
        kwargs['population']=self.population
        self.population=np.array(self._selection(**kwargs)) # quienes sobreviven
        self._norm_fitness()


    def evolve(self, t=100):
        avg,best=[],[]
        for gen in range(t):
            fs=np.sort(-self.fit)
            avg.append(np.mean(-self.fit))
            best.append(fs[0])
            self._offspring()
        return avg, best
    
    def EC(self,f=0.5,cr=0.1,t=10):
        for g in range(t):
            p=[]
            for i,x in enumerate(self.population):
                N=self.population_size
                c=rnd.permutation([j for j in range(N) if j!=i])
                x1,x2,x3=self.population[c[:3]]
                u=x1.code+f*(x2.code-x3.code)
                v=np.zeros(len(x.code))
                for k in range(len(x.code)): 
                    if rnd.random()>cr:
                        v[k]=x.code[k]
                    else:
                        v[k]=u[k]
                if self.f(*x.code)<self.f(*v):
                     p.append(x)
                else:
                     p.append(Chromosome(code=v))
            self.population=np.array(p)
     
    def __init__(self,f,bounds, population_size=100, code_size=10, np=2,
                 parents_selection=random_selection, crossover=uniform_crossover,
                 mutation=None,selection=proportional_selection,coding='g', opt=-1,**kwargs):
        self.f=f
        self.n=len(bounds)
        self.bounds=bounds
        self.code_size=code_size
        self.coding=coding
        self.population_size=population_size
        self.opt=opt
        self._crossover=crossover
        self._selection=selection
        self._get_parents=parents_selection
        self.np=np
        self.kwargs=kwargs
        self._initialize_population()
        
def eggholder(x1,x2):
  return -(x2+47)*np.sin(np.sqrt(np.abs(x2+x1/2+47)))-x1*np.sin(np.sqrt(np.abs(x1-(x2+47))))
        
if __name__=='__main__':
    ec=SimpleEC(eggholder, [(-512,512), (-512,512)], code_size=10, coding='g')
    ec.evolve(100)
    
    
