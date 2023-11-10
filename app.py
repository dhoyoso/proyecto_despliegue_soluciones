import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import datetime as dt
import numpy as np

df = pd.read_csv('resultado_merge.csv')

app = dash.Dash(__name__)

# Agrega una columna 'Cancelled' en formato numérico (0 o 1) para contar las cancelaciones
df['Cancelled'] = df['Cancelled'].astype(int)

def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Proyecto DSA Grupo 5"),
            html.H3("Predicción de retrasos en vuelos"),
            html.Div(
                id="intro",
                children="Esta interfaz proporciona a los operadores de aeropuertos una herramienta integral para prever y gestionar retrasos en vuelos. Los usuarios pueden ingresar información de las torres de control como datos de vuelos y condiciones climáticas para obtener predicciones precisas de posibles retrasos. Las visualizaciones del comportamiento histórico ayudan a equilibrar la distribución de pistas de embarque y optimizar la toma de decisiones operativas."
            ),
        ],
    )

def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            # Fecha inicial
            html.P("Información del vuelo y condiciones climáticas:"),
            dcc.Tab(),
            html.Div(
                id="componentes-fecha-inicial",
                children=[
                    html.P("Fecha:", style=dict(width='10%', textAlign='center', margin='2%')),
                    html.Div(
                        id="componente-fecha",
                        children=[
                            dcc.DatePickerSingle(
                                id='datepicker-inicial',
                                min_date_allowed=dt.datetime.now() - dt.timedelta(days=365),
                                max_date_allowed=dt.datetime.now() + dt.timedelta(days=365),
                                initial_visible_month=dt.datetime.now(),
                                date=dt.datetime.now()
                            )
                        ],
                        style=dict(width='40%', display='inline-block', margin='2%')
                    ),
                    html.P("Hora:", style=dict(width='10%', textAlign='center', margin='2%')),
                    html.Div(
                        id="componente-hora",
                        children=[
                            dcc.Input(
                                id="dropdown-hora-inicial-hora",
                                type='number',
                                value=pd.to_datetime(dt.datetime.now()).hour,
                                min=0,
                                max=23,
                                style=dict(width='100%'),
                                className='HourInput'

                            )
                        ],
                        style=dict(width='40%', display='inline-block', textAlign='center', margin='2%')
                    )
                ],
                style=dict(display='flex', justifyContent='space-between')
            ),
            html.Div(
                        id="componente-slider",
                        children=[
                            html.P("Visibilidad:", style=dict(width='10%', textAlign='center', margin='2%')),
                            dcc.Slider(
                                id='slider-temperatura',
                                min=0,
                                max=100,
                                value=65,
                                marks={
                                    0: {'label': '0°C', 'style': {'color': '#77b0b1'}},
                                    26: {'label': '26°C'},
                                    37: {'label': '37°C'},
                                    100: {'label': '100°C', 'style': {'color': '#f50'}}
                                }
                            )
                        ],
                        style=dict(width='80%', display='inline-block', margin='2%')
                    )
        ]
    )


def graphs():
    return html.Div([
    html.H3('Historia de Retrasos'),
    html.Div([
        html.Div([
            html.Label('Selecciona un aeropuerto:'),
            dcc.Dropdown(
                id='airport-dropdown',
                options=[
                    {'label': 'Todos', 'value': 'all'},  # Opción para seleccionar todos los aeropuertos
                ] + [
                    {'label': df[df['AirportID'] == airport_id].iloc[0]['AeropuertoOrigen'], 'value': airport_id}
                    for airport_id in df['AirportID'].unique()
                ],
                value='all',  # Valor predeterminado: "todos"
                style={'width': '100%'}
            ),
        ], className="four columns", style={'width': '48%'}),
        html.Div([
            html.Label('Selecciona una aerolínea:'),
            dcc.Dropdown(
                id='carrier-dropdown',
                options=[
                    {'label': 'Todos', 'value': 'all'},  # Opción para seleccionar todas las aerolíneas
                ] + [
                    {'label': df[df['Carrier'] == carrier].iloc[0]['Aerolinea'], 'value': carrier}
                    for carrier in df['Carrier'].unique()
                ],
                value='all',  # Valor predeterminado: "todos"
                style={'width': '100%'}
            ),
        ], className="four columns", style={'width': '48%'}),
    ], className="row"),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(id='bar-chart')
        ], className="six columns"),
        html.Div([
            dcc.Graph(id='pie-chart')
        ], className="six columns"),
    ], className="row"),
])

