#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:22:20 2023

@author: Equipo DSA
"""

import pandas as pd
from sklearn.model_selection import train_test_split


merged_data = pd.read_csv('./merged_data.csv')

# División del dataset en variable objetivo (Y) y variables explicativas (X)
X = merged_data.drop(columns =['DepDel15'],axis=1)
Y = merged_data['DepDel15']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

#Importe MLFlow para registrar los experimentos, el regresor de bosques aleatorios y la métrica de error cuadrático medio
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# defina el servidor para llevar el registro de modelos y artefactos
# mlflow.set_tracking_uri('http://localhost:5000')
# registre el experimento
experiment = mlflow.set_experiment("sklearn-flights-delay")

# defina los parámetros del modelo
n_estimators = [100,200,300,400]
max_depth = [3, 6, 8]
max_features = ['sqrt', 'log2']
loss = ['log_loss', 'exponential']
learning_rate = [0.1,0.15,0.20,0.25]

for m in range(len(learning_rate)):
    for l in range(len(loss)):
        for k in range(len(max_features)):
            for j in range(len(max_depth)):
                for i in range(len(n_estimators)):
                    # Aquí se ejecuta MLflow sin especificar un nombre o id del experimento. MLflow los crea un experimento para este cuaderno por defecto y guarda las características del experimento y las métricas definidas. 
                    # Para ver el resultado de las corridas haga click en Experimentos en el menú izquierdo. 
                    with mlflow.start_run(experiment_id=experiment.experiment_id, run_name = "gradientboosting-classifier_" + str(n_estimators[i]) + "_" + str(max_depth[j]) + "_" + str(max_features[k]) + "_" + str(loss[l]) + "_" + str(learning_rate[m])):               
                
                        # Cree el modelo con los parámetros definidos y entrénelo
                        gbc = GradientBoostingClassifier(n_estimators=n_estimators[i], loss=loss[l], learning_rate=learning_rate[m], max_depth=max_depth[j], max_features=max_features[k],  random_state=0)
                        gbc.fit(X_train, y_train)
                        # Realice predicciones de prueba
                        predictions = gbc.predict(X_test)
                    
                        # Registre los parámetros
                        mlflow.log_param("n_estimators", n_estimators[i])
                        mlflow.log_param("max_depth", max_depth[j])
                        mlflow.log_param("max_features", max_features[k])
                        mlflow.log_param("loss", loss[l])
                        mlflow.log_param("learning_rate", learning_rate[m])
                    
                        # Registre el modelo
                        mlflow.sklearn.log_model(gbc, "gradientboosting-classifier-model")
                    
                        # Calcular y registrar las métricas
                        accuracy = accuracy_score(y_test, predictions)
                        precision = precision_score(y_test, predictions)
                        recall = recall_score(y_test, predictions)
                        f1 = f1_score(y_test, predictions)
                
                        mlflow.log_metric("accuracy", accuracy)
                        mlflow.log_metric("precision", precision)
                        mlflow.log_metric("recall", recall)
                        mlflow.log_metric("f1_score", f1)
                        
                        print(accuracy,precision,recall,f1)


# # defina los parámetros del modelo
# penalty = ['l2','l1']
# solver = ['lbfgs', 'saga']

# for i in range(len(n_estimators)):
#     # Aquí se ejecuta MLflow sin especificar un nombre o id del experimento. MLflow los crea un experimento para este cuaderno por defecto y guarda las características del experimento y las métricas definidas. 
#     # Para ver el resultado de las corridas haga click en Experimentos en el menú izquierdo. 
#     with mlflow.start_run(experiment_id=experiment.experiment_id, run_name="logisticregression-classifier"+str(i+1)):

#         # Cree el modelo con los parámetros definidos y entrénelo
#         lr = LogisticRegression(penalty=penalty[i], solver=solver[i], random_state=0)
#         lr.fit(X_train, y_train)
#         # Realice predicciones de prueba
#         predictions = lr.predict(X_test)
    
#         # Registre los parámetros
#         mlflow.log_param("penalty", penalty)
#         mlflow.log_param("solver", solver)
    
#         # Registre el modelo
#         mlflow.sklearn.log_model(lr, "logistic-regression-model")
    
#         # Cree y registre la métrica de interés
#         roc_auc = roc_auc_score(y_test, predictions)
#         mlflow.log_metric("roc_auc_score", roc_auc)
#         print(roc_auc)