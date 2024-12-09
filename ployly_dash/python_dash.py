
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Load Data
# Build App
app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("JupyterDash Demo"),
    dcc.Graph(id='graph'),
    html.Label([
        "colorscale",
        dcc.Dropdown(
            id='colorscale-dropdown', clearable=False,
            value='plasma', options=[
                {'label': c, 'value': c}
                for c in df_number_of_files_levels_info["pid_list"].unique()
            ])
    ]),
])

# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input("colorscale-dropdown", "value")]
)
def update_figure(colorscale):
    
    fig = go.Figure(data=[
        go.Bar(name='Mouse', x=sum_number_files_df.iloc[:, 0], y=sum_number_files_df["total_files_MOUSE"],marker=dict(color='#e69138')), #e69138
#         go.Bar(name='HR', x=sum_number_files_df.iloc[:, 0], y=sum_number_files_df["total_files_HR"],marker=dict(color='#e06666')),
#         go.Bar(name='Gryo', x=sum_number_files_df.iloc[:, 0], y=sum_number_files_df["total_files_GRY"],marker=dict(color='#2f5496')),
#         go.Bar(name='Acc', x=sum_number_files_df.iloc[:, 0], y=sum_number_files_df["total_files_ACC"],marker=dict(color='#478f96')),
#         go.Bar(name='Level_info', x=sum_number_files_df.iloc[:, 0], y=sum_number_files_df["total_files_levels_info"],marker=dict(color='#a64d79')),
    ])
    # Change the bar mode and background color.
    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(230, 230, 230, 0.8)',  # Light gray background
        paper_bgcolor='rgba(255, 255, 255, 1)'    # White paper background 
    )
    
    # Change the bar mode
    fig.update_layout(barmode='group')
    return fig


# Run app and display result inline in the notebook
app.run_server(mode='inline')