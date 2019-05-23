import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import cross_validation

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

data = pd.read_csv(
    "./salesdb/salesDB_grocery_market/sales.csv",
    sep=";",
    nrows=50000,
    usecols=["Quantity", "SalesDate"])

data["SalesDate"] = pd.to_datetime(
    data["SalesDate"], format="%Y-%m-%d %H:%M:%S.%f")

data = data.groupby(data["SalesDate"].dt.hour).sum()
data["index1"] = data.index

# graficando
# grouped2 = data
# grouped2["hora"] = data["SalesDate"].apply(lambda x: x.hour)
# grouped2["dia"] = grouped2["SalesDate"].apply(lambda x: x.day)
# grouped2 = grouped2.groupby(["dia", "hora"]).sum()
# grouped2.plot(ls="none", marker="o")

Y = data["Quantity"]
X = data.drop("Quantity", axis=1)
# YY = grouped2["Quantity"]
# XX = grouped2.drop("Quantity", axis=1)

Xtrain, Xtest, Ytrain, Ytest = train_test_split(
    X, Y, test_size=0.2, random_state=123)

Xtest = Xtest.sort_values("index1")
Ytest = Ytest.sort_index()

linear_regression = LinearRegression()
polynomial_features = PolynomialFeatures(degree=1, include_bias=False)

pipeline = Pipeline([("polynomial_features", polynomial_features),
                     ("linear_regression", linear_regression)])
pipeline.fit(Xtrain, Ytrain)

scores = cross_validation.cross_val_score(
    pipeline, X, Y, scoring="mean_squared_error", cv=10)

plt.plot(Xtest, pipeline.predict(Xtest))
plt.scatter(X, Y)

print(r2_score(Ytest, pipeline.predict(Xtest)))

# y ahora el modelo con el bosque aleatorio.
randomForest = RandomForestRegressor()
randomForest.fit(Xtrain, Ytrain)

plt.plot(Xtest, randomForest.predict(Xtest))
plt.scatter(X, Y)

print(r2_score(Ytest, randomForest.predict(Xtest)))

