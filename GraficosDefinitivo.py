# para leer los datos csv
import pandas as pd

# para graficar los datos
import matplotlib.pyplot as plt

# funciones para importar los datos, limpiarlos y agruparlos
from randomForest import (dataset, limpiandoDataset, agruparDatosMean,
                          agruparDatosSUM)

# dataset 1 - productos vendidos en un dia
# vamos a utilizar este dataset para generar la información de cuánto se
# vendió un producto específico por día de la semana, y ver si hay
# un patrón en estas ventas.
def graficaDiaSemana(producto, quanOrPrice):
    data = dataset()
    data = limpiandoDataset(data)
    data = agruparDatosSUM(data, ["Product", "dia", "fecha", "Price"], "")
    data = data.loc[data.Product == producto]
    if quanOrPrice:
        plt.scatter(data.dia, data.Quantity)
    else:
        plt.scatter(data.dia, data.TotalPrice)


# dataset 2 - cantidad de un cierto producto vendido en cierta semana
def graficaSemana(producto, quanOrPrice):
    data = dataset()
    data = limpiandoDataset(data)
    data = agruparDatosSUM(data, ["Product", "semana", "Price"], "")
    data = data.loc[data.Product == producto]
    if quanOrPrice:
        plt.scatter(data.semana, data.Quantity)
    else:
        plt.scatter(data.semana, data.TotalPrice)


# dataset 3 - ganancias generadas en cierta semana
def gananciasSemana(quanOrPrice):
    data = dataset()
    data = limpiandoDataset(data)
    data = agruparDatosSUM(data, ["semana"],"")
    if quanOrPrice:
        plt.scatter(data.semana, data.Quantity)
    else:
        plt.scatter(data.semana, data.TotalPrice)


# dataset 4 - ganancias generadas en cierto dia de la semana
def gananciasDiaSemana(quanOrPrice):
    data = dataset()
    data = limpiandoDataset(data)
    data = agruparDatosSUM(data, ["fecha", "dia"],"")
    if quanOrPrice:
        plt.scatter(data.dia, data.Quantity)
    else:
        plt.scatter(data.dia, data.TotalPrice)


# dataset 5 - ganancias generada por los productos
def gananciasProductos(quanOrPrice):
    data = dataset()
    data = limpiandoDataset(data)
    data = agruparDatosSUM(data, ["Product"],"")
    if quanOrPrice:
        plt.scatter(data.index, data.Quantity)
    else:
        plt.scatter(data.index, data.TotalPrice)

# dataset 6 - ganancias generada por los categorias
def gananciasCategoria(quanOrPrice):
    data = dataset()
    data = limpiandoDataset(data)
    data = agruparDatosSUM(data, ["Category"],"")
    if quanOrPrice:
        plt.scatter(data.index, data.Quantity)
    else:
        plt.scatter(data.index, data.TotalPrice)
