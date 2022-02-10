import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash
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
df = df.set_index("Năm")
# df.iloc[1:, -1] = df.iloc[1:, -1].apply(lambda x: x.replace(',', ''))
# df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1])

# app layout
layout = html.Div([
    html.H2("Thống kê giá trị giao dịch cổ phiếu theo năm", style= {'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            dcc.Dropdown(
                id= 'year-dpdn1',
                options= [{'label': i, 'value': i} for i in df.index],
                value= '7/28/2000',
                clearable= False,
            )
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id= 'year-dpdn2',
                options= [{'label': i, 'value': i} for i in df.index],
                value= '6/1/2021',
                clearable= False
            )
        ], style={'width': '49%', 'display': 'inline-block'})
    ], className= 'row'),
    #html.Br(),
    html.Div([
        dcc.Checklist(
            id= 'check-list',
            options= [
                    {'label': 'Tổng GTGD', 'value': 'Tổng GTGD cổ phiếu (ngàn tỷ đồng)'},
                    {'label': 'GTGD Bình quân', 'value': 'GTGD Bình quân phiên cổ phiếu (ngàn tỷ đồng)'},
                    {'label': 'GTGD Mua', 'value': 'GTGD Mua cổ phiếu của NĐTNN (ngàn tỷ đồng)'},
                    {'label': 'GTGD Bán', 'value': 'GTGD Bán cổ phiếu của NĐTNN (ngàn tỷ đồng)'}
                ],
            value= df.columns[6:10],
            style={'display':'flex', 'align-items': 'center', 'justify-content': 'center'},
            inputStyle={'cursor':'pointer', 'margin-right': '10px'},
            labelStyle={'background':'white',
                        'padding':'0.5rem 1rem',
                        'border-radius':'0.25rem',
                        'margin-right': '5px',
                        },
        )
    ], className= 'row mt-2'),
    #html.Br(),
    html.Div([
        dcc.Graph(
            id= 'gtgd',
            figure= {},
            config= {
    'displaylogo': False,
    'displayModeBar': False
            }
        ),
    ], className= 'mt-2')
])

@app.callback(
    Output('gtgd', 'figure'),
    [Input('year-dpdn1', 'value'),
     Input('year-dpdn2', 'value'),
     Input('check-list', 'value')]
)
def update_graph(year1, year2, checkitem):
    if pd.to_datetime(year1) <= pd.to_datetime(year2):
        dff = df.loc[year1: year2, df.columns.isin(checkitem)]
        
        traceColors= ['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
        colorMap = {col: i for col, i in zip(df.columns[6:10], traceColors)}
        
        gtgd = go.Figure()
        
        for col in dff.columns:
            if col != "GTGD Bình quân phiên cổ phiếu (ngàn tỷ đồng)":
                gtgd.add_trace(go.Bar(x= dff.index, y= dff.loc[:, col], name= col,
                                      marker= dict(color= colorMap[col])))
            else:
                gtgd.add_trace(go.Scatter(x= dff.index, y= dff.loc[:, col], 
                                          name= col, mode= 'lines', yaxis= 'y2',
                                          marker= dict(color= colorMap[col])))
        
        newnames = {
        'Tổng GTGD cổ phiếu (ngàn tỷ đồng)': "Tổng GTGD",
        'GTGD Bình quân phiên cổ phiếu (ngàn tỷ đồng)': "GTGD Bình quân",
        'GTGD Mua cổ phiếu của NĐTNN (ngàn tỷ đồng)': "GTGD Mua",
        'GTGD Bán cổ phiếu của NĐTNN (ngàn tỷ đồng)': "GTGD Bán"
        }
        gtgd.for_each_trace(lambda t: t.update(name= newnames[t.name],
                                           legendgroup= newnames[t.name]))
        
        if "Tổng GTGD cổ phiếu (ngàn tỷ đồng)" not in checkitem:
            gtgd.update_layout(
                yaxis2= dict(range= [0, 20], 
                        overlaying= 'y', side= 'right',
                        dtick= 20/5, fixedrange= True),
                yaxis= dict(range= [0, 300], dtick= 300/5, fixedrange= True)
            )
        else:
            gtgd.update_layout(
            yaxis2= dict(range= [0, 20], 
                        overlaying= 'y', side= 'right',
                        dtick= 20/5, fixedrange= True),
            yaxis= dict(range= [0, 2500], dtick= 2500/5, fixedrange= True)
        )


        gtgd.update_layout(margin=dict(l=60, r=30, t=20, b=100), height= 500, 
                           legend= dict(orientation = 'h', y= 1, x= 0.5, yanchor= 'top', xanchor= 'center',
                                        itemclick= False),
                           template= 'plotly_white')
        gtgd.add_annotation(dict(font=dict(color='black',size=15),
                                            x=0,
                                            y=-0.25,
                                            showarrow=False,
                                            text="ĐVT: Ngàn tỷ đồng",
                                            textangle=0,
                                            #xanchor='left',
                                            xref="paper",
                                            yref="paper"))
        
        return gtgd
    
    elif pd.to_datetime(year1) > pd.to_datetime(year2):
        raise dash.exceptions.PreventUpdate
