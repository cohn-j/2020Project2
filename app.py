import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

clean_df = pd.read_csv("clean.csv")

app.layout = html.Div([

    html.H1("Web App Dashboard with Dash", style={'text-align':'center'}),

    dcc.Dropdown(id="slct_year", 
                options=[
                    {'label':'Financial Services', 'value':2015},
                    {'label':'Consumer Cyclical', 'value':2016},
                    {'label':'Healthcare', 'value':2017},                    
                    {'label':'Energy', 'value':2018},
                    {'label':'Technology', 'value':2018},
                    {'label':'Industrials', 'value':2018},
                    {'label':'Communication Services', 'value':2018}],
                multi=False,
                value='2015',
                style={'width':'40%'},
                placeholder="Select a sector",
                ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_graph', figure={})

])  

@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='my_graph', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The sector chosen by user was: {}".format(option_slctd)

    dff = clean_df.copy()
    dff = dff[dff["Sector"] == option_slctd]
    dff = dff[dff["Sector"] == "Financial Services"]

    # Plotly Express
    # fig = px.choropleth(
    #     data_frame=dff,
    #     locationmode='USA-states',
    #     locations='state_code',
    #     scope="usa",
    #     color='Pct of Colonies Impacted',
    #     hover_data=['State', 'Pct of Colonies Impacted'],
    #     color_continuous_scale=px.colors.sequential.YlOrRd,
    #     labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
    #     template='plotly_dark'
    # )

    # Plotly Graph Objects (GO)
    fig = go.Figure(
        data=[go.Candlestick(x=dff['timestamp'],
                open=dff['open'],
                high=dff['high'],
                low=dff['low'],
                close=dff['close']
                )])
    
    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)
