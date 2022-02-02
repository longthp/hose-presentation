import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import gtvh, tstk, gtgd, smck, home

SIDEBAR_STYLE = {
    "position": 'fixed',
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": '16rem',
    "padding": '2rem 1rem',
    "background-color": '#f8f9fa'
}

CONTENT_STYLE = {
    "display": 'block',
    "margin-left": '18rem',
    "margin-right": '2rem',
    "padding": '2rem 1rem'
}

datalink = "https://docs.google.com/spreadsheets/d/1IAdgprQDqr72g9L4TGQwr28Z7MhWrn5q/edit?usp=sharing&ouid=114293294712205665019&rtpof=true&sd=true"

sidebar = dbc.Card([
    dbc.CardBody([
        html.H2("HOSE", className= 'display-4'),
        html.Hr(),
        html.P("Sở Giao dịch Chứng khoán Thành phố Hồ Chí Minh"),
        dbc.Nav([
            dbc.NavLink('Home', href= '/apps/home', active= 'exact'),
            dbc.NavLink('Page 1', href= '/apps/gtvh', active= 'exact'),
            dbc.NavLink('Page 2', href= '/apps/tstk', active= 'exact'),
            dbc.NavLink('Page 3', href= '/apps/gtgd', active= 'exact'),
            dbc.NavLink('Page 4', href= '/apps/smck', active= 'exact')
        ], vertical= True, pills= True)
    ]),
    dbc.CardFooter([
        dbc.CardLink("Link Số Liệu", href= datalink)
    ])
], style= SIDEBAR_STYLE)

content = html.Div(id= 'page-content', children= [], style= CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id= 'url'),
    sidebar,
    content
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def update_page_content(pathname):
    if pathname == "/apps/home":
        return home.layout
    if pathname == "/apps/gtvh":
        return gtvh.layout
    if pathname == "/apps/tstk":
        return tstk.layout
    if pathname == "/apps/gtgd":
        return gtgd.layout
    elif pathname == "/apps/smck":
        return smck.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=False)

