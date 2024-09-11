import dash
import pandas as pd
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import plotly.express as px
from dash.dash_table.Format import Format
from dash.dash_table import FormatTemplate
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from datetime import datetime
import base64
import logging
import os

base_dir = os.getcwd()
system_path = base_dir + '/'

image_path = system_path+'assets/'
menu_icon = base64.b64encode(open(image_path + 'menu_icon.png', 'rb').read())
home_icon = base64.b64encode(open(image_path + 'home_icon.png', 'rb').read())
table_icon = base64.b64encode(open(image_path + 'table_icon.png', 'rb').read())
graph_icon = base64.b64encode(open(image_path + 'graph_icon.png', 'rb').read())



sidebar = dbc.Nav(
    children=[
        dbc.NavItem(dbc.NavLink(
            style = {
                'display': 'flex',
                'flexDirection': 'row'
            },
            children = [
                html.Img(src='data:image/png;base64,{}'.format(home_icon.decode()), style={
                'width':'1.25rem', 'height':'1.25rem',
                'zIndex':'1',
                }),
                html.Span("Home", style={'padding-left': '0.5rem'})
            ],
            href="/"
            
        )),

        dbc.NavItem(dbc.NavLink(
            style = {
                'display': 'flex',
                'flexDirection': 'row'
            },
            children = [
                html.Img(src='data:image/png;base64,{}'.format(table_icon.decode()), style={
                'width':'1.25rem', 'height':'1.25rem',
                'zIndex':'1',
                }),
                html.Span("Table", style={'padding-left': '0.5rem'})
            ],
            
            href="http://127.0.0.1:3214/table-page",  active=True
            )),

        dbc.NavItem(dbc.NavLink(
            style = {
                'display': 'flex',
                'flexDirection': 'row'
            },
            children = [
                html.Img(src='data:image/png;base64,{}'.format(graph_icon.decode()), style={
                'width':'1.25rem', 'height':'1.25rem',
                'zIndex':'1',
                }),
                html.Span("Graph", style={'padding-left': '0.5rem'})
            ],

            href="http://127.0.0.1:3214/graph-page")), 
    ],
    vertical = True
)


