import numpy.random as rnd
import numpy as np

def proportional_selection(**kwargs):
    population=kwargs['population'] # poblacion completa
    k=kwargs['sample_size'] # numero de elementos a seleccionar
    prob=kwargs['prob'] # pobabilidad de cada elemento
    return [population[i] for i in [rnd.choice(len(population), p=prob) for i in range(k)]]

def random_selection(**kwargs):
    population=kwargs['population']
    k=kwargs['sample_size']
    return [population[i] for i in [rnd.choice(len(population)) for i in range(k)]]

def uniform_crossover(parents):
    p1,p2=parents
    h1=["".join([rnd.rand()>0.5 and x1[i] or x2[i] for  i in range(len(x1))]) 
        for x1,x2 in (p1.code,p2.code)]
    return h1

def undx(parents):
    n=len(parents) # Numero de padres
    p=np.array([x.code for x in parents[:-1]]) # n-1 para sacar la media
    r=parents[-1].code
    xm=np.mean(p, axis=0)
    d=p-xm
    dn=np.linalg.norm(d, axis=1).reshape(n-1,1)
    e=d/dn
    g=np.linalg.norm(r-xm)
    t1=1/(n-2)
    t2=0.35**2/n
    h=np.array([xm+np.sum(rnd.normal(0,t1,n-1).reshape(n-1,1)*d + 
                rnd.normal(0,t2,n-1).reshape(n-1,1)*g*e, axis=0)/(n-1) 
                for i in range(1)])
    return h[0]
