import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import datetime as dt
import numpy as np
import plotly.express as px
import random


df = pd.read_csv('resultado_merge.csv')

app = dash.Dash(__name__)

# Agrega una columna 'Cancelled' en formato numérico (0 o 1) para contar las cancelaciones
df['Cancelled'] = df['Cancelled'].astype(int)


def generate_random_color(n):
    color_list = []
    for i in range(n):
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        color_list.append(color)
    return color_list


def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            #html.H5("Proyecto DSA Grupo 5"),
            html.H3("Predicción de retrasos en vuelos"),
            html.Div(
                id="intro",
                children="Esta interfaz proporciona a los operadores de aeropuertos una herramienta integral para prever y gestionar retrasos en vuelos. Los usuarios pueden ingresar información de las torres de control como datos de vuelos y condiciones climáticas para obtener predicciones precisas de posibles retrasos. Las visualizaciones del comportamiento histórico ayudan a equilibrar la distribución de pistas de embarque y optimizar la toma de decisiones operativas. Los datos históricos se obtienen del Buró de Estadísticas de Transporte del Departamento de Transporte de los Estados Unidos (DOT) quien realiza un seguimiento puntual de los vuelos nacionales operados por grandes transportistas aéreos."
            ),
        ],
    )


def create_counters():
    """
    :return: A Div containing descriptive counters.
    """
    return html.Div([
        html.Div([
            html.P(f"Número de aeropuertos: ", id='aeropuertos-counter'),
            html.P(f"Número de aerolíneas: ", id='aerolineas-counter'),       
        ], className="four columns", style={'width': '48%'}),
        html.Div([
            html.P(f"Número de vuelos: ", id='vuelos-counter'),
            html.P(f"Número de retrasos en la historia: ", id='retrasos-counter'),     
        ], className="four columns", style={'width': '48%'}),
    ], className="row")
    

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
                    html.P("Fecha:", style=dict(width='10%', textAlign='center', margin='1%')),
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
                        style=dict(width='95%', display='inline-block', margin='1%')
                    )
                ],
                style=dict(display='flex', width='95%')
            ),
            html.Div([
                    html.Label('Selecciona un aeropuerto origen:'),
                    dcc.Dropdown(
                        id='airport-dropdown-control-origin',
                        options=[
                            {'label': 'Todos', 'value': 'all'},  # Opción para seleccionar todos los aeropuertos
                        ] + [
                            {'label': df[df['AirportID'] == airport_id].iloc[0]['AeropuertoOrigen'], 'value': airport_id}
                            for airport_id in df['AirportID'].unique()
                        ],
                        value='all',  # Valor predeterminado: "todos"
                        style={'width': '100%'}
                    ),
                ], className="four columns", style={'width': '95%', 'margin':'1%'}
            ),
            html.Div([
                    html.Label('Selecciona un aeropuerto destino:'),
                    dcc.Dropdown(
                        id='airport-dropdown-control-destiny',
                        options=[
                            {'label': 'Todos', 'value': 'all'},  # Opción para seleccionar todos los aeropuertos
                        ] + [
                            {'label': df[df['DestAirportID'] == airport_id].iloc[0]['AeropuertoDestino'], 'value': airport_id}
                            for airport_id in df['DestAirportID'].unique()
                        ],
                        value='all',  # Valor predeterminado: "todos"
                        style={'width': '100%'}
                    ),
                ], className="four columns", style={'width': '95%', 'margin':'1%'}
            ),
            html.Div([
                    html.Label('Selecciona una aerolínea:'),
                    dcc.Dropdown(
                        id='carrier-dropdown-control',
                        options=[
                            {'label': 'Todos', 'value': 'all'},  # Opción para seleccionar todas las aerolíneas
                        ] + [
                            {'label': df[df['Carrier'] == carrier].iloc[0]['Aerolinea'], 'value': carrier}
                            for carrier in df['Carrier'].unique()
                        ],
                        value='all',  # Valor predeterminado: "todos"
                        style={'width': '100%'}
                    ),
                ], className="four columns", style={'width': '95%', 'margin':'1%'}
            ),
            html.Div(
                id="componente-slider",
                children=[
                    html.P("Velocidad del Viento (m/s):", style=dict(width='100%', textAlign='left', margin='1%')),
                    dcc.Slider(
                        id='slider-viento',
                        min=0,
                        max=10,
                        step=0.5,
                        value=5,
                        marks={
                            0: {'label': '0m/s', 'style': {'color': '#8fce00'}},
                            5: {'label': '5m/s', 'style': {'color': '#ffd966'}},
                            10: {'label': '10m/s', 'style': {'color': '#f50'}}
                        }
                    )
                ],
                style=dict(width='95%', display='inline-block', margin='1%')
            ),
            html.Div(
                id="componente-slider2",
                children=[
                    html.P("Humedad Relativa (%):", style=dict(width='100%', textAlign='left', margin='1%')),
                    dcc.Slider(
                        id='slider-humedad',
                        min=0,
                        max=100,
                        step=1,
                        value=50,
                        marks={
                            0: {'label': '0%', 'style': {'color': '#8fce00'}},
                            50: {'label': '50%', 'style': {'color': '#ffd966'}},
                            100: {'label': '100%', 'style': {'color': '#f50'}}
                        }
                    )
                ],
                style=dict(width='95%', display='inline-block', margin='1%')
            ),
            html.Div(
                id="componente-slider3",
                children=[
                    html.P("Temperatura (de bulbo húmedo °C):", style=dict(width='100%', textAlign='left', margin='1%')),
                    dcc.Slider(
                        id='slider-temperaturabulbo',
                        min=0,
                        max=50,
                        step=1,
                        value=25,
                        marks={
                            0: {'label': '0°C', 'style': {'color': '#8fce00'}},
                            25: {'label': '25°C', 'style': {'color': '#ffd966'}},
                            50: {'label': '50°C', 'style': {'color': '#f50'}}
                        }
                    )
                ],
                style=dict(width='95%', display='inline-block', margin='1%')
            ),
            html.Div(
                id="componente-slider4",
                children=[
                    html.P("Temperatura (de punto de rocío °C):", style=dict(width='100%', textAlign='left', margin='1%')),
                    dcc.Slider(
                        id='slider-temperaturarocio',
                        min=-50,
                        max=50,
                        step=1,
                        value=0,
                        marks={
                            -50: {'label': '-50°C', 'style': {'color': '#8fce00'}},
                            0: {'label': '0°C', 'style': {'color': '#ffd966'}},
                            50: {'label': '50°C', 'style': {'color': '#f50'}}
                        }
                    )
                ],
                style=dict(width='95%', display='inline-block', margin='1%')
            ),
            html.Div(
                id="componente-slider5",
                children=[
                    html.P("Presión estacionaria (hPa):", style=dict(width='100%', textAlign='left', margin='1%')),
                    dcc.Slider(
                        id='slider-stationpressure',
                        min=20,
                        max=40,
                        step=0.1,
                        value=30,
                        marks={
                            20: {'label': '20hPa', 'style': {'color': '#8fce00'}},
                            30: {'label': '30hPa', 'style': {'color': '#ffd966'}},
                            40: {'label': '40hPa', 'style': {'color': '#f50'}}
                        }
                    )
                ],
                style=dict(width='95%', display='inline-block', margin='1%')
            ),
            html.Div(
                id="componente-slider6",
                children=[
                    html.P("Altimetro (inHg):", style=dict(width='100%', textAlign='left', margin='1%')),
                    dcc.Slider(
                        id='slider-altimeter',
                        min=20,
                        max=40,
                        step=0.1,
                        value=30,
                        marks={
                            20: {'label': '20inHg', 'style': {'color': '#8fce00'}},
                            30: {'label': '30inHg', 'style': {'color': '#ffd966'}},
                            40: {'label': '40inHg', 'style': {'color': '#f50'}}
                        }
                    )
                ],
                style=dict(width='95%', display='inline-block', margin='1%')
            ),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Div([
                html.Div([
                    html.Button('Predecir Retraso', id='my-button', className='my-button-class', n_clicks=0, style=dict(width='100%', height='5%', display='inline-block', marginBottom='5%')),
                ], className="four columns", style={'width': '48%'}),
                html.Div([
                    dcc.Markdown(children='TRUE o FALSE', id='prediction-output', className='my-predresult-class', style={"width":'50%', "height":'10%', "display":'inline-block', "margin-left":'10%', "margin-top":'1%', "margin-bottom":'5%', 'textAlign':'center'})
                ], className="four columns", style={'width': '48%'}),
            ], className="row"),
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
    create_counters(),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(id='bar-chart')
        ], className="six columns"),
        html.Div([
            dcc.Graph(id='pie-chart')
        ], className="six columns"),
    ], className="row"),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(id='bar-chart2')
        ], className="six columns"),
        html.Div([
            dcc.Graph(id='pie-chart2')
        ], className="six columns"),
    ], className="row")
])


