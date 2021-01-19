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
#added
import flask
import os
from flask import Flask



# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

clean_df = pd.read_csv("Resources/clean.csv")

df_tree = pd.read_csv("overview.csv")

# clean_df['Year'],clean_df['Month'],clean_df['Day']= clean_df['timestamp'].str.split('-',2).str

# clean_df['Year'] = pd.to_numeric(clean_df['Year'])
# clean_df['Month'] = pd.to_numeric(clean_df['Month'])
# clean_df['Day'] = pd.to_numeric(clean_df['Day'])

clean_df['Year'],clean_df['Month'],clean_df['Day']= clean_df['timestamp'].str.split('-',2).str
clean_df['Year'] = pd.to_numeric(clean_df['Year'])
clean_df['Month'] = pd.to_numeric(clean_df['Month'])
clean_df['Day'] = pd.to_numeric(clean_df['Day'])
clean_df['timestamp'] = pd.to_datetime(clean_df['timestamp'], format='%Y%m%d', errors='ignore')

#added
server = Flask(__name__)
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# print(clean_df)

# url="https://raw.githubusercontent.com/cohn-j/2020Project2/blob/dev/clean.csv"
# s=requests.get(url).content
# clean_df = pd.read_csv(io.StringIO(s.decode('utf-8')))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



available_indicators = clean_df['Sector'].unique()

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        {%favicon%}
        {%scripts%}
        {%css%}

    </head>
    <body> 

            {%app_entry%}
        <footer>
            {%config%}
            {%renderer%}          
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    
    html.H1("Stock Sector Dashboard", style={'text-align':'center'}),
    
    html.Div([
        dcc.Graph(id='treemap',figure = {})
        ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),    
    
    # dcc.Dropdown(
    #             id='dropdown', 
    #             options=[{'label': i, 'value': i} for i in available_indicators],
    #             multi=False,
    #             value='Industrials',
    #             style={'width':'40%'},
    #             placeholder="Select a Sector",
    #             ),
    html.Div([
        dcc.Graph(id='my_graph', figure={}),
    ]),
    html.Div([
        dcc.Slider(
            id='year-slider',
            min=clean_df['Year'].min(),
            max=clean_df['Year'].max(),
            value=clean_df['Year'].min(),
            marks={str(y): str(y) for y in clean_df['Year'].unique()},
            step=None
        )
        ]),

    html.Div([
        dcc.Dropdown(
        id='dropdown',
        options=[
            {'label':'Financial Services', 'value':'Financial Services'},
            {'label':'Energy', 'value':'Energy'}, 
            {'label':'Communication Services', 'value':'Communication Services'}, 
            {'label':'Healthcare', 'value':'Healthcare'}, 
            {'label':'Technology', 'value':'Technology'}, 
            {'label':'Consumer Cyclical', 'value':'Consumer Cyclical'},
            {'label':'Industrials', 'value':'Industrials'} 
        ],
        value='Financial Services'
        ),
    ]),
    html.Div([
       dcc.Graph(id='candle', figure = {})
    ], 
    style = {'width': '100%', 'height': '600px'}),

    html.Div([html.A(html.Button('Click to view more plotting!', className='three columns'),
    href='static/candle.html', target='_blank')])
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
    fig = px.scatter(filtered_df, x="timestamp", y="close",
                     size="volume", color="Sector", hover_name="Ticker",
                     log_x=False, size_max=55)
    fig.update_layout(title = 'Monthly Closing Price per Stock per Sector', transition_duration=500)             

   
    
    # fig.update_xaxes(title=xaxis_column_name)

    # fig.update_yaxes(title=yaxis_column_name)


    return fig

@ app.callback(
    Output('treemap','figure'),
    Input ('treemap', 'value')
    )    
def update_treemap(value):


  fig2 = px.treemap(df_tree, path=['Sector','Ticker'], 
  values=df_tree["MarketCapitalization"],
  hover_data = ['MarketCapitalization'])

  fig2.update_layout(title='Treemap',
  treemapcolorway=['green', 'lightgreen'])
  
  return fig2

@ app.callback(
    Output('candle','figure'),
    Input('dropdown','value')
)
def update_candle(selected_sector):
    dff = clean_df.copy()
    fin_df = dff[dff["Sector"] == selected_sector]
    fig3 = go.Figure(data=[go.Candlestick(x=fin_df['timestamp'],
                open=fin_df['open'],
                high=fin_df['high'],
                low=fin_df['low'],
                close=fin_df['close'],
                increasing_line_color= 'lightgreen', 
                decreasing_line_color= 'gray',
                name=selected_sector,
                showlegend=True,
                visible=True,
                ids=['Financial Services','Energy','Healthcare','Consumer Cyclical','Communication Services','Technology'],
                hovertext=fin_df['Ticker']
                )])
    fig3.update_layout(
        title='Candlestick',
        yaxis_title=selected_sector
#         xaxis_rangeslider_visible='slider' in value
    )

    return fig3


@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)
  
if __name__ == '__main__':
    app.run_server(debug=True)
