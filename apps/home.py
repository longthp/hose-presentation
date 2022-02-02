from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app


layout = html.Div([
            dbc.Row([
                dbc.Col([
                    html.H2("THỐNG KẾ SỐ LIỆU 21 NĂM", style= {'textAlign': 'center'}),
                    html.H3("2000 - 2021", style= {'textAlign': 'center'})
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.CardImg(src= '/assets/hose.jpg', className= 'mt-2 mb-2',
                        style= {"width": 'auto', 'height': 'auto'}
                       )
                ]),
                dbc.Col([                
                    dbc.CardImg(src= '/assets/hose_zimk2.jpg', className= 'mt-2 mb-2'),
                    dbc.Card([
                        dbc.ListGroup([
                            dbc.ListGroupItem([
                                dcc.Markdown("**Tên viết tắt: ** HOSE")
                            ]),
                            dbc.ListGroupItem(dcc.Markdown("**Người đại diện Pháp luật: **Ông Lê Hải Trà - Tổng Giám đốc")),
                            dbc.ListGroupItem(dcc.Markdown("**Địa chỉ: **16 Võ Văn Kiệt, phường Nguyễn Thanh Bình, Quận 1, Thành phố Hồ Chí Minh")),
                            dbc.ListGroupItem(dbc.CardLink(dcc.Markdown("**Trang web**"), href= "https://www.hsx.vn"))
                            ])
                    ])
                ])
            ])
])