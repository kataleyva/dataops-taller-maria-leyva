#!/usr/bin/env python
# coding: utf-8

# # Análisis exploratorio de dataset ventas

# In[2]:


import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd().parent))

import pandas as pd
import matplotlib.pyplot as plt
from src.extract import extract_data
from src.transform import clean_data, calculate_metrics, aggregate_sales


# ## Carga y estructura de datos

# In[3]:


df_raw = extract_data("../data/ventas.db")
print(f"Filas: {df_raw.shape[0]} | Columnas: {df_raw.shape[1]}")
df_raw.head()


# In[5]:


df_raw.dtypes


# ## Calidad de los datos

# In[6]:


df_raw.isna().sum()


# In[8]:


columnas_sin_id = [col for col in df_raw.columns if col != "id"]
print(f"Duplicados: {df_raw.duplicated(subset=columnas_sin_id).sum()}")


# In[9]:


print(f"Cantidades negativas: {(df_raw['cantidad'] < 0).sum()}")
print(f"Precios <= 0: {(df_raw['precio_unitario'] <= 0).sum()}")
print(f"Fecha mínima: {df_raw['fecha'].min()} | Fecha máxima: {df_raw['fecha'].max()}")
df_raw[["cantidad", "precio_unitario"]].describe()


# ## Limpieza de datos

# In[10]:


df = calculate_metrics(clean_data(df_raw))
print(f"Total de filas antes: {len(df_raw)} | Total de filas después: {len(df)}")
print(f"Total nulos: {df.isna().sum().sum()}")
df.head()


# # Análisis exploratorio de datos

# ## Ventas por categoría

# In[13]:


ventas_categoria = df.groupby("categoria")["venta_total"].sum().sort_values(ascending = False)
ventas_categoria.plot(kind = "bar", title = "Ventas totales por categoría", ylabel = "Ventas ($)", rot = 0)
plt.show()
ventas_categoria


# # Tendencia mensual

# In[15]:


ventas_mes = df.groupby("mes")["venta_total"].sum()
ventas_mes.plot(kind = "line", marker = "o", title = "Ventas totales por mes", xlabel = "Mes")
plt.show()


# # Clientes recurrentes

# In[16]:


compras_cliente = df["cliente_id"].value_counts()
print(f"Clientes distintos: {compras_cliente.size}")
print(f"Promedio de compras por cliente: {compras_cliente.mean():.1f}")
compras_cliente.head(5)


# # Conclusiones

# 1. En la gráfica de ventas totales por categoría, la categoría con mayor cantidad de ventas es "Electronica" con 12663.44, seguida de "Ropa" con 9029.53, luego "Deportes" con 8012.00, y la que tiene menor cantidad de ventas es "Hogar" con 4949.65.
# 
# 2. En el diagrame de líneas se evidencia que las ventas tuvieron una tendencia creciente con picos muy fuertes de descenso en los meses 7 y 9. Mientras que los meses 6 y 12 tuvieron la mayor cantidad de ventas realizadas. Asimismo, se permite evidenciar que entre los meses 5 y 6, y 10 y 11, las ventas se mantuvieron casi constantes.
# 
# 3. En total de 200 registros, se tuvieron 50 clientes distintos donde el promedio total de compra por cliente fue de 4. Los clientes con mayor cantidad de compras son los que de ID: 23, 11, 44, 37 y 46 con 10, 8, 7 y 6 ventas respectivamente.

# ## Exportación a script

# In[17]:


get_ipython().system('jupyter nbconvert --to script exploracion.ipynb')

