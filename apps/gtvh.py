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
    html.Br(),
    html.Div([
        dcc.Graph(
        id= 'gtvh',
        figure= {},
        config= {
            'displaylogo': False,
            'displayModeBar': False
            }
        )
    ])
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
                height= 500,
                labels= {'y': '', 'x': '', 'Năm': ''},
                template= 'plotly_white'
            )
    gtvh.update_layout(
        hovermode= 'x',
        margin= dict(l=60, r=30, t=20, b=100), 
        yaxis= dict(fixedrange= True)
    )
    gtvh.update_traces(textposition= 'outside', texttemplate= "%{text:.3s}", hovertemplate=None)
    gtvh.add_annotation(dict(font=dict(color='black',size=15),
                                        x=0,
                                        y=-0.2,
                                        showarrow=False,
                                        text="ĐVT: Ngàn tỷ đồng",
                                        textangle=0,
                                        xanchor='left',
                                        xref="paper",
                                        yref="paper"))
    return gtvh
