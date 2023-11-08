import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Cargar tus datos
df = pd.read_csv("C:\\Users\\camab\\OneDrive\\Documentos\\Maestria Andes\\6toCiclo\\Despliegue\\merged_data (1).csv")

# Total de vuelos analizados
total_vuelos = len(df)  # Obtiene el número total de filas en el DataFrame



# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Define el diseño del tablero
app.layout = html.Div([
    html.H1("Programa tu vuelo", style={'text-align': 'center', 'color': 'blue'}),  # Título centrado y en azul
    html.Div(f"TOTAL meses: {total_vuelos}", style={'text-align': 'center',}),
    html.Div(
    [
        html.H2("TOTAL VUELOS ANALIZADOS:", style={'text-align': 'lefth', 'font-weight': 'bold'}),
        html.Hr(),  # Agregar una línea horizontal
        html.Div(f"{total_vuelos:.2f}", style={'text-align': 'center'}),]),
    dcc.Graph(id="line-chart"),  # Gráfico de línea
    dcc.Graph(id="scatter-chart"),  # Gráfico de dispersión
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Opción 1', 'value': 'opcion1'},
            {'label': 'Opción 2', 'value': 'opcion2'}
        ],
        value='opcion1'
    )
])

# Define una función para actualizar el gráfico de línea y el gráfico de dispersión
@app.callback(
    [Output("line-chart", "figure"), Output("scatter-chart", "figure")],
    Input("dropdown", "value")
)
def update_charts(selected_value):
    # Filtra los datos según la opción seleccionada
    if selected_value == 'opcion1':
        filtered_df = df  # Puedes ajustar la lógica de filtrado según tus necesidades
    else:
        filtered_df = df  # Otra lógica de filtrado si es necesario

    # Crea el gráfico de línea
    line_figure = px.line(
        filtered_df,
        x='Month',
        y='WindSpeed',
        title='Gráfico de Velocidad del Viento por Mes',
        labels={'Month': 'Mes', 'WindSpeed': 'Velocidad del Viento'}
    )

    # Crea el gráfico de dispersión
    vuelos_por_semana = df['DayOfWeek'].value_counts().reset_index()
    vuelos_por_semana.columns = ['DayOfWeek', 'Numero de Vuelos']
    
    scatter_figure = px.scatter(vuelos_por_semana, x='DayOfWeek', y='Numero de Vuelos', labels={'DayOfWeek': 'Día de la Semana', 'Numero de Vuelos': 'Número de Vuelos'})

    return line_figure, scatter_figure

if __name__ == '__main__':
    app.run_server(debug=True, port=8061)