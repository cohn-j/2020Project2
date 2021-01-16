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
clean_df['timestamp'] = pd.to_datetime(clean_df['timestamp'])

dates = ['2015-02-17', '2015-05-17', '2015-08-17', '2015-11-17',
         '2016-02-17', '2016-05-17', '2016-08-17', '2016-11-17',  
         '2017-02-17']
date_mark = {i : dates[i] for i in range(0, 9)}

# print(clean_df)

# url="https://raw.githubusercontent.com/cohn-j/2020Project2/blob/dev/clean.csv"
# s=requests.get(url).content
# clean_df = pd.read_csv(io.StringIO(s.decode('utf-8')))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

trace_1 = go.Scatter(x = clean_df.Year, y = clean_df['close'],
                    name = 'Ticker',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layout = go.Layout(title = 'Time Series Plot',
                   hovermode = 'closest')
fig = go.Figure(data = [trace_1], layout = layout)

available_indicators = clean_df['Sector'].unique()

app.layout = html.Div([    
                # a header and a paragraph
                html.Div([
                    html.P("Time Series Plot")
                         ],
                     style = {'padding' : '50px' ,
                              'backgroundColor' : '#3aaab2'}),
                # adding a plot
    dcc.Graph(id='plot', figure= fig),
    dcc.Slider(
            id='year-slider',
            min=clean_df['Year'].min(),
            max=clean_df['Year'].max(),
            value=clean_df['Year'].min(),
            marks={str(y): str(y) for y in clean_df['Year'].unique()},
            step=None
    ),

    dcc.Dropdown(
        id='dropdown',
        options= [{'label' : i, 'value' : i} for i in available_indicators],
        multi=False,
        value='',
        style={'width':'40%'},
        placeholder="Select sector"
    )
])  

@app.callback(
    # Output('output_container', 'children'),
    Output('plot', 'figure'),
    Input('year-slider', 'value'),
    Input('dropdown', 'value')
)
# def update_graph(xaxis_column_name, yaxis_column_name, year_value):
def update_figure(input1, input2):

    # filtering the data
    clean_df2 = clean_df[(clean_df.Year > dates[input2[0]]) & (clean_df.Date < dates[input2[1]])]

    # filtered_df = clean_df[clean_df.Year == selected_year]
    # dff = clean_df[clean_df['Year'] == year_value]
    trace_1 = go.Scatter(x = clean_df2.Year, y = st2['Ticker'],
                        name = 'Ticker',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'))
    
    trace_2 = go.Scatter(x = clean_df.Year, y = clean_df[input1],
                        name = input1,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    fig = go.Figure(data = [trace_1, trace_2], layout = layout)
    return fig


    # fig = px.scatter(filtered_df, x="Year", y="close",
    #                  size="volume", color="Sector", hover_name="Ticker",
    #                  log_x=False, size_max=55)

    fig.update_layout(transition_duration=500)                 

   
    
    # fig.update_xaxes(title=xaxis_column_name)

    # fig.update_yaxes(title=yaxis_column_name)


    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
