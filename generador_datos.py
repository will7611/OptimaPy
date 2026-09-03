import pandas as pd
import random

# Simular 6 meses de ventas para un micromercado local
meses = [1, 2, 3, 4, 5, 6]
datos = []

# Producto 1: Tendencia al alza (Ej. Aceite Fino 1L) - Costo: 11.5 Bs.
for m in meses:
    datos.append([m, 'Aceite Fino 1L', 11.5, int(150 + (m * 15) + random.uniform(-10, 10))])

# Producto 2: Ventas estables (Ej. Arroz Grano de Oro 1kg) - Costo: 7.0 Bs.
for m in meses:
    datos.append([m, 'Arroz Grano de Oro 1kg', 7.0, int(300 + random.uniform(-20, 20))])

# Producto 3: Tendencia a la baja (Ej. Fideo Famosa 500g) - Costo: 4.5 Bs.
for m in meses:
    datos.append([m, 'Fideo Famosa 500g', 4.5, int(250 - (m * 10) + random.uniform(-15, 15))])

df_historico = pd.DataFrame(datos, columns=['mes', 'producto', 'costo_unitario_bs', 'ventas_unidades'])

# Guardar como Excel para que Power BI lo pueda leer fácilmente después
df_historico.to_excel('historial_ventas_pyme.xlsx', index=False)
print("Archivo 'historial_ventas_pyme.xlsx' generado con éxito.")