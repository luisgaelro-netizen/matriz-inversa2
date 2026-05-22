import streamlit as st
import numpy as np
import pandas as pd

# Configuracion de la pagina
st.set_page_config(layout="wide")

# Panel de entrada y presentacion
st.title("Resolucion de Sistemas de Ecuaciones (Metodo de Matriz Inversa)")
st.write("Especifique las dimensiones del sistema e introduzca los coeficientes para calcular la solucion mediante el calculo de la inversa de la matriz A.")

# Control de dimensiones del sistema (limitado por estabilidad)
n = st.number_input("Dimension del sistema (n x n):", min_value=2, max_value=4, value=3, step=1, key="dim_n")

st.markdown("### Entrada de Datos")
st.write("Edite los valores numericos directamente en las celdas de las tablas inferiores:")

# Disposicion en columnas para las matrices de entrada
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("**Matriz de Coeficientes (A)**")
    # Carga de la matriz de ejemplo por defecto para n=3
    if n == 3:
        matriz_inicial_A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
    else:
        matriz_inicial_A = np.zeros((n, n), dtype=float)
        
    df_A = pd.DataFrame(matriz_inicial_A, columns=[f"x{i+1}" for i in range(n)])
    A_editada = st.data_editor(df_A, use_container_width=True, key="matriz_a")

with col2:
    st.markdown("**Vector de Terminos Independientes (b)**")
    # Carga del vector de ejemplo por defecto para n=3
    if n == 3:
        vector_inicial_b = np.array([8, -11, -3], dtype=float)
    else:
        vector_inicial_b = np.zeros(n, dtype=float)
        
    df_b = pd.DataFrame(vector_inicial_b, columns=["b"])
    b_editado = st.data_editor(df_b, use_container_width=True, key="vector_b")

# Ejecucion del proceso de calculo
if st.button("Ejecutar Calculos"):
    try:
        A_val = A_editada.values
        b_val = b_editado["b"].values

        # 1. Calculo de la matriz inversa usando numpy
        A_inversa = np.linalg.inv(A_val)

        # 2. Producto punto entre la matriz inversa y el vector b
        solucion = np.dot(A_inversa, b_val)

        # Despliegue de resultados: Matriz Inversa
        st.markdown("### Matriz Inversa Calculada (A⁻¹)")
        df_inversa = pd.DataFrame(A_inversa, columns=[f"Columna {i+1}" for i in range(n)])
        # Se formatea la tabla para mostrar 4 decimales
        st.dataframe(df_inversa.style.format("{:.4f}"), use_container_width=True)

        # Despliegue de resultados: Solucion del sistema
        st.markdown("### Vector Resultante de Soluciones")
        columnas_resultado = st.columns(n)
        for i in range(n):
            with columnas_resultado[i]:
                st.metric(label=f"Incognita x{i+1}", value=f"{solucion[i]:.4f}")

        st.markdown("---")
        # Boton para reiniciar la aplicacion
        if st.button("Volver a empezar", key="reset_inversa"):
            st.session_state.clear()
            st.rerun()

    # Intercepcion especifica de matrices que no tienen inversa (Determinante = 0)
    except np.linalg.LinAlgError:
        st.error("Error matematico: La matriz introducida es singular (su determinante es cero). Esto significa que no posee matriz inversa y el sistema no tiene una solucion unica.")
    
    # Intercepcion de cualquier otro error general (entradas nulas, formatos invalidos)
    except Exception as e:
        st.error(f"Error en la ejecucion del proceso. Compruebe la validez de los datos introducidos. Detalle tecnico: {e}")