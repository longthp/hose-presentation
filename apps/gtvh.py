import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("data.csv"))

df.iloc[1:, -1] = df.iloc[1:, -1].apply(lambda x: x.replace(',', ''))
df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1])

layout = html.Div([
    html.H2("Giá trị vốn hóa thị trường cổ phiếu theo năm", style= {'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            dcc.Dropdown(
                id= 'year-dpdn1',
                options= [{'label': i, 'value': i} for i in df['Năm']],
                value= '7/28/2000',
                clearable= False,
            )
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id= 'year-dpdn2',
                options= [{'label': i, 'value': i} for i in df['Năm']],
                value= '6/1/2021',
                clearable= False
            )
        ], style={'width': '49%', 'display': 'inline-block'})
    ], className= 'row'),
    
    dcc.Graph(
        id= 'gtvh',
        figure= {}
    )
])

@app.callback(
    Output('gtvh', 'figure'),
    [Input('year-dpdn1', 'value'), 
     Input('year-dpdn2', 'value')]
)
def update_graph(year1, year2):
    dff = df.set_index("Năm").loc[year1:year2]
    
    gtvh = px.bar(
                dff,
                x= dff.index, 
                y= dff.iloc[:, 5],
                text= dff.iloc[:, 5],
                hover_name= dff.index,
                color_discrete_sequence= ['dodgerblue'],
                height= 500,
                labels= {'y': '', 'x': '', 'Năm': ''},
                template= 'plotly'
            )
    gtvh.update_layout(title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, hovermode= 'x')
    gtvh.update_traces(textposition= 'outside', texttemplate= "%{text:.3s}", hovertemplate=None)
    
    return gtvh