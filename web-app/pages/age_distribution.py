from dash import html, register_page, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

from df import df

register_page(__name__, path='/Age_Distribution')

df1 = df[(df['toothbrush_type'] == 'Toothbrush 2000')]
df2 = df[(df['toothbrush_type'] == 'Toothbrush 4000')]

fig_2000 = px.bar(
    df1,
    x="customer_age",
    y="order_quantity",
    barmode="group",
    title ="Plot of Customer Age vs Order Quantity for the Toothbrush 2000")
fig_4000 = px.bar(
    df2,
    x="customer_age",
    y="order_quantity",
    barmode="group",
    title ="Plot of Customer Age vs Order Quantity for the Toothbrush 4000")

fig_2000.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig_4000.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

layout = html.Div(children=[
    html.Div([
        dcc.Dropdown(
            df1['Toothbrush_Type'].unique(),
            "Toothbrush 2000",
            id='data-input'
        )
    ]),
    dcc.Graph(
        id='age-graph-output'
    )
])

@callback(
    Output('age-graph-output','figure'),
    Input('data-input','value')
)

def update_graph(input_value):
    if input_value == "Toothbrush 2000" :
        return fig_2000
    elif input_value == "Toothbrush 4000" :
        return fig_4000