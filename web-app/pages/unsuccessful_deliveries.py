from dash import Dash, dcc, html, Input, Output, page_container, register_page
import dash_bootstrap_components as dbc
import plotly.express as px

from df import df

register_page(__name__, path='/unsuccessful_deliveries')

figure = px.pie(
    df,
    values = 'order_quantity',
    labels= 'delivery_status',
    title= 'Proportion of Unsuccessful Deliveries')

layout = html.Div(
    children = [
        dcc.Graph(
            id = 'Failed_Deliveries',
            figure = figure
        )
    ]
)