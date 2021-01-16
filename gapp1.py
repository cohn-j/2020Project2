import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import requests
import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import io

app = dash.Dash(__name__)

clean_df = pd.read_csv("Resources/clean.csv")

clean_df['Year'],clean_df['Month'],clean_df['Day']= clean_df['timestamp'].str.split('-',2).str

clean_df['Year'] = pd.to_numeric(clean_df['Year'])
clean_df['Month'] = pd.to_numeric(clean_df['Month'])
clean_df['Day'] = pd.to_numeric(clean_df['Day'])

# print(clean_df)

# url="https://raw.githubusercontent.com/cohn-j/2020Project2/blob/dev/clean.csv"
# s=requests.get(url).content
# clean_df = pd.read_csv(io.StringIO(s.decode('utf-8')))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



available_indicators = clean_df['Sector'].unique()

app.layout = html.Div([
    html.H1("Stock Data by Sectors", style={'text-align':'center'}),
    
    # dcc.Dropdown(
    #             id='dropdown', 
    #             options=[{'label': i, 'value': i} for i in available_indicators],
    #             multi=False,
    #             value='Industrials',
    #             style={'width':'40%'},
    #             placeholder="Select a Sector",
    #             ),
    dcc.Graph(id='my_graph', figure={}),
    dcc.Slider(
            id='year-slider',
            min=clean_df['Year'].min(),
            max=clean_df['Year'].max(),
            value=clean_df['Year'].min(),
            marks={str(y): str(y) for y in clean_df['Year'].unique()},
            step=None
    ),
    
    

])  

@app.callback(
    # Output('output_container', 'children'),
    Output('my_graph', 'figure'),
    Input('year-slider', 'value'),
    # Input('dropdown', 'value')
)
# def update_graph(xaxis_column_name, yaxis_column_name, year_value):
def update_figure(selected_year):
    filtered_df = clean_df[clean_df.Year == selected_year]
    # dff = clean_df[clean_df['Year'] == year_value]
    
    fig = px.scatter(filtered_df, x="Year", y="close",
                     size="volume", color="Sector", hover_name="Ticker",
                     log_x=False, size_max=55)

    fig.update_layout(transition_duration=500)                 

   
    
    # fig.update_xaxes(title=xaxis_column_name)

    # fig.update_yaxes(title=yaxis_column_name)


    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
