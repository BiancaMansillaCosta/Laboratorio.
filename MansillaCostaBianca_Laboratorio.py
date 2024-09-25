# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:30:05 2024

@author: 55194298
"""

import pandas as pd
import numpy as np
import datetime as dt

import pandas as pd

emisiones2016 = pd.read_csv("C:\\Users\\55194298\\Downloads\\emisiones-2016.csv", sep = ";" )
emisiones2017 = pd.read_csv("C:\\Users\\55194298\\Downloads\\emisiones-2017.csv", sep = ";" )
emisiones2018 = pd.read_csv("C:\\Users\\55194298\\Downloads\\emisiones-2018.csv", sep = ";" )
emisiones2019 = pd.read_csv("C:\\Users\\55194298\\Downloads\\emisiones-2019.csv", sep = ";" )
#emisiones

emisiones = pd.concat([emisiones2016, emisiones2017, emisiones2018, emisiones2019])

#Parte 1: Generar un DataFrame con los datos de los cuatro archivos.
emisiones
print(emisiones)

columnas = ["ESTACION", "MAGNITUD", "ANO", "MES"]
columnas.extend([col for col in emisiones if col.startswith("D")])
emisiones = emisiones [columnas]
emisiones


emisiones = emisiones.melt(id_vars=["ESTACION", "MAGNITUD", "ANO", "MES"], var_name="DIA", value_name= "VALOR") 
emisiones
print(emisiones)

emisiones["DIA"] = emisiones.DIA.str.strip("D")
emisiones["FECHA"] = emisiones.ANO.apply(str) + "/" + emisiones.MES.apply(str) + "/" + emisiones.DIA.apply(str)

emisiones['FECHA'] = pd.to_datetime(emisiones.FECHA, format='%Y/%m/%d', infer_datetime_format=True, errors='coerce')

#Borra el Nan: filas con fechas no válidas
emisiones = emisiones.drop(emisiones[np.isnat(emisiones.FECHA)].index)
emisiones.sort_values(["ESTACION", "MAGNITUD", "FECHA"])
print(emisiones)

print("Estaciones: ", emisiones.ESTACION.unique())
print("Estaciones: ", emisiones.MAGNITUD.unique())
print("------------------------------:")

def evolucion(estacion, contaminante, desde, hasta):
    return emisiones[(emisiones.ESTACION == estacion) & (emisiones.MAGNITUD == contaminante) & (emisiones.FECHA >= desde) & (emisiones.FECHA <= hasta)].sort_values('FECHA').VALOR

print(evolucion(56, 8, dt.datetime.strptime('2018/10/25', '%Y/%m/%d'), dt.datetime.strptime('2019/02/12', '%Y/%m/%d')))

print(emisiones.groupby("MAGNITUD").VALOR.describe())
print(emisiones.groupby(["ESTACION", "MAGNITUD"]).VALOR.describe())

def resumen (estacion, contaminante):
    return emisiones[(emisiones.ESTACION == estacion) & (emisiones.MAGNITUD == contaminante)].VALOR.describe()

print("Resumen Dióxido de Nitrógeno en Plaza Elíptica:\n", resumen(56, 8), "\n", sep="")
print("Resumen Dióxido de Nitrógeno en Plaza del Carmen:\n", resumen(35, 8), sep="")

def evolucion_mensual(contaminante, ano):
    return emisiones[(emisiones.MAGNITUD == contaminante) & (emisiones.ANO == ano)].groupby(["ESTACION", "MES"]).VALOR.mean().unique
print(evolucion_mensual(8,2019))