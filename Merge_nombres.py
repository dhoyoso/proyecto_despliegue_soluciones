#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# Cargar el DataFrame 'merged_data.csv'
merged_data = pd.read_csv(r"C:\Users\camab\Downloads\merged_data (1).csv")
merged_data['Carrier'] = merged_data['Carrier'].apply(str)
# Cargar el DataFrame 'L_AIRPORT_ID.csv'
L_AIRPORT_ID = pd.read_csv(r"C:\Users\camab\OneDrive\Documentos\Maestria Andes\6toCiclo\Despliegue\RetrasosVuelos\L_AIRPORT_ID.csv")
Unique_carrier = pd.read_csv(r"C:\Users\camab\Downloads\L_UNIQUE_CARRIERS.csv", sep=",")
# Realizar el merge basado en las columnas 'AirportID' y 'DestAirportID'
result = merged_data.merge(L_AIRPORT_ID, left_on=['DestAirportID',], right_on=['Code'], how='inner')
#result = merged_data.merge(L_AIRPORT_ID, left_on=['AirportID',], right_on=['Code'], how='inner')
#result = merged_data.merge(Unique_carrier, left_on=['Carrier',], right_on=['Codigo'], how='inner')
# result contendrá el resultado del merge con todas las columnas de ambos DataFrames
# Puedes guardar este resultado en un nuevo archivo CSV si lo deseas
#result.to_csv('resultado_merge.csv', index=False)
result = result.rename(columns={'Description': 'AeropuertoDestino'})

result = result.merge(L_AIRPORT_ID, left_on=['AirportID',], right_on=['Code'], how='inner')

result = result.rename(columns={'Description': 'AeropuertoOrigen'})


result = result.merge(Unique_carrier, left_on=['Carrier'], right_on=['Code'], how='inner')

result.info()

result = result.drop(['Code_x', 'Code_y',"Code"], axis=1)

result = result.rename(columns={'Description': 'Aerolinea'})

result.head()

result = result.rename(columns={'Description': 'AeropuertoOrigen'})
result.to_csv('resultado_merge.csv', index=False)