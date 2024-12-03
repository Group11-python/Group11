# 1 #
import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objs as go

# Reading the Data
data = pd.read_csv("avocado.csv")

# Filtering the Data
data = data.query("type == 'conventional' and region == 'Albany'")
# What it does: This line filters the data to only include rows where the type column has the value 'conventional' 
# and the region column has the value 'Albany'. Essentially, it selects only the conventional avocados sold in the Albany region.

# Converting the Date Column
data = data.assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
# What it does: This line converts the Date column from a string format to a datetime format, making it easier 
# to work with dates. The pd.to_datetime function helps convert the date strings into proper datetime objects.

# Sorting the Data by Date
data = data.sort_values(by="Date")
# What it does: This line sorts the data by the Date column in ascending order. 

# In Dash, when we create a new app, we start by making an instance of the Dash class. 
# The Dash(__name__) part initializes the app and sets up everything needed for it to run.
app = Dash(__name__)


# 2 #
# --- Defining the Layout of Your Dash Application --- #
app.layout = html.Div(
    children=[
        html.H1("Avocado Analytics"),
        
        html.P("Analyze the behavior of avocado prices and the number"
                " of avocados sold in the US between 2015 and 2018"),
        
        # Graph for Average Price
        dcc.Graph(
        id='price-graph',
        figure={
            "data": [
                go.Scatter(
                    x=data["Date"],
                    y=data["AveragePrice"],
                    mode='lines',
                    name='Average Price'
                )
            ],
            "layout": go.Layout(
                title='Average Price of Avocados'
            )
        }
    ),
        
        # Graph for Total Volume
        dcc.Graph(
            id='volume-graph',
            figure={
                "data": [
                    go.Scatter(
                        x=data["Date"],
                        y=data["Total Volume"],
                        mode='lines',
                        name='Total Volume'
                    )
                ],
                "layout": go.Layout(
                    title='Avocados Sold'
                )
            }
        ),
    ]
)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)