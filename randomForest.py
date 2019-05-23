# importando las bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import sqlite3

bd = sqlite3.connect("./salesdb/salesDB_grocery_market/restaurante.sqlite")
dataB = bd.cursor()
allData = dataB.execute('select  categories.CategoryName, Products.ProductName, sales.Quantity, sales.SalesDate from sales, Products, categories where sales.ProductID = Products.ProductID AND categories.CategoryID = Products.CategoryID LIMIT 10')
for row in allData:
    print(row) 
'''
# función para obtener estadísticas sobre los datos
def valInterval(g):
    st_interval = st.t.interval(
        0.95,
        len(g) - 1,
        loc=np.mean(g.Quantity),
        scale=st.sem(g.Quantity))
    return pd.Series(dict(st_interval=st_interval))


# importando el dataset
data = pd.read_csv(
    "./salesdb/salesDB_grocery_market/sales.csv",
    sep=";",
    nrows=150000,
    usecols=["Quantity", "SalesDate","ProductID"])

dataProd = pd.read_csv(
    "./salesdb/salesDB_grocery_market/products.csv",
    sep=";",
    nrows=150000,
    usecols=["ProductID", "ProductName","Price", "CategoryID"])
dataCat = pd.read_csv(
    "./salesdb/salesDB_grocery_market/categories.csv",
    sep=";",
    nrows=150000,
    usecols=["CategoryID", "CategoryName"])
# convirtiendo la columna de fecha en datetime
data["SalesDate"] = pd.to_datetime(
    data["SalesDate"], format="%Y-%m-%d %H:%M:%S.%f")

# creando columnas de fecha y hora
data["fecha"] = data["SalesDate"].dt.date
data["hora"] = data["SalesDate"].dt.hour

# agrupando por fecha y hora
data = data.groupby(["ProductID", "fecha", "hora"]).mean()
#data = data.groupby([ data["hora"], data["ProductID"]]).sum()

# se promedia el total de compras por cada hora del día en todos los días
# del dataset
data = data.reset_index(level="ProductID")
#data = data.groupby(data.hora).mean()
print(data)
'''