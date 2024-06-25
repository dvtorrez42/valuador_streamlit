#app.py
import streamlit as st
import requests
import joblib
import numpy as np
import pandas as pd

model = joblib.load('./rnd_clf_2024-06-19.pkl')

def predict_house_price_new(tipoPropiedad, m2C, banios, recamaras, precio_m2T, h3_7):
    
    dict = {'tipoPropiedad':[float(tipoPropiedad)],
            'm2C': float(m2C),
            'banios':float(banios),
            'recamaras': float(recamaras),
            'precio_m2T':float(precio_m2T),
            'h3_7':float(h3_7)
       }
 
    df_to_predict = pd.DataFrame(dict)
    
    prediction = model.predict(df_to_predict)
    
    return np.round(prediction,0).tolist()[0]

st.title("Tasá tu casa o departamento virtualmente")

        
#tipoPropiedad = st.radio(
#    "Tipo de Propiedad",
#    [":house: Casa", ":department_store: Departamento" ]
#)
tipoPropiedad = st.selectbox(
    ":house: / :office:  Tipo de Propiedad (0: Casa, 1: Departamento)",
    ("0", "1")
)
m2C = st.number_input(":triangular_ruler: Metros cuadrados cubiertos", min_value=0, max_value=1000, value=100)
banios = st.number_input(":toilet: Cantidad de baños", min_value=0, max_value=10, value=1)
recamaras = st.number_input(":bed: Cantidad de cuartos", min_value=0, max_value=20, value=1)
precio_m2T = st.number_input(":moneybag: USD por metro cuadrado", min_value=0, max_value=10000, value=1500)
h3_7 = st.number_input(":cityscape: Barrio", min_value=0, max_value=100, value=8)


if st.button("Predict"):
    precio_predicho = predict_house_price_new(tipoPropiedad=tipoPropiedad,
                                              m2C=m2C,
                                              banios=banios,
                                              recamaras=recamaras,
                                              precio_m2T=precio_m2T,
                                              h3_7=h3_7)
    
    
    #result = requests.get("http://fastapi:8000/predict", params=params) 
    if precio_predicho > 0:
        st.success(f"El precio aproximado es de: {precio_predicho}")
    else:
        st.error("There was an error with the prediction.")
