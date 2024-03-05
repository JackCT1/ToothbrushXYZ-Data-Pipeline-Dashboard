from dash import html, register_page

register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='Toothbrush XYZ Data Analytics'),
    html.P(children='Welcome to the Toothbrush XYZ Data Analytics Dashboard.')
]) 