def postalcode_filter(data):
    return [html.Span('Postal code: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'postalcode-filter',
                style={
                    'width':'7rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.85rem'
                },
                options = list(data['all_postalcodes']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_postalcodes'])[0]
                )

    ]


def region_filter(data):
    return [html.Span('Region', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'region-filter',
                style={
                    'width':'7rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.85rem'
                },
                options = list(data['all_regions']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_regions'])[0]
                )

    ]

def state_filter(data):
    return [html.Span('State', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'state-filter',
                style={
                    'width':'7rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.85rem'
                },
                options = list(data['all_states']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_states'])[0]
                )
    ]



def tableHTML(tbl_summary, all_filter_dict):
    return html.Div(
        id = 'container_custom_table',
        style ={
            'width': '95%',
            'marginLeft': 'auto',
            'marginRight': 'auto',
            'marginTop': '2.5rem',
            'display': 'grid',
            'min-width': '800px', 
            'gridTemplateRows': '50px auto auto auto',
            'gridTemplateColumns': '2fr 2fr',
            'columnGap': '1rem',
            'rowGap': '0.5rem'
                },
        #page content
        children = 
            [
                #the top row containing menu icon, brandname and filters
                html.Div(
                    id ='topRowTable',
                    style = {
                        # 'gridColumn': '1 / 2'
                        
                    },
                    children = [
                        html.Div(
                            style = {
                                'display':'flex',
                                'flexDirection': 'row',
                                # 'justifyContent': 'space-between'
                            },
                            children = [
                                html.A(
                                    children = [
                                        html.Img(src='data:image/png;base64,{}'.format(menu_icon.decode()), style={
                                        'width':'1.875rem', 'height':'1.875rem', 'position':'absolute',
                                        'zIndex':'1',
                                        }),
                                    ],
                                    id="open-offcanvas-backdrop", 
                                    n_clicks=0,
                                    href = '#',
                                    style = {
                                        'width':'10%',
                                        'height':'2.5rem',
                                        'marginTop': '0.4%'
                                    }
                                ),

                                html.H5(
                                    style = {
                                        'width': '90%',
                                        'marginTop': '0.5%'
                                    },
                                    children = [
                                        html.B('Superstore')
                                    ]
                                ),
                            ]
                        ),

                        
                    ]
                ),

                #the date range picker
                html.Div(
                    id = 'dateRangeDivTable',
                    style= {
                        
                        # 'width':'100%',
                        # 'gridColumn': '4 / 6'
                    },
                    children = [
                        html.Span(
                            style={
                                'marginTop':'4%',
                                'fontSize':'0.875rem'
                            },
                            children=[
                                'Date Filter: ',
                                dcc.DatePickerRange(
                                    id='date-range-picker',
                                    min_date_allowed=date(2014, 1, 1),
                                    max_date_allowed=date(2017, 12, 31),
                                    start_date_placeholder_text='Start Date',
                                    end_date_placeholder_text='End Date',
                                    # initial_visible_month=date(2024, datetime.now().month, 1),
                                    start_date = date(2017, 12, 30),
                                    end_date= date(2017, 12, 30),
                                    style = {
                                        'fontSize': '0.438rem',
                                        'display': 'inline-block', 
                                        }
                                ),
                            ]
                        )
                    ]
                ),

                #table div
                dbc.Card(
                    id = 'tableDiv',
                    style = {
                        'textAlign': 'center',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'rowGap': '1rem',
                        'gridColumn': '1/-1'
                    },

                    children = [
                        html.Div(
                            id = 'tableRowTop',
                            style = {
                                'display':'flex',
                                'flexDirection': 'row',
                                'justifyContent': 'space-around',
                                'alignItems': 'center',
                                'marginTop': '1rem'
                            },
                            children = [
                                html.Span(
                                style={
                                    'marginLeft':'5px', 
                                    'color':'#595959', 
                                    'fontSize':'1.0rem'
                                },
                                children=html.B('Total Sales by Postal Code')
                                ),
                                html.Div(
                                id = 'postal-code-filter-div',
                                style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'alignItems': 'center',
                                },
                                children = postalcode_filter(all_filter_dict)
                                ),

                                html.Div(
                                id = 'region-filter-div',
                                style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'alignItems': 'center',
                                },
                                children = region_filter(all_filter_dict)
                                ),

                                html.Div(
                                id = 'state-filter-div',
                                style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'alignItems': 'center',
                                },
                                children = state_filter(all_filter_dict)
                                ),

                            ]

                        ),
                        html.Div(
                            id = 'table-div',
                            style={
                                'width':'96%',
                                'height':'200px', 
                                'borderStyle':'solid',
                                'borderColor':'#F2F2F2', 
                                'marginLeft':'auto', 
                                'marginRight':'auto'
                            },
                            children=[
                                # html.Hr(style={'width':'99%','margin':'0px'}),
                            
                                #The Table

                                dcc.Loading(
                                id = 'table-loader',
                                children = [
                                    html.Div(
                                        id = 'table-data',
                                        style={
                                            'width':'100%', 
                                            'marginLeft':'auto'
                                        },
                                        children = [
                                            dash_table.DataTable(data=tbl_summary.to_dict('records'),
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
                                                for i in tbl_summary.columns
                                            ],
                                            fixed_rows={'headers': True},
                                            style_table={
                                                'height':'180px',
                                                'overflowY': 'auto'
                                            },
                                            style_data_conditional=()
                                        ),


                                        ]
                                        )
                                    ],

                                    type = 'circle'
                                )
                                
                                ]
                            ),

                            dbc.Button(
                                "Export Data",
                                className="mb-3",
                                color="primary",
                                id="export-data-button",
                                style={
                                    'maxWidth': '20%',
                                    'fontSize':'0.9rem',
                                    'alignSelf': 'flex-end',
                                    'marginRight': '1.8rem'
                                },
                            ),
                            dcc.Download(id="download-table-data-as-csv")
                    ]
                ),


                #update table div
                html.Div(
                    id = 'updateTableDiv',
                    style = {
                        'display' : 'flex',
                        'flexDirection': 'column',
                        'maxHeight': '15rem',
                        'fontSize': '1rem',
                        'flexWrap': 'wrap',
                        'width': '40%',
                        # 'marginLeft': 'auto',
                        # 'marginRight': 'auto',
                        'marginTop': '1.25rem',
                        'rowGap': '1rem',
                        'columnGap': '2rem',
                        'gridColumn': '1/-1'
                    },
                    children = [
                        html.Div(
                            id = 'postalcode-filter-div',
                            style={
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'left',
                            },
                            children = [
                                html.Span('Postal code'),
                                dcc.Input(
                                    id="input_postalcode",
                                    type="number",
                                    placeholder="Enter postal code e.g., 2345",
                                )
                                
                            ]

                        ),

                        html.Div(
                            id = 'region-input-div',
                            style={
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'left',
                            },
                            children = [
                                html.Span('Region'),
                                dcc.Input(
                                    id="input_region",
                                    type="text",
                                    placeholder="Enter region e.g., South",
                                    debounce=True
                                )

                            ]
                            ),
                        
                        html.Div(
                            id = 'state-input-div',
                            style={
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'left',
                            },
                            children = [
                                html.Span('State'),
                                dcc.Input(
                                    id="input_state",
                                    type="text",
                                    placeholder="Enter state e.g., Boston",
                                    debounce=True
                                )
                                
                            ]
                        ),

                        html.Div(
                            id = 'quantity-input-div',
                            style={
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'left',
                            },
                            children = [
                                html.Span('Quantity'),
                                dcc.Input(
                                    id="input_quantity",
                                    type="number",
                                    placeholder="Enter quantity e.g., 1000",
                                    debounce=True
                                )
                            ]
                        ),

                        html.Div(
                            id = 'sales-input-div',
                            style={
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'left',
                            },
                            children = [
                                html.Span('Sales'),
                                dcc.Input(
                                    id="input_sales",
                                    type="number",
                                    placeholder="Enter sales e.g., 10",
                                    debounce=True
                                )
                                
                            ]
                        ),

                        dbc.Button(
                            "Add data",
                            className="mb-3",
                            color="primary",
                            id="add-data-button",
                            style={
                                'maxWidth': '30%',
                                'fontSize':'0.938rem',
                                'marginTop': 'inherit'
                            },
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Alert"), close_button=True),
                                dbc.ModalBody("Please input data in all fields before clicking on Add data"),
                                dbc.ModalFooter(
                                ),
                            ],
                            id="alert-incomplete",
                            centered=True,
                            is_open=False,
                        ),

                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Alert"), close_button=True),
                                dbc.ModalBody("Cannot insert. The postal code already exists"),
                                dbc.ModalFooter(
                                ),
                            ],
                            id="alert-duplicate",
                            centered=True,
                            is_open=False,
                        ),

                    ]

                ),

                

                #footer - offcanvas script
                dbc.Offcanvas(
                    sidebar,
                    id="offcanvas",
                    title="Superstore",
                    is_open=False,
                    style = {'maxWidth':'25%'}
                ),
            ]
    )