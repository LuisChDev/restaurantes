import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.externals import joblib

# modelo lineal
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

plt.close("all")

data = pd.read_csv(
    "./salesdb/salesDB_grocery_market/sales.csv", sep=";", nrows=50000)

# creando columnas de dia de la semana, dia del mes y hora:
# parseando la fecha.
data["SalesDate"] = pd.to_datetime(
    data["SalesDate"], format="%Y-%m-%d %H:%M:%S.%f")

# creando columnas de hora y dia
data["hora"] = data["SalesDate"].apply(lambda x: x.hour)
data["dia"] = data["SalesDate"].apply(lambda x: x.day)
data["diasem"] = data["SalesDate"].apply(lambda x: x.dayofweek)

# agrupando por hora y mostrando total de data.
print(data["hora"].value_counts().sort_index())

# graficando el numero de ventas por dia de la semana, hora o día del mes.
df = data["dia"].value_counts().sort_index()
df = df.cumsum()
plt.figure()
df.plot()

# predecimos el número de ventas de acuerdo a la hora del día, el día de la
# semana y del mes. Limpiamos la base de datos para que sólo queden los datos
# relevantes.

# primero, se agrupan los datos de acuerdo a dichos tiempos.
data = data.drop([
        "SalesPersonID", "CustomerID", "ProductID", "TotalPrice",
        "TransactionNumber", "Discount", "SalesID"
    ],
    axis=1)
# grouped = data.groupby(["dia", "diasem", "hora"]).sum()

# ordenando por fecha y hora
sortedDF = data.sort_values(by=["SalesDate"])
print(sortedDF)

# ubicando las entradas sin fecha
nanDate = sortedDF[sortedDF.SalesDate.notnull()]
print(nanDate)

# agrupando por hora
porHora = nanDate.groupby([nanDate["SalesDate"].dt.date,
                           nanDate["SalesDate"].dt.hour]).sum()
porHora.plot(ls="none", marker="o")

porHora2 = porHora.drop(["dia", "hora", "diasem"], axis=1)
print(porHora2)
porHora2.plot(ls="none", marker="o")

grouped = data.groupby(["diasem", "hora"]).sum()
grouped = grouped.drop("dia", axis=1)

grouped2 = data.groupby(["dia", "hora"]).sum()
grouped2 = grouped2.drop("diasem", axis=1)

grouped3 = data.groupby(["dia", "diasem"]).sum()
grouped3 = grouped3.drop("hora", axis=1)
print(grouped)

grouped.plot(ls="none", marker="o")

# separando los puntos en train y test
y = grouped.Quantity
X = grouped.index
print(grouped.index)
print(grouped.Quantity.head())
print(grouped.drop("Quantity", axis=1).head())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=123, stratify=y)
