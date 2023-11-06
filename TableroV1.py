import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

# Inicializa la aplicación Dash
app = dash.Dash(__name__)

# Carga los datos desde el archivo CSV "merged_data.csv"
df = pd.read_csv("C:\\Users\\camab\\OneDrive\\Documentos\\Maestria Andes\\6toCiclo\\Despliegue\\merged_data (1).csv")

# Define el diseño del tablero
app.layout = html.Div([
    html.H1("Programa tu vuelo", style={'text-align': 'center', 'color': 'blue'}),  # Título centrado y en azul
    dcc.Graph(id="line-chart"),  # Gráfico de línea
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Opción 1', 'value': 'opcion1'},
            {'label': 'Opción 2', 'value': 'opcion2'}
        ],
        value='opcion1'
    )
])

# Define una función para actualizar el gráfico de línea
@app.callback(
    Output("line-chart", "figure"),
    Input("dropdown", "value")
)
def update_line_chart(selected_value):
    # Filtra los datos según la opción seleccionada
    if selected_value == 'opcion1':
        filtered_df = df  # Puedes ajustar la lógica de filtrado según tus necesidades
    else:
        filtered_df = df  # Otra lógica de filtrado si es necesario

    # Crea el gráfico de línea
    figure = {
        'data': [
            {
                'x': filtered_df['Month'] + filtered_df['Day'],  # Eje X (Mes + Día)
                'y': filtered_df['WindSpeed'],  # Datos de la columna "WindSpeed"
                'type': 'line',
                'name': 'Velocidad del Viento',
            }
        ],
        'layout': {
            'title': 'Gráfico de Velocidad del Viento por Día y Mes',
            'xaxis': {'title': 'Fecha'},
            'yaxis': {'title': 'Velocidad del Viento'},
        }
    }

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
