# importando las bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st


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
    usecols=["Quantity", "SalesDate"])

# convirtiendo la columna de fecha en datetime
data["SalesDate"] = pd.to_datetime(
    data["SalesDate"], format="%Y-%m-%d %H:%M:%S.%f")

# creando columnas de fecha y hora
data["fecha"] = data["SalesDate"].dt.date
data["hora"] = data["SalesDate"].dt.hour

# agrupando por fecha y hora
data = data.groupby([data["fecha"], data["hora"]]).sum()

# se promedia el total de compras por cada hora del día en todos los días
# del dataset
data = data.reset_index(level="hora")
data = data.groupby(data.hora).mean()
