# importando las bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import sqlite3


def dataset():
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
    return data


def limpiandoDataset(data):

    # convirtiendo la columna de fecha en datetime
    data = data.sort_values("SalesDate")
    print('organizando datos')
    data = data[data["SalesDate"] != 'NULL']
    print('eliminando datos nulos')
    data["SalesDate"] = pd.to_datetime(
        data["SalesDate"], format="%Y-%m-%d %H:%M:%S.%f")
    print('fechas parseadas')
    # creando columnas de fecha y hora
    data["fecha"] = data["SalesDate"].dt.date
    data["hora"] = data["SalesDate"].dt.hour
    data["dia"] = data["SalesDate"].dt.dayofweek
    data["semana"] = data["SalesDate"].dt.week

    return data


def agruparDatosSUM(data, campos, campo):
    data = data.groupby(campos).sum()
    print('datos agrupados')
    # data = data.groupby([ data["hora"], data["ProductID"]]).sum()

    # se promedia el total de compras por cada hora del día en todos los días
    # del dataset
    if campo != "":
        data = data.reset_index(level=campo)
    else:
        data = data.reset_index()
    # data = data.groupby(data.hora).mean()
    return data


def agruparDatosMean(data, campos, campo):
    data = data.groupby(campos).mean()
    print('datos agrupados')
    # data = data.groupby([ data["hora"], data["ProductID"]]).sum()

    # se promedia el total de compras por cada hora del día en todos los días
    # del dataset
    if campo != "":
        data = data.reset_index(level=campo)
    else:
        data = data.reset_index()

    # data = data.groupby(data.hora).mean()
    return data


if __name__ == "__main__":

    # dataset 1 - productos vendidos en un dia
    # data1 = dataset()
    # data1 = limpiandoDataset(data1)
    # data1 = agruparDatosSUM(data1, ["Product", "dia", "fecha", "Price"],"")
    # print(data1)

    # dataset 2 - cantidad de un cierto producto vendido en cierta semana
    # data2 = dataset()
    # data2 = limpiandoDataset(data2)
    # data2 = agruparDatosSUM(data2, ["Product", "semana", "Price"],"")
    # print(data2)

    # dataset 3 - ganancias generadas en cierta semana
    # data3 = dataset()
    # data3 = limpiandoDataset(data3)
    # data3 = agruparDatosSUM(data3, ["semana"],"")
    # print(data3)

    # dataset 4 - ganancias generadas en cierto dia de la semana
    # data4 = dataset()
    # data4 = limpiandoDataset(data4)
    # data4 = agruparDatosSUM(data4, ["dia"],"")
    # print(data4)

    # dataset 5 - ganancias generada por los productos
    # data5 = dataset()
    # data5 = limpiandoDataset(data5)
    # data5 = agruparDatosSUM(data5, ["Product"],"")
    # print(data5)

    # dataset 6 - ganancias generada por los categorias
    data6 = dataset()
    data6 = limpiandoDataset(data6)
    data6 = agruparDatosSUM(data6, ["Category"], "")
    print(data6)
