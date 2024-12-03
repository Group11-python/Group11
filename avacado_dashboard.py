import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# Reading the Data
data = pd.read_csv("avocado.csv")

# Converting the Date Column
data = data.assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))

# Sorting the Data by Date
data = data.sort_values(by="Date")

app = Dash(__name__)
app.title = "Avocado Analytics: Understand Your Avocados!"

# Define the layout of the app
app.layout = html.Div(
    children=[
        html.Img(src='./assets/avacado.jpg', className="header-image"),
        #html.P(children="🥑", className="header-emoji"),
        html.H1("Avocado Analytics", className="header-title"),
        
        html.P(
            "Analyze the behavior of avocado prices and the number of avocados sold in the US between 2015 and 2018",
            className="header-description"
        ),

        # Dropdown for selecting region              ### 1 ###
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in data['region'].unique()],
            value='Albany',
            className="dropdown"
        ),
        
        # Dropdown for selecting type                  
        dcc.Dropdown(
            id='type-dropdown',
            options=[{'label': avocado_type, 'value': avocado_type} for avocado_type in data['type'].unique()],
            value='conventional',
            className="dropdown"
        ),

        # Graph for Average Price
        dcc.Graph(
            id='price-graph'
        ),

        # Graph for Total Volume
        dcc.Graph(
            id='volume-graph'
        ),
    ],
    className="container"
)

# Define callback to update graphs based on dropdown selections    ### 2 ###
@app.callback(
    [Output('price-graph', 'figure'),
     Output('volume-graph', 'figure')],
    [Input('region-dropdown', 'value'),
     Input('type-dropdown', 'value')]
)
def update_graphs(selected_region, selected_type):    ### 3 ###
    filtered_data = data.query("region == @selected_region and type == @selected_type")     
    
    price_figure = {
        "data": [
            go.Scatter(
                x=filtered_data["Date"],
                y=filtered_data["AveragePrice"],
                mode='lines',
                line=dict(color='green'),
                hovertemplate= "$%{y:.2f}<extra></extra>",
                name='Average Price'
            )
        ],
        "layout": go.Layout(
            title='Average Price of Avocados'
        )
    }
    
    volume_figure = {
        "data": [
            go.Scatter(
                x=filtered_data["Date"],
                y=filtered_data["Total Volume"],
                mode='lines',
                line=dict(color='green'),
                name='Total Volume'
            )
        ],
        "layout": go.Layout(
            title='Avocados Sold'
        )
    }
    
    return price_figure, volume_figure


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