# Define la interfaz de usuario con los menús desplegables, los gráficos de barras y el gráfico de pastel
app.layout = html.Div(
    id="app-container",
    children=[
        
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[


                # Grafica de la serie de tiempo
                html.Div(
                    id="model_graph",
                    children=[
                        graphs()
                    ],
                ),

            
            ],
        ),
    ],
)

# Crea una función de callback para actualizar los gráficos en función de las selecciones en los menús desplegables
@app.callback(
    [Output('bar-chart', 'figure'), Output('pie-chart', 'figure')],
    [Input('airport-dropdown', 'value'), Input('carrier-dropdown', 'value')]
)
def actualizar_graficos(airport_id, carrier):
    if airport_id == 'all':
        # Si se selecciona "todos" en el menú de aeropuertos, se muestra un gráfico con todos los datos
        df_filtrado = df
        title_bar = 'Cantidad de retrasos en todos los aeropuertos'
    else:
        # Filtra el DataFrame en función del valor seleccionado en el menú de aeropuertos
        df_filtrado = df[df['AirportID'] == airport_id]
        airport_name = df[df['AirportID'] == airport_id].iloc[0]['AeropuertoOrigen']
        title_bar = f'Cantidad de retrasos en el aeropuerto <br> {airport_name}'

    if carrier == 'all':
        # Si se selecciona "todos" en el menú de aerolíneas, se muestra un gráfico con todos los datos
        title_pie = 'Proporción de retrasos en todas las aerolíneas'
    else:
        # Filtra el DataFrame en función del valor seleccionado en el menú de aerolíneas
        df_filtrado = df_filtrado[df_filtrado['Carrier'] == carrier]
        carrier_name = df[df['Carrier'] == carrier].iloc[0]['Aerolinea']
        title_pie = f'Proporción de retrasos para la aerolínea <br> {carrier_name}'

    # Combina Month y Day en una nueva columna para el eje x
    df_filtrado['Month_Day'] = df_filtrado['Month'].astype(str) + '-' + df_filtrado['Day'].astype(str)

    # Agrupa los datos por Month_Day y cuenta la cantidad de DepDel15 True
    data_bar = df_filtrado.groupby('Month_Day')['DepDel15'].sum().reset_index()

    # Crea el gráfico de barras
    fig_bar = {
        'data': [
            {'x': data_bar['Month_Day'], 'y': data_bar['DepDel15'], 'type': 'bar', 'name': 'DepDel15 True'},
        ],
        'layout': {
            'title': title_bar,
            'xaxis': {'title': 'Mes-Día'},
            'yaxis': {'title': 'Cantidad de Retrasos'},
        }
    }

    # Calcula la cantidad de vuelos retrasados (DepDel15=True) y no retrasados (DepDel15=False)
    vuelos_retrasados = df_filtrado[df_filtrado['DepDel15'] == True].shape[0]
    vuelos_no_retrasados = df_filtrado[df_filtrado['DepDel15'] == False].shape[0]

    # Crea el gráfico de pastel
    labels_pie = ['Retrasados', 'No Retrasados']
    values_pie = [vuelos_retrasados, vuelos_no_retrasados]

    fig_pie = {
        'data': [
            go.Pie(
                labels=labels_pie,
                values=values_pie,
                textinfo='percent',
            ),
        ],
        'layout': {
            'title': title_pie,
        }
    }

    return fig_bar, fig_pie

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)