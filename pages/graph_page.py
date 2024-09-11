import dash
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import plotly.express as px
from libraries.graph.graph_layout import *
from libraries.helpers import *
from models import *
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from datetime import datetime
import base64
import logging
import os

base_dir = os.getcwd()
system_path = base_dir + '/'

dash.register_page(__name__, path='/graph-page')


page_data, all_dict = load_n_transform()

bubble_data = pd.DataFrame(data = {
    'Sales': list(page_data['Sales']['Sales']),
    'Profit': list(page_data['Profit']['Profit']),
    'Quantity': list(page_data['Quantity']['Quantity']),
    'Ship Mode': list(page_data['Ship Mode']['Ship Mode']),
})

page_data = handle_aggregation(page_data)





layout = graphPageHTML(page_data, all_dict, bubble_data)