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
from sklearn import datasets, linear_model

plt.close("all")

data = pd.read_csv(
    "./salesdb/salesDB_grocery_market/sales.csv", sep=";", nrows=10000)

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
data = data.drop(
    "SalesPersonID", axis=1).drop(
        "CustomerID", axis=1).drop(
            "ProductID", axis=1).drop(
                "TotalPrice", axis=1).drop(
                    "TransactionNumber", axis=1)
data = data.drop("Discount", axis=1)
data = data.drop("SalesID", axis=1)
grouped = data.groupby(["dia", "diasem", "hora"]).sum()
print(grouped)

grouped.plot()

# separando los puntos en train y test
y = grouped.Quantity
X = grouped.drop("Quantity", axis=1)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=123, stratify=y)

# creando el modelo lineal
regr = linear_model.LinearRegression()

# pipeline = make_pipeline(
#     preprocessing.StandardScaler(), RandomForestRegressor(n_estimators=100))

# hyperparameters = {
#     'randomforestregressor__max_features': ['auto', 'sqrt', 'log2'],
#     'randomforestregressor__max_depth': [None, 5, 3, 1]
# }

# clf = GridSearchCV(pipeline, hyperparameters, cv=10)
regr.fit(X_train, y_train)
print(regr.best_params_)

y_pred = regr.predict(X_test)
print(r2_score(y_test, y_pred))
print(mean_squared_error(y_test, y_pred))

joblib.dump(regr, "regression.pkl")
