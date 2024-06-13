# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 22:59:43 2024

@author: sajit
"""

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import requests  # For making API requests to FastAPI server
import streamlit as st


def analyze_data(data):


    url = "http://localhost:8000/predict_risk"  
    headers = {"Content-Type": "application/json"}
    data_body = {"policyno": data['Policy No'].values[0],
            "age": int(data['Age'].values[0]),
            "gender": data['Gender'].values[0],
            "annualincome": float(data['Annual income'].values[0]),
            "occupation": data['Occupation'].values[0],
            "education": data['Education'].values[0],
            "sumassured": float(data['Sum assured'].values[0]),
            "annualpremium":float(data['Annual premium'].values[0]),
            "premfreq": int(data['Prem frequency'].values[0]),
            "affscore": int(data['Affluence score'].values[0])}

    response = requests.post(url, headers=headers, json=data_body)
    with st.container(border=True):
        if response.status_code == 200:
            st.write("Risk Prediction Successfull !")
            # Optionally, display the response data from the API
            dataframe = pd.DataFrame(response.json())
            st.write("API response:")
            st.dataframe(dataframe,hide_index=True)
            st.write(f"Success Code: {response.status_code}")
        else:
            st.error(f"Error sending data: {response.status_code}")


  
# Streamlit app configuration
st.set_page_config(page_title="Risk Prediction", layout="wide")
st.title('Risk Forecast Calculator')

st.subheader("List of policy details to be evaluated for risk:")
data = {
    'Policy No': ['P2378AH', 'P6689GD', 'P0089TU','P9545VZ','P5567BU'],
    "Age": [55, 30, 18, 64,42],
    "Gender": ["M", "F", "M", "M","M"],
    "Annual income": [400000, 1304530, 4800000, 640000,5520000],
    "Occupation":  ["Others", "Self Employed", "Salaried", "Others","Salaried"],
    "Education":  ["Others", "Graduate", "Degree", "SSC","Degree"],
    "Sum assured": [5000000, 1000000, 5000000, 11500000,5000000],
    "Annual premium": [20000, 29300, 19350, 57200,8090],
    "Prem frequency": [12, 2, 6, 12,3],
    "Affluence score": [3, 4, 5, 3,5]
}

df = pd.DataFrame(data)

# Display the table
st.dataframe(df,hide_index=True)

options = df["Policy No"].tolist()  # Get a list of names for radio buttons
selected_name = st.radio("Select a Policy No:", options=options)


filtered_data = df[df["Policy No"]==selected_name]
  
# Display a button to trigger the function with the DataFrame
if st.button("Analyze Risk Probabilities", type="primary"):
  st.write('Routing Request to Model API....')
  analyze_data(filtered_data)  # Pass a copy of the DataFrame (recommended practice)

