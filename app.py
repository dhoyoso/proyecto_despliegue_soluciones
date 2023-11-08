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
            #html.H5("Proyecto 1"),
            html.H3("Predicción de retrasos en vuelos"),
            html.Div(
                id="intro",
                children="Esta herramienta contiene información sobre la demanda energética total en Austria cada hora según lo públicado en ENTSO-E Data Portal. Adicionalmente, permite realizar pronósticos hasta 5 dias en el futuro."
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
            html.P("Detalles del vuelo para predecir retrasos:"),
            dcc.Tab(),
            html.Div(
                id="componentes-fecha-inicial",
                children=[
                    html.P("Fecha:",style=dict(width='10%', textAlign='center', margin= '2%')),
                    html.Div(
                        id="componente-fecha",
                        children=[
                            dcc.DatePickerSingle(
                                id='datepicker-inicial',
                                min_date_allowed=dt.datetime.now()-dt.timedelta(days=365),
                                max_date_allowed=dt.datetime.now()+dt.timedelta(days=365),
                                initial_visible_month=dt.datetime.now(),
                                date=dt.datetime.now()
                            )
                        ],
                        style=dict(width='20%')
                    ),
                    html.Div(
                        id="campo-slider",
                        children=[
                            html.P("Hora:"),
                            dcc.Slider(
                                id="slider-proyeccion",
                                min=0,
                                max=24,
                                step=1,
                                value=0,
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True},
                            )
                        ]
                    ),
                    html.Div(
                        id="componente-hora",
                        children=[
                            dcc.Dropdown(
                                id="dropdown-hora-inicial-hora",
                                options=[{"label": i, "value": i} for i in np.arange(0,25)],
                                value=pd.to_datetime(dt.datetime.now()).hour,
                                # style=dict(width='50%', display="inline-block")
                            )
                        ],
                        style=dict(width='20%')
                    ),
                    
                ],
                style=dict(display='flex')
            ),

            html.Br(),

            # Slider proyección
            html.Div(
                id="campo-slider",
                children=[
                    html.P("Ingrese horas a proyectar:"),
                    dcc.Slider(
                        id="slider-proyeccion",
                        min=0,
                        max=119,
                        step=1,
                        value=0,
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ]
            )
     
        ]
    )

def graphs():
    return html.Div([
    html.H1('Gráfico de Barras y Gráfico de Pastel Dash'),
    html.Div([
        html.Div([
            html.Label('Selecciona un aeropuerto:'),
            dcc.Dropdown(
                id='airport-dropdown',
                options=[
                    {'label': 'Todos', 'value': 'all'},  # Opción para seleccionar todos los aeropuertos
                ] + [
                    {'label': airport_id, 'value': airport_id}
                    for airport_id in df['AirportID'].unique()
                ],
                value='all'  # Valor predeterminado: "todos"
            ),
        ], className="four columns"),
        #description_card(), generate_control_card(),
        html.Div([
            html.Label('Selecciona una aerolínea:'),
            dcc.Dropdown(
                id='carrier-dropdown',
                options=[
                    {'label': 'Todos', 'value': 'all'},  # Opción para seleccionar todas las aerolíneas
                ] + [
                    {'label': carrier, 'value': carrier}
                    for carrier in df['Carrier'].unique()
                ],
                value='all'  # Valor predeterminado: "todos"
            ),
        ], className="four columns"),
    ], className="row"),
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
        title_bar = 'Cantidad de DepDel15 True en Todos los Aeropuertos'
    else:
        # Filtra el DataFrame en función del valor seleccionado en el menú de aeropuertos
        df_filtrado = df[df['AirportID'] == airport_id]
        title_bar = f'Cantidad de DepDel15 True en el Aeropuerto {airport_id}'

    if carrier == 'all':
        # Si se selecciona "todos" en el menú de aerolíneas, se muestra un gráfico con todos los datos
        title_pie = 'Proporción de Vuelos Retrasados y No Retrasados en Todas las Aerolíneas'
    else:
        # Filtra el DataFrame en función del valor seleccionado en el menú de aerolíneas
        df_filtrado = df_filtrado[df_filtrado['Carrier'] == carrier]
        title_pie = f'Proporción de Vuelos Retrasados y No Retrasados para la Aerolínea {carrier}'

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
            'yaxis': {'title': 'Cantidad DepDel15 True'},
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