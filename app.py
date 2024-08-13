#app.py
import streamlit as st
import joblib
import numpy as np
import pandas as pd


# configs
MUNICIPIOS_OPTIONS = ['Centro', 'Oeste', 'Norte', 'Este', 'Sur', 'Equipetrol', 'Urubo',
       'Ciudadelas', 'Ñuflo de Chávez', 'Las Palmas']
H3_6_OPTIONS = ['868b221a7ffffff', '868b22117ffffff', '868b22187ffffff',
       '868b22137ffffff', '868b22c4fffffff', '868b22c5fffffff',
       '868b221afffffff', '868b22c47ffffff', '868b22cefffffff',
       '868b221b7ffffff', '868b2219fffffff', '868b22197ffffff',
       '868b22ccfffffff', '868b22c57ffffff', '868b2218fffffff',
       '868b22c6fffffff', '868b2211fffffff', '868b2289fffffff',
       '868b2256fffffff']

price_pipe = joblib.load('./price_pipe.joblib')

def predict_house_price_new(banios, estacionamientos, m2C, m2T, municipio, recamaras, h3_6):
    
    dict = {'banios':float(banios),
            'estacionamientos': float(estacionamientos),
            'm2C':float(m2C),
            'm2T': float(m2T),
            'municipio':municipio,
            'recamaras':float(recamaras),
            'h3_6':h3_6
       }

    df_to_predict = pd.DataFrame(dict, index=[0])
    
    prediction = price_pipe.predict(df_to_predict)
    
    return prediction.tolist()[0]

st.title("Tase su casa virtualmente")

        
#tipoPropiedad = st.radio(
#    "Tipo de Propiedad",
#    [":house: Casa", ":department_store: Departamento" ]
#)

# m2C = st.number_input(":triangular_ruler: Metros cuadrados cubiertos", min_value=0, max_value=1000, value=100)
# banios = st.number_input(":toilet: Cantidad de baños", min_value=0, max_value=10, value=1)
# recamaras = st.number_input(":bed: Cantidad de cuartos", min_value=0, max_value=20, value=1)
# precio_m2T = st.number_input(":moneybag: USD por metro cuadrado", min_value=0, max_value=10000, value=1500)
# h3_7 = st.number_input(":cityscape: Barrio", min_value=0, max_value=100, value=8)

usdbob = st.number_input(
    ":dollar: Cotización del Dólar", value=6.86, min_value=6.0, max_value=30.0, placeholder="Cotizaciónd el dolar para ver el precio en esta moneda"
)

municipio = st.selectbox(":round_pushpin: Zona:", options=MUNICIPIOS_OPTIONS, index=2, 
                       #format_func=special_internal_function, 
                       key=None, help=None, on_change=None, args=None, kwargs=None, placeholder="Elegir una zona de la ciudad", disabled=False, label_visibility="visible")
m2T = st.slider(":triangular_ruler: Metros cuadrados totales", min_value=50, max_value=1000, value=None, step=50)
m2C = st.slider(":triangular_ruler: Metros cuadrados cubiertos", min_value=50, max_value=1000, value=None, step=50)
recamaras = st.slider(":bed: Cantidad de cuartos", min_value=1, max_value=5, step=1, value=None)
banios = st.slider(":toilet: Cantidad de baños", min_value=1, max_value=5, step=1, value=None)
estacionamientos = st.slider(":car: Cantidad de estacionamientos", min_value=1, max_value=3, step=1, value=None)
h3_6=st.selectbox(":round_pushpin: Zona especial:", options=H3_6_OPTIONS, index=2, 
                       #format_func=special_internal_function, 
                       key=None, help=None, on_change=None, args=None, kwargs=None, placeholder="Elegir una zona de la ciudad", disabled=False, label_visibility="visible")

if st.button("Predict"):
    precio_predicho = predict_house_price_new(banios=banios,
                                            estacionamientos=estacionamientos,
                                            m2C=m2C,
                                            m2T=m2T,
                                            municipio=municipio,
                                            recamaras=recamaras,
                                            h3_6=h3_6)
    
    
    #result = requests.get("http://fastapi:8000/predict", params=params) 
    if precio_predicho > 0:
        st.success(f"El precio aproximado es de: Bs. {round(np.exp(precio_predicho))}, ó USD {round(np.exp(precio_predicho)/usdbob)}.")
    else:
        st.error("Hubo un error en la tasación. Por favor contactarse al teléfono 12345678.")
