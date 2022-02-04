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
    html.H2("Thống kê giá trị giao dịch cổ phiếu theo năm", style= {'textAlign': 'center'}),
    
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
    dcc.Graph(
        id= 'gtgd',
        figure= {}
    )
])

@app.callback(
    Output('gtgd', 'figure'),
    [Input('year-dpdn1', 'value'),
     Input('year-dpdn2', 'value')]
)
def update_graph(year1, year2):
    dff = df.set_index("Năm").loc[year1: year2]
    
    gtgd = make_subplots(specs= [[{"secondary_y": True}]])
    
    for col in dff.columns[6:10]:
        if col == "GTGD Bình quân phiên cổ phiếu (ngàn tỷ đồng)":
            gtgd.add_trace(
                go.Scatter(
                    #dff,
                    x= dff.index,
                    y= dff['GTGD Bình quân phiên cổ phiếu (ngàn tỷ đồng)'],
                    name= 'GTGD Bình quân phiên cổ phiếu (ngàn tỷ đồng)',
                    mode= 'lines'),
                secondary_y= True
                )
        else:
            gtgd.add_trace(
                go.Bar(
                    #dff,
                    x= dff.index,
                    y= dff.loc[:, col],
                    name= col
                ),
                secondary_y= False
            )
    newnames = {
    'Tổng GTGD cổ phiếu (ngàn tỷ đồng)': "Tổng GTGD",
    'GTGD Bình quân phiên cổ phiếu (ngàn tỷ đồng)': "GTGD Bình quân",
    'GTGD Mua cổ phiếu của NĐTNN (ngàn tỷ đồng)': "GTGD Mua",
    'GTGD Bán cổ phiếu của NĐTNN (ngàn tỷ đồng)': "GTGD Bán"
    }
    gtgd.for_each_trace(lambda t: t.update(name= newnames[t.name],
                                       legendgroup= newnames[t.name]))
    gtgd.update_layout(
            template= 'presentation',
            legend= dict(
                orientation= "h",
                #yanchor= "top",
                y= -0.2,
                #xanchor= "center",
                #x= 0.5
            )
        )
    gtgd.update_layout(title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, 
                           height= 500)
    gtgd.update_layout(margin=dict(l=60, r=30, t=20, b=100))
    gtgd.add_annotation(dict(font=dict(color='black',size=15),
                                        x=0,
                                        y=-0.2,
                                        showarrow=False,
                                        text="ĐVT: Ngàn tỷ đồng",
                                        textangle=0,
                                        #xanchor='left',
                                        xref="paper",
                                        yref="paper"))
    
    return gtgd