# Define la interfaz de usuario con los menús desplegables, los gráficos de barras y el gráfico de pastel
app.layout = html.Div(
    id="app-container",
    style={'zoom': '75%'},
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


# Crea una función de callback para actualizar los gráficos y contadores en función de las selecciones en los menús desplegables
@app.callback(
    [Output('bar-chart', 'figure'), Output('pie-chart', 'figure'), Output('bar-chart2', 'figure'), Output('pie-chart2', 'figure'), 
     Output('aeropuertos-counter', 'children'), Output('aerolineas-counter', 'children'), Output('vuelos-counter', 'children'), Output('retrasos-counter', 'children')],
    [Input('airport-dropdown', 'value'), Input('carrier-dropdown', 'value')]
)
def actualizar_graficos_y_contadores(airport_id, carrier):
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

    # Agrupa los datos por Month_Day y cuenta la cantidad de DepDel15 True
    data_bar = df_filtrado.groupby('Day')['DepDel15'].sum().reset_index()

    # Use the function to generate a list of 31 random colors
    custom_colors = generate_random_color(31)

    # Crea el gráfico de barras
    fig_bar = {
        'data': [
            {'x': data_bar['Day'], 'y': data_bar['DepDel15'], 'type': 'bar', 'name': 'DepDel15 True', 'marker': {'color': custom_colors}},
        ],
        'layout': {
            'title': title_bar,
            'xaxis': {'title': 'Día del mes'},
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
                marker=dict(colors=px.colors.qualitative.Set1)

            ),
        ],
        'layout': {
            'title': title_pie,
        }
    }

    # Agrupa los datos por DayOfWeek y cuenta la cantidad de DepDel15 True
    data_bar2 = df_filtrado.groupby('DayOfWeek')['DepDel15'].sum().reset_index()

    # Create a dictionary for the mapping
    mapping_dict = {
        1: 'lunes',
        2: 'martes',
        3: 'miercoles',
        4: 'jueves',
        5: 'viernes',
        6: 'sabado',
        7: 'domingo'
    }

    # Map the values in the 'DayOfWeek' column to their corresponding Spanish names
    data_bar2['DayOfWeek'] = data_bar2['DayOfWeek'].map(mapping_dict)

    colores = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)', 'rgb(148, 103, 189)',
                    'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

    fig_line = {
        'data': [
            {'x': data_bar2['DayOfWeek'], 'y': data_bar2['DepDel15'], 'type': 'line', 'name': 'DepDel15 True', 'marker': {'color': colores}},
        ],
        'layout': {
            'title': title_bar+'<br> dependiendo del día de la semana',
            'xaxis': {'title': 'Día de la semana'},
            'yaxis': {'title': 'Cantidad de Retrasos'},
        }
    }


    # Calcula la temperatura promedio por día de la semana
    vuelos_por_dia = df_filtrado.value_counts('Day').reset_index()
    vuelos_por_dia.rename(columns={vuelos_por_dia.columns[1]: 'Cantidad Vuelos'}, inplace=True)

    # Crea el gráfico de barras
    fig = px.bar(vuelos_por_dia, x="Day", y="Cantidad Vuelos", title=title_bar.replace('Cantidad de retrasos', 'Cantidad de vuelos'), 
                labels={'Day': 'Día del mes', 'Day':'Día del mes'}, color="Cantidad Vuelos",
                )
    
   
    aeropuertos_count = len(df_filtrado['AirportID'].unique())
    aerolineas_count = len(df_filtrado['Carrier'].unique())
    vuelos_count = df_filtrado.shape[0]

    return fig_bar, fig_pie, fig_line, fig, f"Número de aeropuertos: {aeropuertos_count}", f"Número de aerolíneas: {aerolineas_count}", f"Número de vuelos: {vuelos_count}", f"Vuelos retrasados: {vuelos_retrasados}"




# Ejecuta la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)


# Poner controles de entrada para predicción.
# Poner sección de referenciación de datos.
# Cambiar colores del tema? 