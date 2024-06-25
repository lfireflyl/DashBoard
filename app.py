import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from pages import home, clients, purchase, about

external_stylesheets = [dbc.themes.ZEPHYR]  
app = Dash(__name__, external_stylesheets=external_stylesheets,  use_pages=True)
app.config.suppress_callback_exceptions = True


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#BDBDBD", 
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("", className="display-6"),
        html.Hr(),
        html.P(
            "Проект студента БСБО-14-21 Боярова Д.М.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Главная", href="/", active="exact"),
                dbc.NavLink("Анализ клиентов", href="/clients", active="exact"),
                dbc.NavLink("Анализ продуктов и покупок", href="/purchase", active="exact"),
                dbc.NavLink("О проекте", href="/about", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/clients":
        return clients.layout
    elif pathname == "/purchase":
        return purchase.layout
    elif pathname == "/about":
        return about.layout
    
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == '__main__':
        app.run_server(debug=True)