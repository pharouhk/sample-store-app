import os
from datetime import date, datetime, timedelta
from dash import Dash, html, dcc, no_update, dash_table, no_update
from dash.dependencies import Input, Output, State
from dash.dash_table.Format import Format
from dash.dash_table import FormatTemplate
import json
import base64
import pandas as pd
import numpy as np
from collections import defaultdict
import time
import logging
from functools import reduce
from collections import OrderedDict


def generate_month_order(start_year = '2014', end_year = '2017'):
    month_order = []
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year_list = []
    year_length = (int(end_year) - int(start_year))+1
    for ind in range(0, year_length):
        yr = str(int(start_year) + ind)
        for month in month_list:
            month_order.append( month + '-' + yr)

    return month_order



def handle_aggregation(data_dict):
    """
    function that will know the columns to aggregate based on previous states
    """

    agg_data = {}
    metrics = list(data_dict.keys())
    metrics = [metric for metric in metrics if metric != 'Ship Mode'] #remove ship mode data from metrics
    
    for each_metric in metrics:
        metric_data = data_dict[each_metric]
        #test of data length
        metric_data_grp = metric_data[[each_metric, 'Order Date', 'Year']].groupby(['Order Date', 'Year']).sum().reset_index()
        if len(metric_data_grp) <= 30:
            by = 'Order Date'
        elif len(metric_data_grp) > 30 and len(metric_data_grp) <=365:
            by = 'Month'
        else:
            by = 'Year'
        agg_colums = [each_metric] + [by]
        if by != 'Year':
            if each_metric in ['Discount', 'Days to Ship']:
                grouped = metric_data[agg_colums+['Year']].groupby([by]+['Year']).mean().reset_index()
            else:
                grouped = metric_data[agg_colums+['Year']].groupby([by]+['Year']).sum().reset_index()
            
            if by == 'Month':
                month_order = generate_month_order()
                grouped['Month'] = pd.Categorical(grouped['Month'], categories=month_order, ordered=True)
                grouped = grouped.sort_values("Month", ascending=True)
        else:
            if each_metric in ['Discount', 'Days to Ship']:
                grouped = metric_data[agg_colums].groupby([by]).mean().reset_index()
            else:
                grouped = metric_data[agg_colums].groupby([by]).sum().reset_index()

        agg_data[each_metric] = grouped

    return agg_data


def get_quarter(month_col, yr_col):
    quarter = []
    for month_num, yr in zip(month_col, yr_col):
        if month_num in ['01', '02', '03']:
            quarter.append('Q1' + ' - ' + str(yr))
        elif month_num in ['04', '05', '06']:
            quarter.append('Q2' + ' - ' + str(yr))
        elif month_num in ['07', '08', '09']:
            quarter.append('Q3' + ' - ' + str(yr))
        else:
            quarter.append('Q4' + ' - ' + str(yr))
    return quarter


def generate_table(data):
    
    data_table = dash_table.DataTable(
                        data=data.to_dict('records'),
                        # sort_action='native',
                        style_cell={
                            'textAlign': 'center', 
                            'fontSize':13, 
                            'fontFamily':'Helvetica',
                            'minWidth':45,
                            'maxWidth': 45, 
                            'width': 45, 
                            'white-space':'normal'
                        },
                        style_header={
                            'color': '#000000','fontSize':15, 'font-weight': 'bold'
                        },
                        columns=[
                            {"name": i, "id": i, 'type':'numeric', 'format':Format(group=',')} if i in ['Returned', 'Quantity','Sales']
                            else {"name": i, "id": i, 'type':'numeric', 'format':FormatTemplate.percentage(2)}
                            if i in ["Discount"] else {"name": i, "id": i, 'type':'text'}
                            for i in data.columns
                        ],
                        fixed_rows={'headers': True},
                        style_table={
                            'height':'180px',
                            'overflowY': 'auto'
                        },
                        style_data_conditional=()
                    )

    return data_table