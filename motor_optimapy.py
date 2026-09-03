import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Cargar los datos generados
df_historico = pd.read_excel('historial_ventas_pyme.xlsx')

predicciones = []

# 2. Entrenar modelo por cada producto
for producto in df_historico['producto'].unique():
    df_prod = df_historico[df_historico['producto'] == producto]
    
    X = df_prod[['mes']]
    y = df_prod['ventas_unidades']
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Predecir mes 7
    mes_futuro = pd.DataFrame({'mes': [7]})
    venta_predicha = modelo.predict(mes_futuro)[0]
    
    predicciones.append({
        'producto': producto,
        'venta_proyectada_mes_7': round(venta_predicha, 0),
        'costo_unitario_bs': df_prod['costo_unitario_bs'].iloc[0]
    })

df_prediccion = pd.DataFrame(predicciones)

# 3. Datos de stock simulado actual en el almacén de la tienda
stock_actual_tienda = {'Aceite Fino 1L': 80, 'Arroz Grano de Oro 1kg': 310, 'Fideo Famosa 500g': 150}
df_prediccion['stock_actual'] = df_prediccion['producto'].map(stock_actual_tienda)

# 4. Inteligencia Operativa: Precios y Alertas
# Margen del 30% sobre el costo para el mercado retail
df_prediccion['precio_sugerido_bs'] = round(df_prediccion['costo_unitario_bs'] / (1 - 0.30), 2)

df_prediccion['unidades_a_comprar'] = df_prediccion['venta_proyectada_mes_7'] - df_prediccion['stock_actual']
df_prediccion['unidades_a_comprar'] = df_prediccion['unidades_a_comprar'].apply(lambda x: x if x > 0 else 0)

df_prediccion['alerta_inventario'] = np.where(
    df_prediccion['unidades_a_comprar'] > 0, 
    'URGENTE: Contactar Proveedor', 
    'Stock Suficiente'
)

print("\n--- RESULTADOS OPTIMAPY ---")
print(df_prediccion[['producto', 'venta_proyectada_mes_7', 'unidades_a_comprar', 'alerta_inventario', 'precio_sugerido_bs']])