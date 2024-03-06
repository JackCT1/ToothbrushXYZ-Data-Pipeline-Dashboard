from dash import html, register_page, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px

from df import df

register_page(__name__, path='/Time_of_Day_Distribution')

time_of_day_bins = pd.cut(df['Order_Hour'],
    bins=[0, 4, 8, 12, 16, 20, df['Order_Hour'].max()],
    labels=(['12:00AM - 04:00AM', '04:00AM - 08:00AM', '08:00AM - 12:00PM', '12:00PM - 04:00PM', '04:00PM - 08:00PM', '08:00PM - 12:00AM'])
)

df = df.groupby(['Toothbrush_Type', time_of_day_bins])[['Order_Number']].count()
df = df.reset_index()
df = df.pivot(index='Order_Hour', columns='Toothbrush_Type', values='Order_Number')

fig = px.bar(df, x=df.index, y=['Toothbrush 2000', 'Toothbrush 4000'])

fig_2000 = px.bar(df, x=df.index, y='Toothbrush 2000')
fig_4000 = px.bar(df, x=df.index, y='Toothbrush 4000')

fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig_2000.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig_4000.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

layout = html.Div(children=[
    dcc.Graph(
        id='time-of-day-distribution',
        figure=fig
    ),
    html.Div([
        dcc.Dropdown(
            df['Toothbrush_Type'].unique(),
            "Toothbrush 2000",
            id='data-input'
        )
    ]),
    dcc.Graph(
        id='time-graph-output'
    )
])

@callback(
    Output('time-graph-output','figure'),
    Input('data-input','value')
)

def update_graph(input_value):
    if input_value == "Toothbrush 2000" :
        return fig_2000
    elif input_value == "Toothbrush 4000" :
        return fig_4000
    elif input_value == "Toothbrush 2000 and 4000":
        return fig