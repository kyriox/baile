import numpy as np
import matplotlib.pyplot as plt


def dibuja_frontera_2D(clf, X, yp, ax=None, titulo='', pasos=200, margen=0.5):
  """Dibuja la frontera de decisión de un clasificador sobre datos de 2 dimensiones.

  clf     clasificador ya entrenado, con un método predict
  X       datos de n x 2 que se grafican encima de la frontera
  yp      etiquetas usadas para colorear los puntos
  ax      ejes de matplotlib donde dibujar (si es None se usan los actuales)
  titulo  título opcional para los ejes
  pasos   resolución de la rejilla (pasos x pasos puntos)
  margen  cuánto se extiende la rejilla más allá de los datos
  """
  if ax is None:
    ax = plt.gca()
  # rejilla que cubre todo el rango de los datos
  x = np.linspace(X[:, 0].min() - margen, X[:, 0].max() + margen, pasos)
  y = np.linspace(X[:, 1].min() - margen, X[:, 1].max() + margen, pasos)
  XX, YY = np.meshgrid(x, y)
  # clasificamos CADA punto de la rejilla: el resultado es la frontera
  B = np.c_[XX.ravel(), YY.ravel()]
  Bo = np.asarray(clf.predict(B)).ravel().reshape(XX.shape)
  ax.contourf(XX, YY, Bo, alpha=0.2)
  ax.scatter(X[:, 0], X[:, 1], c=yp, edgecolors='k', linewidths=0.3)
  if titulo:
    ax.set_title(titulo)
  return ax
