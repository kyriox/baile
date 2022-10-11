import numpy as np
import sympy as sp
import numpy.random as rnd
from sympy.combinatorics.graycode import GrayCode, gray_to_bin
from sklearn.preprocessing import normalize


def proportional_selection(population,prob,k):
    return [population[i] for i in [rnd.choice(len(population), p=prob) for i in range(k)]]

def random_selection(population,k):
    return [population[i] for i in [rnd.choice(len(population)) for i in range(k)]]

def uniform_crossover(parents):
    p1,p2=parents
    h1=["".join([rnd.rand()>0.5 and x1[i] or x2[i] for  i in range(len(x1))]) 
        for x1,x2 in (p1.code,p2.code)]
    return h1


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


    def _norm_fitness(self):
        datax=np.array([gn.fit for gn in self.population])
        datax=np.nan_to_num(datax,nan=1e-6)
        self.fit=datax
        #print("----------------",data)
        data=(datax - np.min(datax)) / (np.max(datax) - np.min(datax))
        prob=data/np.sum(data)
        self.prob=prob
        #r=np.argwhere(np.isnan(prob))
        #if len(r):
        #    i=r[0,0]
        #    print(data[i],datax[i],np.min(datax),np.max(datax))
        for gn,v,p in zip(self.population,data,self.prob):
            gn.nfit,gn.prob=v,p

    def _fitness(self, code):
        if self.coding=='g':
            optv=self.f(*[self._gray_to_real(x,bounds) for x,bounds in zip(code,self.bounds)])
        elif self.coding=='b':
            optv=self.f(*[self._bin_to_real(x,bounds) for x,bounds in zip(code,self.bounds)])
        else:
            optv=self.f(*code)
        return optv*self.opt
    

    def _offspring(self, l=50):
        childs=[0 for i in range(l)]
        for i in range(l):
            parents=self._get_parents(self.population,self.prob,self.np)
            code=self._crossover(parents)
            childs[i]=Chromosome(code,fit=self._fitness(code))
        self.population+=childs
        self._norm_fitness()
        self.population=self._selection(self.population,self.prob,self.population_size)
        self._norm_fitness()

    def evolve(self, t=100):
        avg,best=[],[]
        for gen in range(t):
            fs=np.sort(-self.fit)
            avg.append(np.mean(-self.fit))
            best.append(fs[0])
            self._offspring()
        return avg, best

    def __init__(self,f,bounds, population_size=100, code_size=10, np=2,
                 parents_selection=random_selection, crossover=uniform_crossover,
                 mutation=None,selection=proportional_selection,coding='g', opt=-1):
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
        self._initialize_population()
        
def eggholder(x1,x2):
  return -(x2+47)*np.sin(np.sqrt(np.abs(x2+x1/2+47)))-x1*np.sin(np.sqrt(np.abs(x1-(x2+47))))
        
if __name__=='__main__':
    ec=SimpleEC(eggholder, [(-512,512), (-512,512)], code_size=10, coding='g')
    ec.evolve(100)
    
    
