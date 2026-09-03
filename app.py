import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import random
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="OptimaPy ERP", layout="wide", page_icon="📈")

# Función interna para simular el mercado
def generar_datos_demo():
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
            tendencia = random.randint(50, 150)
            if 'Coca' in prod and m in [1, 2, 11, 12]: tendencia += 100 # Sube en verano
            datos.append([m, prod, costo, tendencia])
    return pd.DataFrame(datos, columns=['mes', 'producto', 'costo_unitario_bs', 'ventas_unidades'])

# --- BARRA LATERAL: Configuración ---
with st.sidebar:
    st.title("⚙️ Configuración")
    st.info("Modo de presentación para el jurado:")
    usar_demo = st.button("🚀 Cargar Datos de Demostración")
    st.markdown("---")
    archivo_subido = st.file_uploader("O sube un Excel de ventas real", type=["xlsx"])
    margen_objetivo = st.slider("Margen de Ganancia Deseado (%)", 10, 50, 30) / 100
    gastos_fijos = st.number_input("Gastos Fijos Mensuales (Bs.)", value=2500)

st.title("📈 OptimaPy: Inteligencia Operativa")

df_historico = None
if usar_demo:
    df_historico = generar_datos_demo()
elif archivo_subido is not None:
    df_historico = pd.read_excel(archivo_subido)

if df_historico is not None:
    
    # Motor Predictivo
    predicciones = []
    for producto in df_historico['producto'].unique():
        df_prod = df_historico[df_historico['producto'] == producto]
        X = df_prod[['mes']]
        y = df_prod['ventas_unidades']
        
        modelo = LinearRegression()
        modelo.fit(X, y)
        venta_predicha = max(0, modelo.predict(pd.DataFrame({'mes': [13]}))[0]) 
        
        predicciones.append({
            'Producto': producto,
            'Venta_Proyectada': round(venta_predicha, 0),
            'Costo_Unitario_Bs': df_prod['costo_unitario_bs'].iloc[0]
        })

    df_pred = pd.DataFrame(predicciones)
    df_pred['Stock_Actual'] = np.random.randint(20, 100, size=len(df_pred))
    
    # Cálculos Operativos y Financieros
    df_pred['Precio_Sugerido_Bs'] = round(df_pred['Costo_Unitario_Bs'] / (1 - margen_objetivo), 2)
    df_pred['Unidades_A_Comprar'] = (df_pred['Venta_Proyectada'] - df_pred['Stock_Actual']).clip(lower=0)
    df_pred['Alerta'] = np.where(df_pred['Unidades_A_Comprar'] > 0, '🔴 Comprar', '🟢 Ok')
    df_pred['Ganancia_Bruta'] = df_pred['Venta_Proyectada'] * (df_pred['Precio_Sugerido_Bs'] - df_pred['Costo_Unitario_Bs'])

    # --- KPIs ---
    ganancia_total = df_pred['Ganancia_Bruta'].sum()
    flujo_neto = ganancia_total - gastos_fijos
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas Proyectadas (Unidades)", int(df_pred['Venta_Proyectada'].sum()))
    col2.metric("Ganancia Bruta Esperada (Bs.)", f"{ganancia_total:,.2f}")
    col3.metric("Flujo Neto (Bs.)", f"{flujo_neto:,.2f}", delta=float(flujo_neto))

    st.markdown("---")
    
    # --- GRÁFICO EMPRESARIAL 1: Comparativa de Inventario ---
    st.subheader("📊 Análisis de Inventario Predictivo")
    fig_bar = go.Figure(data=[
        go.Bar(name='Stock Actual', x=df_pred['Producto'], y=df_pred['Stock_Actual'], marker_color='#00CC96'),
        go.Bar(name='Venta Proyectada', x=df_pred['Producto'], y=df_pred['Venta_Proyectada'], marker_color='#EF553B')
    ])
    fig_bar.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Unidades", margin=dict(t=10, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)

    col_izq, col_der = st.columns([1.2, 1])
    
    with col_izq:
        st.subheader("📋 Decisiones de Compra y Precios")
        st.dataframe(df_pred[['Producto', 'Stock_Actual', 'Unidades_A_Comprar', 'Precio_Sugerido_Bs', 'Alerta']], use_container_width=True)
        
    with col_der:
        # --- GRÁFICO EMPRESARIAL 2: Tendencias Limpias ---
        st.subheader("📈 Tendencias del Mercado")
        fig_line = px.line(df_historico, x='mes', y='ventas_unidades', color='producto', markers=True)
        fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Mes", yaxis_title="Ventas", margin=dict(t=10, b=10))
        st.plotly_chart(fig_line, use_container_width=True)

else:
    st.info("👈 Haz clic en 'Cargar Datos de Demostración' en el menú lateral para iniciar la plataforma.")