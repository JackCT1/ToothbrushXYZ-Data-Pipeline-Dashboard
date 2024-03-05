from dash import Dash, dcc, html, Input, Output, page_container, page_registry
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.VAPOR])

app.layout = html.Div([
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in page_registry.values()
        ]
    ),
    page_container
])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)