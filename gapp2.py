import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

# Step 1. Launch the application
app = dash.Dash(__name__)
# Step 2. Import the dataset
clean_df = pd.read_csv("Resources/clean.csv")

clean_df['Year'],clean_df['Month'],clean_df['Day']= clean_df['timestamp'].str.split('-',2).str

clean_df['Year'] = pd.to_numeric(clean_df['Year'])
clean_df['Month'] = pd.to_numeric(clean_df['Month'])
clean_df['Day'] = pd.to_numeric(clean_df['Day'])

# Step 3. Create a plotly figure
trace_1 = go.Scatter(x = st.Year, y = st['Ticker'],
                    name = 'Ticker',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
layout = go.Layout(title = 'Time Series Plot',
                   hovermode = 'closest')
fig = go.Figure(data = [trace_1], layout = layout)

# Step 4. Create a Dash layout
app.layout = html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1("This is my first dashboard"),
                    html.P("")
                         ], 
                    style = {'padding' : '50px' , 
                             'backgroundColor' : '#3aaab2'}),
# adding a plot        
                dcc.Graph(id = 'plot', figure = fig)
                      ])
# Step 5. Add callback functions


# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug = True)
