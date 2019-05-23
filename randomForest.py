# importando las bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import sqlite3

bd = sqlite3.connect("./salesdb/salesDB_grocery_market/restaurante.sqlite")
print('conexion exitosa!')
dataB = bd.cursor()
allData = dataB.execute('select categories.CategoryName, Products.ProductName, sales.Quantity, Products.Price,(sales.Quantity*Products.Price), sales.SalesDate from sales, Products, categories where sales.ProductID = Products.ProductID AND categories.CategoryID = Products.CategoryID LIMIT 100000')
products = []
print('leyendo datos!')
for row in allData:
    products.append({
        'Category': row[0],
        'Product': row[1],
        'Quantity': row[2],
        'Price': row[3],
        'TotalPrice': row[4],
        'SalesDate': row[5]
    })
data = pd.DataFrame(data=products)
print('lectura exitosa!')

# convirtiendo la columna de fecha en datetime
data = data.sort_values("SalesDate")
print('organizando datos')
data = data[data["SalesDate"]!='NULL']
print('eliminando datos nulos')

data["SalesDate"] = pd.to_datetime(
    data["SalesDate"], format="%Y-%m-%d %H:%M:%S.%f")
print('fechas parseadas')
# creando columnas de fecha y hora
data["fecha"] = data["SalesDate"].dt.date
data["hora"] = data["SalesDate"].dt.hour
data["dia"] = data["SalesDate"].dt.dayofweek

# agrupando por fecha y hora
data = data.groupby(["Product","hora","dia", "fecha", "Price"]).mean()
print('datos agrupados')
#data = data.groupby([ data["hora"], data["ProductID"]]).sum()

# se promedia el total de compras por cada hora del día en todos los días
# del dataset
data = data.reset_index()
#data = data.groupby(data.hora).mean()
print(data["Product"])

'''
- total ventas en la semana
- que producto se vende mas en cierto dia
- 

'''