#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load your dataset - replace with your actual CSV path
data = pd.read_csv('automobile_sales.csv')

# Prepare year list for dropdown (1980 to 2023)
year_list = [i for i in range(1980, 2024)]

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    # Title (Task 2.1)
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': '24px'}
    ),

    # Dropdown for Report Type (Task 2.2)
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        placeholder='Select a report type',
        value=None,
        style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
    ),

    # Dropdown for Year selection (Task 2.2)
    dcc.Dropdown(
        id='select-year',
        options=[{'label': str(year), 'value': year} for year in year_list],
        placeholder='Select year',
        value=None,
        style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'},
        disabled=True
    ),

    # Output container (Task 2.3)
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap'})
])

# Callback to enable/disable year dropdown (Task 2.4)
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_year_dropdown(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False  # enable year dropdown
    else:
        return True  # disable year dropdown

# Callback to update graphs in output container (Task 2.4, 2.5, 2.6)
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        R_chart1 = dcc.Graph(
            figure=px.line(recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index(),
                           x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales Over Recession Years")
        )

        R_chart2 = dcc.Graph(
            figure=px.bar(recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index(),
                          x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Vehicle Sales by Type (Recession)")
        )

        R_chart3 = dcc.Graph(
            figure=px.pie(recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index(),
                          values='Advertising_Expenditure', names='Vehicle_Type',
                          title="Ad Expenditure Share by Vehicle Type (Recession)")
        )

        R_chart4 = dcc.Graph(
            figure=px.bar(recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales']
                          .mean().reset_index(),
                          x='Unemployment_Rate', y='Automobile_Sales', color='Vehicle_Type',
                          title="Effect of Unemployment Rate on Vehicle Sales (Recession)")
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year is not None:
        yearly_data = data[data['Year'] == input_year]

        Y_chart1 = dcc.Graph(
            figure=px.line(data.groupby('Year')['Automobile_Sales'].mean().reset_index(),
                           x='Year', y='Automobile_Sales',
                           title='Yearly Average Automobile Sales')
        )

        Y_chart2 = dcc.Graph(
            figure=px.line(yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index(),
                           x='Month', y='Automobile_Sales',
                           title=f'Total Monthly Automobile Sales in {input_year}')
        )

        Y_chart3 = dcc.Graph(
            figure=px.bar(yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index(),
                          x='Vehicle_Type', y='Automobile_Sales',
                          title=f'Average Vehicles Sold by Vehicle Type in {input_year}')
        )

        Y_chart4 = dcc.Graph(
            figure=px.pie(yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index(),
                          values='Advertising_Expenditure', names='Vehicle_Type',
                          title=f'Total Advertising Expenditure by Vehicle Type in {input_year}')
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]

    else:
        return None

# ✅ THIS LINE MUST BE AT THE BOTTOM
if __name__ == '__main__':
    app.run(debug=True)
