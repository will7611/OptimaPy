import pandas as pd
import numpy as np
import random

meses = list(range(1, 13))
productos = [
    ('Aceite Fino 1L', 11.5), ('Arroz Grano de Oro 1kg', 7.0), ('Fideo Famosa 500g', 4.5),
    ('Azúcar Guabirá 1kg', 6.0), ('Harina Princesa 1kg', 5.5), ('Leche Pil 1L', 6.5),
    ('Café Copacabana 250g', 22.0), ('Mantequilla Regia 200g', 12.0), ('Coca Cola 2L', 13.0),
    ('Papel Higiénico Nacional', 15.0)
]

datos = []
for m in meses:
    for prod, costo in productos:
        # Simulamos tendencias: Bebidas suben en verano (meses 1, 2, 11, 12), arroz es estable
        tendencia = random.randint(50, 150)
        if 'Coca' in prod and m in [1, 2, 11, 12]: tendencia += 100
        
        datos.append([m, prod, costo, tendencia])

df_masivo = pd.DataFrame(datos, columns=['mes', 'producto', 'costo_unitario_bs', 'ventas_unidades'])
df_masivo.to_excel('ventas_pos_anual.xlsx', index=False)
print("Base de datos masiva generada: ventas_pos_anual.xlsx")