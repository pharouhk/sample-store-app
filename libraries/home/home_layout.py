import dash
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
from libraries.home.chart_generator import *
import plotly.express as px
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
sales_quantity_icon = base64.b64encode(open(image_path + 'sales_quantity_icon.png', 'rb').read())
sales_icon = base64.b64encode(open(image_path + 'sales_icon.png', 'rb').read())
profit_icon = base64.b64encode(open(image_path + 'profit_icon.png', 'rb').read())
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
            href="/", active=True
            
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
            
            href="http://127.0.0.1:3214/table-page")),

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

def homeHTML(data_dict):
    return html.Div(
        id = 'container_custom',
        style ={
            'width': '95%',
            'marginLeft': 'auto',
            'marginRight': 'auto',
            'display': 'grid',
            'gridTemplateRows': '40px 50px 80px auto auto',
            'gridTemplateColumns': '0.75fr 0.75fr 0.75fr 0.75fr 1.0fr',
            'columnGap': '1rem',
            'rowGap': '0.5rem'
                },
        #page content
        children = 
            [
                #empty div for separation between the first page content and browser
                html.Div(
                    id="emptyDiv",
                    style = {
                        'width': '100%',
                        'gridColumn': '1 / -1'
                    }
                ),

                #the top row containing menu icon, brandname and filters
                html.Div(
                    id ='topRow',
                    style = {
                        'gridColumn': '1 / 5', 
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
                    id = 'dateRangeDiv',
                    style= {
                        
                        'width':'100%',
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

                #empty div row
                html.Div(
                    id="emptyDiv2",
                    style = {
                        'width': '100%',
                        'gridColumn': '1 / -1'
                    }
                ),

                dcc.Loading(
                id = 'sales-card-loader',
                children = [

                    #left card group with charts and metrics
                    html.Div(
                        id = 'quantityCard',
                        style = {
                            'textAlign': 'center'
                        },

                        children = [
                            dbc.Card(
                                style = {
                                },
                                children = [
                                    dbc.CardBody(
                                        [
                                            html.Img(
                                                src='data:image/png;base64,{}'.format(sales_quantity_icon.decode()),
                                                className="card-title",
                                                style={
                                                'width':'1.875rem', 'height':'1.875rem',
                                                'zIndex':'1',
                                                }
                                            ),
                                            html.P(
                                                html.B(
                                                    id = 'total-quantity',
                                                    children = [format(round(data_dict['Sales']/1000, 2), ",") + "K"]
                                                ), 
                                            style={'fontSize': '1.75rem', 'color': '#5DC6F1'}),
                                            html.Span("Total Sales Quantity"),
                                    ]
                                    )

                                ]
                                
                            ),
                            
                        ]
                    ),
                ],

                type = 'circle'

                ),


                dcc.Loading(
                id = 'sales-card-loader',
                children = [

                    html.Div(
                        id = 'salesCard',
                        style = {
                        },

                        children = [
                            dbc.Card(
                                style = {
                                    'textAlign': 'center'
                                },
                                children = [
                                    dbc.CardBody(
                                        [
                                            html.Img(
                                                src='data:image/png;base64,{}'.format(sales_icon.decode()),
                                                className="card-title",
                                                style={
                                                'width':'1.875rem', 'height':'1.875rem',
                                                'zIndex':'1',
                                                }
                                            ),
                                            html.P(
                                                html.B(
                                                    id='total-sales',
                                                    children = ["€" + format(round(data_dict['Quantity']/1000, 2), ",") + "K"]
                                                ), 
                                            style={'fontSize': '1.75rem', 'color': '#5DC6F1'}),
                                            dcc.Link(html.Span("Total Sales"), href = 'http://127.0.0.1:3214/table-page')
                                        ]
                                    )

                                ]
                                
                            ),
                            
                        ]
                    ),
                ],

                type = 'circle'
                ),

                dcc.Loading(
                id = 'profit-card-loader',
                children = [

                    html.Div(
                        id = 'profitCard',
                        style = {
                            'textAlign': 'center'
                        },

                        children = [
                            dbc.Card(
                                style = {
                                },
                                children = [
                                    dbc.CardBody(
                                        [
                                        html.Img(
                                            src='data:image/png;base64,{}'.format(profit_icon.decode()),
                                            className="card-title",
                                            style={
                                            'width':'1.875rem', 'height':'1.875rem',
                                            'zIndex':'1',
                                            }
                                        ),
                                        html.P(
                                            html.B(
                                                id='total-profit',
                                                children = ["€" + format(round(data_dict['Profit']/1000, 2), ",") + "K"]
                                                ), 
                                            style={'fontSize': '1.75rem', 'color': '#5DC6F1'}),
                                        html.Span("Total Profit"),
                                    ]
                                    )

                                ]
                                
                            ),
                            
                        ]
                    ),
                ],
                type = 'circle'

                ),


                dcc.Loading(
                id = 'rate-card-loader',
                children = [
                    html.Div(
                        id = 'discountRateCard',
                        style = {
                            'textAlign': 'center'
                        },

                        children = [
                            dbc.Card(
                                style = {
                                },
                                children = [
                                    dbc.CardBody(
                                        [
                                        dcc.Graph(
                                            id='metric-discount-fig',
                                            responsive=True,
                                            figure=donut_chart(data_dict['Discount'], 'discount'),
                                            style = {
                                                    'height': '14vh'
                                            },
                                            config={'displayModeBar': False}
                                        ),
                                        html.Span("Average Discount Rate"),
                                    ]
                                    )

                                ]
                                
                            ),
                            
                        ]
                    ),
                ],
                type = 'circle'
                ),

                #right card row with a gauge chart
                dcc.Loading(
                id = 'right-card-loader',
                children = [
                    html.Div(
                    id = 'rightCard',
                    style = {
                        'textAlign': 'center'
                    },

                    children = [
                        dbc.Card(
                            style = {
                            },
                            children = [
                                dbc.CardBody(
                                    [
                                    dcc.Graph(
                                        id='metric-profit-fig',
                                        responsive=True,
                                        figure=donut_chart(data_dict['Profit Ratio'], 'profit_ratio'),
                                        style = {
                                                'height': '14vh'
                                        },
                                        config={'displayModeBar': False}
                                    ),
                                    dcc.Link(html.Span("Profit Ratio"), href='http://127.0.0.1:3214/graph-page')
                                ]
                                )

                            ]
                            
                        ),
                        
                    ]
                ),

                ],

                type = 'circle'
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