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

# app layout
layout = html.Div([
    html.H2("Số mã chứng khoán niêm yết mới theo năm", style= {'textAlign': 'center'}),
    
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
    html.Br(),
    html.Div([
        dcc.Graph(
            id= 'smck',
            figure= {},
            config= {
                'displaylogo': False,
                'displayModeBar': False
            }
        )
    ])
])

@app.callback(
    Output('smck', 'figure'),
    [Input('year-dpdn1', 'value'),
     Input('year-dpdn2', 'value')]
)
def update_graph(year1, year2):
    dff = df.set_index("Năm").loc[year1: year2]
    
    smck = make_subplots(specs= [[{"secondary_y": False}]])

    for col in dff.columns[0:5]:
        smck.add_trace(
                go.Bar(x= dff.index, y= dff.loc[:, col], name= col)
            )

    smck.update_layout(
        template= 'plotly_white',
        height= 500,
        margin=dict(l=60, r=30, t=20, b=100), 
        yaxis= dict(fixedrange= True),
        legend= dict(
            orientation= 'h',
            y= -0.2
        )
    )
    
    return smck
