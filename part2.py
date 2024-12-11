#!/usr/bin/env python
# coding: utf-8

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1: Create a Dash application and give it a meaningful title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',  # Align the title to the center
            'color': '#503D36',     # Set the color to #503D36
            'font-size': '24px'     # Set the font size to 24px
        }
    ),

    # TASK 2.2: Add two dropdown menus
    # Set up the app layout with two dropdown menus
    html.Div([  # First Dropdown Menu: Select Report Type (Statistics)
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',  # Set ID for the first dropdown
            options=[  # Options for statistics selection
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',  # Default selected value
            placeholder='Select Report Type',  # Placeholder text
            style={'width': '50%', 'padding': '10px'}  # Style for dropdown (optional)
        )
    ], style={'padding': '20px'}),

    html.Div([  # Second Dropdown Menu: Select Year
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',  # Set ID for the second dropdown
            options=[{'label': str(i), 'value': i} for i in range(1980, 2024, 1)],  # List of years as options
            value=2020,  # Default year value
            style={'width': '50%', 'padding': '10px'}  # Style for dropdown (optional)
        )
    ], style={'padding': '20px'}),

    # Add a division for output display
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ])
])

# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False  # Enable year dropdown
    else: 
        return True  # Disable year dropdown for Recession Period Statistics


# Callback for plotting
# Define the callback function to update the output container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                           x='Year', 
                           y='Automobile_Sales', 
                           title="Average Automobile Sales Fluctuation Over Recession Period")
        )

        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                          x='Vehicle_Type',
                          y='Automobile_Sales',
                          title="Average Number of Vehicles Sold by Vehicle Type")
        )
        
        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, 
                          names='Vehicle_Type', 
                          values='Advertising_Expenditure',
                          title="Total Advertising Expenditure Share by Vehicle Type During Recessions")
        )

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby('Unemployment_Rate')['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                          x='Unemployment_Rate',
                          y='Automobile_Sales',
                          labels={'Unemployment_Rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Automobile sales using line chart for the selected year.
        yas = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, 
                           x='Year', 
                           y='Automobile_Sales', 
                           title='Yearly Automobile Sales')
        )

        # Plot 2: Total Monthly Automobile sales using line chart.
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                           x='Month',
                           y='Automobile_Sales',
                           title='Total Monthly Automobile Sales')
        )

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, 
                          x='Vehicle_Type', 
                          y='Automobile_Sales', 
                          title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year))
        )

        # Plot 4: Pie chart for total advertisement expenditure for each vehicle type
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, 
                          names='Vehicle_Type', 
                          values='Advertising_Expenditure',
                          title='Total Advertisement Expenditure by Vehicle Type')
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
