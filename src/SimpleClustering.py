import numpy as np
#from scipy.spatial.distance import cosine
from sklearn.cluster import KMeans as skmeans
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
from sklearn.decomposition import PCA
import pandas as pd
from matplotlib import transforms

#distancia euclideana
def euclidiana(x,y):
    m=x-y
    return np.sqrt(np.sum(m*m))

#distancia coseno
def coseno(x,y):
    dist=1.0 - np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
    # si los vectores ya están normalizados se podría utilizar la siguente linea
    #dist=1.0 - np.dot(x, y)
    return dist

# Función para graficar clusters en dos y tres dimensiones
def plotClusters(data,labels,centroids={},f="",centroids_txt_labels={}):
    fig=plt.figure(figsize=(6, 6))
    sbox = dict(boxstyle='round', facecolor='white', alpha=0.4)
    data=np.asarray(data)
    d=data.shape[1] # dimensión de los datos (número de columnas)
    if d==3:
        ax = fig.add_subplot(111, projection='3d')
    else:
        ax = fig.add_subplot(111)
    labels=np.asarray(labels)
    K=np.unique(labels)
    color_map=iter(cm.viridis(np.linspace(0,1,len(K))))
    for k in K:
        D=data[np.where(labels==k)]
        x,y=D[:,0],D[:,1]
        cl=next(color_map)
        if d==3:
            z=D[:,2]
            ax.scatter(x,y,z, color=cl,s=32)
        else:
            ax.scatter(x,y, color=cl,s=32)
        if len(centroids):
            txt_label=centroids_txt_labels and str(centroids_txt_labels[k]) or str(k)
            if len(centroids[k])==3:
                xc,yc,zc=centroids[k]
                ax.text(xc,yc,zc,txt_label,bbox=sbox,fontsize=14)
            else:
                xc,yc=centroids[k]
                ax.text(xc,yc,txt_label,bbox=sbox,fontsize=14)
    if d==3:
        ax.set_zticks([])
    ax.set_xticks([])
    ax.set_yticks([])
    if f:
        fig.savefig(f)

# Transformar datos N>3 dimensionales a 2 o tres dimensiones usando PCA                  
def plotPCA(data, labels, d=2,f="",centroids={},vectors=True):
    pca = PCA(n_components=d)
    pca.fit(data)
    X=pca.transform(data)
    origin2d=[0],[0]
    origin3d=[0],[0],[0]
    pca_centroids={}
    for k,c in centroids.items():
        pca_centroids[k]=pca.transform([centroids[k]])[0,:]
    plotClusters(X,labels,f=f,centroids=pca_centroids)
    if len(centroids)>0 and vectors:
        for k,c in pca_centroids.items():
            if d==2:
                plt.quiver(*origin2d, pca_centroids[k][0],pca_centroids[k][1],angles='xy',
                        scale_units='xy', scale=1, color='skyblue')
            else: 
                plt.quiver(*origin3d, pca_centroids[k][0],pca_centroids[k][1],pca_centroids[k][2],color='skyblue')

# Plantilla simple para implementar métodos de clustering
class Clustering:
    
    # Distancia de un elemento x a su centroide más cercano.
    # Devuelve la pareja (distancia, id_del_cluster)
    def _nearest_centroid(self,x):
        return min((self.distance_function(c,x),i)
                   for i,c in self.centroids_.items())

    ## Calcular SSE, se usa inertia igual que en la implementacion de sckit-learn
    ## SSE = suma de las distancias AL CUADRADO de cada elemento a su centroide MAS CERCANO
    def _inertia(self):
        self.inertia_=0
        for x in self.data:
            d,i=self._nearest_centroid(x) # el más cercano, no uno cualquiera
            self.inertia_+=d**2           # al cuadrado, como en la definición del SSE

    # asigna los elementos en la colección a su centroide más cercano
    # genera las etiquetas de los clusters
    def _assign_nearest_centroids(self):
         self.labels_=[-1 for x in self.data]
         for j,x in enumerate(self.data):
             d,i=self._nearest_centroid(x)
             self.labels_[j]=i

    # Ejemplo de random Clustering, es equivalente a la primera iteración de KMeans
    def randomClustering(self):
         # seleccionamos K elmentos distintos de forma aleatoria.
         # replace=False evita elegir dos veces el mismo elemento, que daría
         # menos de K clusters
         idx=np.random.choice(self.data.shape[0], self.n_clusters, replace=False)
         # diccionario {id_cluster: vector}, con los ids 0..K-1 como en scikit-learn
         self.centroids_=dict(enumerate(self.data[idx,:]))
         self._assign_nearest_centroids() #asignamos las etiquetas
         self._inertia() # calculamos el SSE
         return self

    def KMeans(self):
         print("Su implentación de KMeans")

    def FFTraversal(self):
        print("su implementación de Farthest First Traversal") 

    # Metodo para entrenar el modelo, solo recibe un numpy.array con los datos de n x p.
    # Donde n es el número de elmentos y p la dimensión            
    def fit(self,data):
        self.data=data
        self.algorithm()
        return self
    #Metodo que asinga un clusters a los elementos en data
    def predict(self,data):
        labels=[-1 for x in data]
        for j,x in enumerate(data):
            d,i=self._nearest_centroid(x)
            labels[j]=i
        return np.array(labels)
    #estructura propuesta para los algoritmos
    # La variable algorithm es un string con el nombre de su función de clustering
    def __init__(self,n_clusters=3,distance_function=euclidiana,algorithm='randomClustering'):
        self.n_clusters=n_clusters  # número de clusters K
        self.inertia_=0 # SSE
        self.distance_function=distance_function #Funcion de distancia, por defecto euclidiana
        self.algorithm=getattr(self, algorithm) 
    
    

    
                                
    

         
