import dash
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import plotly.express as px
from libraries.table.table_layout import *
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

dash.register_page(__name__, path='/table-page')

page_data, all_dict = load_n_transform_to_tbl()



layout = tableHTML(page_data, all_dict)