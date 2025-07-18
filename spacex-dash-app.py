# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# Create a dash application
app = dash.Dash(__name__)
# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),
    # Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    # RangeSlider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=500,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])
# Callback function for pie chart and scatter chart
@app.callback(
    [Output('success-pie-chart', 'figure'),
     Output('success-payload-scatter-chart', 'figure')],
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_charts(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                             (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    # Pie Chart
    if selected_site == 'ALL':
        pie_fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches by Site'
        )
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        pie_fig = px.pie(
            site_df,
            names='class',
            title=f'Success vs Failure for site {selected_site}'
        )
    # Scatter Plot
    scatter_fig = px.scatter(
        filtered_df if selected_site == 'ALL' else filtered_df[filtered_df['Launch Site'] == selected_site],
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Correlation between Payload and Success'
    )
    return pie_fig, scatter_fig
# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8053, debug=False)
