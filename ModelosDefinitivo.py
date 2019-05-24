# DataFrame
import pandas as pd

# ### modelos de sklearn
from sklearn import model_selection as ms
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

# funciones para generar las tablas que se usarán
from randomForest import (dataset, limpiandoDataset, agruparDatosSUM,
                          agruparDatosMean)


# modelo de las ganancias totales por semana.
def gananciasDiaSemana(quanOrPrice):
    data = dataset()
    data = limpiandoDataset(data)
    data = agruparDatosSUM(data, ["fecha", "dia"], "")
    return data


# modelo de las ventas totales de un producto.
def gananciasProducto(producto, quanOrPrice):
    data = dataset()
    data = limpiandoDataset(data)
    data = agruparDatosSUM(data, ["Product", "dia", "fecha"], "")
    data = data.loc[data.Product == producto]
    return data


datosGlobal = gananciasDiaSemana(False)
datosVino = gananciasProducto("Wine - Red, Colio Cabernet", True)

# separando los datos en objetivo (Y) y features (X)
Y = datosGlobal.TotalPrice
X = datosGlobal.dia.values.reshape(-1, 1)
# Y = datosVino.Quantity
# X = datosVino.dia

# preparando los modelos
semilla = 7
modelos = []
modelos.append(("LR", LinearRegression()))
modelos.append(("DT", DecisionTreeRegressor()))
modelos.append(("RF", RandomForestRegressor()))
modelos.append(("SVR", SVR()))

# evaluando cada modelo
results = []
names = []
scoring = 'r2'
for name, model in modelos:
    kfold = ms.KFold(n_splits=10, random_state=semilla)
    cv_results = ms.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)
