import dash
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import plotly.express as px
from libraries.graph.chart_generator import *
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

            href="http://127.0.0.1:3214/graph-page", active=True
            )),
    ],
    vertical = True
)

#filter variables
def week_filter(data):
    return [html.Span('Week: ', style={'marginLeft':'0.25rem'}), 
            dcc.Dropdown(
                    id = 'week-filter',
                    style={
                        'width':'6.25rem', 
                        'marginLeft':'0.125rem',
                        'marginRight':'auto',
                        'fontSize':'0.625rem'
                    },
                    options = list(data['all_weeks']),
                    #Very Important! value is type string, different from dcc.Checklist 
                    value = list(data['all_weeks'])[0]
                    )
    ]

def month_filter(data):
    return [html.Span('Month: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                        id = 'month-filter',
                        style={
                            'width':'6.25rem',
                            'marginLeft':'0.125rem',
                            'marginRight':'auto',
                            'fontSize':'0.625rem'
                        },
                        options = list(data['all_months']),
                        #Very Important! value is type string, different from dcc.Checklist 
                        value = list(data['all_months'])[0]
                        )
    ]
                

def quarter_filter(data):
    return [html.Span('Quarter: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'quarter-filter',
                style={
                    'width':'6.25rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data['all_quarters']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_quarters'])[0]
                )

    ]
                
def year_filter(data): 
    return [html.Span('Year: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'year-filter',
                style={
                    'width':'6.25rem', 
                    'marginLeft':'0.125rem', 
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data['all_years']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_years'])[0]
                )
    ]
                

def segment_filter(data):
    return [html.Span('Segment: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'segment-filter',
                style={
                    'width':'7rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data['all_segments']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_segments'])[0]
                )

    ]
                    

def ship_mode_filter(data):
    return [html.Span('Ship Mode: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'ship-mode-filter',
                style={
                    'width':'7rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data['all_ship_modes']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_ship_modes'])[0]
                )

    ]
    
                

def customer_name_filter(data):
    return [html.Span('Customer Name: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'customer-name-filter',
                style={
                    'width':'7rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data['all_customers']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_customers'])[0]
                )
    ]
                    

def category_filter(data): 
    return [html.Span('Category: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'category-filter',
                style={
                    'width':'7rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data['all_categories']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_categories'])[0]
                )
    ]
    

def sub_category_filter(data):
    return [html.Span('Sub-Category: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'sub-category-filter',
                style={
                    'width':'7rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data['all_sub_categories']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_sub_categories'])[0]
                )
    ]
            
                    


def prod_name_filter(data):
    return [html.Span('Product Name: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'product-name-filter',
                style={
                    'width':'10rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data['all_products']),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data['all_products'])[0]
                )
    ]
                    

def y_axis_filter(data):
    return [html.Span('Y-axis: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'y-axis-filter',
                style={
                    'width':'5.25rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data["all_y_axis"]),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data["all_y_axis"])[0]
                )
    ]
    
            

def x_axis_filter(data):
    return [html.Span('X-axis: ', style={'marginLeft':'0.25rem'}),
            dcc.Dropdown(
                id = 'x-axis-filter',
                style={
                    'width':'5.25rem', 
                    'marginLeft':'0.125rem',
                    'marginRight':'auto',
                    'fontSize':'0.625rem'
                },
                options = list(data["all_x_axis"]),
                #Very Important! value is type string, different from dcc.Checklist 
                value = list(data["all_x_axis"])[0]
            )
    ] 
            




#page layout putting it all together
def graphPageHTML(data, all_filter_dict, bubble_data):
    return html.Div(
        id = 'container_custom_graph',
        style ={
            'width': '95%',
            'marginTop': '2.5rem',
            'marginLeft': 'auto',
            'marginRight': 'auto',
            'display': 'grid',
            'gridTemplateRows': '50px auto',
            'gridTemplateColumns': '0.9fr 0.9fr 2.2fr',
            'columnGap': '1rem',
            'rowGap': '0.5rem'
                },
        #page content
        children = 
            [
                
                html.Div(
                    id ='topRow',
                    style = {
                        'width': '100%',
                    },
                    children = [
                        html.Div(
                            style = {
                                'display':'flex',
                                'flexDirection': 'row',
                                'width': '100%'
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
                                        # 'height':'2.5rem',
                                        'marginTop': '0.4%'
                                    }
                                ),

                                html.H5(
                                    style = {
                                        'width': '90%',
                                        'marginTop': '0.5%',
                                        'textAlign': 'center'
                                    },
                                    children = [
                                        html.B('Superstore')
                                    ]
                                ),
                            ]
                        ),

                        
                    ]
                ),

                #date range div
                html.Div(
                id = 'dateRangeDivGraph',
                style= {
                    'width':'100%',
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

                #global period filters
                html.Div(
                    id = 'periodFilters',
                    style = {
                        'display' : 'flex',
                        'flexDirection': 'column',
                        'justifyContent': 'space-between',
                        'fontSize': '0.875rem',
                        'flexWrap': 'wrap'
                    },

                    children = [
                            #week filter
                            html.Div(
                                id='week-filter-div',
                                style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'alignItems': 'center',
                            },

                            children = 
                                week_filter(all_filter_dict)
                            ),

                            #month filter
                            html.Div(
                                id='month-filter-div',
                                style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'alignItems': 'center',
                            },

                            children =  month_filter(all_filter_dict)
                            ),

                            #quarter filter
                            html.Div(
                                id='quarter-filter-div',
                                style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'alignItems': 'center',
                            },

                            children = quarter_filter(all_filter_dict)
                            ),

                            #year filter
                            html.Div(
                                id='year-filter-div',
                                style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'alignItems': 'center',
                            },

                            children = year_filter(all_filter_dict)
                            )
                            
                        ]
                ),

                #left card group with bar charts
                html.Div(
                    id = 'barChartDivs',
                    style = {
                        'display': 'flex',
                        'flexDirection': 'column',
                        'colGap': '0.3rem',
                        'gridColumn': '1/3'
                    },

                    children = [
                        dbc.Card(
                            style = {
                            },
                            children = [
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                        id = 'profit-fig-loader',
                                        children = [
                                            dcc.Graph(
                                                id='profit-fig', 
                                                responsive=True,
                                                style = {
                                                    'height': '18vh'
                                                },
                                                figure=generate_combo_charts(data_dict= {'Profit':data['Profit'], 'Profit Ratio': data['Profit Ratio']},
                                                y_axis=['Profit', 'Profit Ratio']), 
                                                config={'displayModeBar': False}
                                            )
                                        ],
                                        type = 'circle'
                                    )
                                        
                                ]
                                )

                            ]
                        ),

                        dbc.Card(
                            style = {
                            },
                            children = [
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                        id = 'discount-fig-loader',
                                        children = [
                                            dcc.Graph(
                                                id='discount-fig', 
                                                responsive=True,
                                                style = {
                                                    'height': '18vh'
                                                },
                                                figure=generate_single_charts(data['Discount'], y_axis='Discount'), 
                                                config={'displayModeBar': False}
                                            )
                                        ],

                                        type = 'circle'
                                    )
                                ]
                                )

                            ]
                        ),

                        dbc.Card(
                            style = {
                            },
                            children = [
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                        id = 'daystoship-fig-loader',
                                        children = [
                                            dcc.Graph(
                                                id='days-to-ship-fig', 
                                                responsive=True,
                                                style = {
                                                    'height': '18vh'
                                                },
                                                figure=generate_single_charts(data['Days to Ship'], y_axis='Days to Ship'), 
                                                config={'displayModeBar': False}
                                            )
                                        ],
                                        type = 'circle'
                                    )                                        
                                ]
                                )

                            ]
                        ),

                        dbc.Card(
                            style = {
                            },
                            children = [
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                        id = 'quantvsret-fig-loader',
                                        children = [
                                            dcc.Graph(
                                                id='quantity-vs-returns-fig', 
                                                responsive=True,
                                                style = {
                                                    'height': '18vh'
                                                },
                                                figure=generate_combo_charts(data_dict= {'Quantity':data['Quantity'], 'Returned': data['Returned']},
                                                y_axis=['Quantity', 'Returned']), 
                                                config={'displayModeBar': False}
                                            )
                                        ],
                                        type = 'circle'
                                    )
                                ]
                                )

                            ]
                        ),

                        dbc.Card(
                            style = {
                                
                            },
                            children = [
                                dbc.CardBody(
                                    [
                                        dcc.Loading(
                                        id = 'sales-fig-loader',
                                        children = [
                                            dcc.Graph(
                                                id='sales-fig', 
                                                responsive=True,
                                                style = {
                                                    'height': '18vh'
                                                },
                                                figure=generate_single_charts(data['Sales'], y_axis='Sales'), 
                                                config={'displayModeBar': False}
                                            )
                                        ],
                                        type = 'circle'
                                    )
                                        
                                ]
                                )

                            ]
                        ),
                        
                    ]
                ),

                dbc.Card(
                    id = 'rightBubbleCard',
                    style = {
                        'display': 'flex',
                        'flexDirection': 'column',
                        'rowGap': '1.5rem',
                        'gridColumn': '3/4'
                    },

                    children = [
                        #top filters
                        html.Div(
                            id = 'bubbleFilters',
                            style = {
                                'display' : 'flex',
                                'flexDirection': 'column',
                                'maxHeight': '9rem',
                                # 'justifyContent': 'space-between',
                                'fontSize': '0.675rem',
                                'flexWrap': 'wrap',
                                'width': '80%',
                                'marginLeft': 'auto',
                                'marginRight': 'auto',
                                'marginTop': '1.25rem',
                                'rowGap': '1rem'
                            },
                            children = [
                                html.Div(
                                    id = 'segment-filter-div',
                                    style={
                                    'display': 'flex',
                                    'flexDirection': 'row',
                                    'alignItems': 'center',
                                    },
                                    children = segment_filter(all_filter_dict)

                                ),

                                html.Div(
                                    id = 'ship-mode-filter-div',
                                    style={
                                    'display': 'flex',
                                    'flexDirection': 'row',
                                    'alignItems': 'center',
                                    },
                                    children = ship_mode_filter(all_filter_dict)
                                    ),
                                
                                html.Div(
                                    id = 'customer-name-filter-div',
                                    style={
                                    'display': 'flex',
                                    'flexDirection': 'row',
                                    'alignItems': 'center',
                                    },
                                    children = customer_name_filter(all_filter_dict)
                                ),

                                html.Div(
                                    id = 'category-filter-div',
                                    style={
                                    'display': 'flex',
                                    'flexDirection': 'row',
                                    'alignItems': 'center',
                                    },
                                    children = category_filter(all_filter_dict)
                                ),

                                html.Div(
                                    id = 'sub-category-filter-div',
                                    style={
                                    'display': 'flex',
                                    'flexDirection': 'row',
                                    'alignItems': 'center',
                                    },
                                    children = sub_category_filter(all_filter_dict)
                                ),

                                html.Div(
                                    id = 'prod-name-filter-div',
                                    style={
                                    'display': 'flex',
                                    'flexDirection': 'row',
                                    'alignItems': 'center',
                                    },
                                    children = prod_name_filter(all_filter_dict)
                                )

                            ]

                        ),

                        
                        #bubble chart
                        html.Div(
                            id = 'bubbleChartDiv',
                            style = {
                                'display': 'flex',
                                'flexDirection': 'column',
                                'rowGap': '1rem',
                                'width': '90%',
                                'marginLeft': 'auto',
                                'marginRight': 'auto',
                            },
                            children = [

                                html.Div(
                                    id = 'y-axis-filter-div',
                                    style={
                                    'display': 'flex',
                                    'flexDirection': 'row',
                                    'alignItems': 'center',
                                    },
                                    children = y_axis_filter(all_filter_dict)
                                ),
                                
                                dcc.Loading(
                                id = 'bubble-fig-loader',
                                children = [

                                    dcc.Graph(
                                    id='bubble-fig', 
                                    responsive=True,
                                    style = {
                                        'height': '40vh'
                                    },
                                    figure=generate_bubble_chart(bubble_data, x_axis='Sales', y_axis='Profit', color='Ship Mode', size='Quantity'), 
                                    config={'displayModeBar': False}
                                    ),
                                ],

                                type = 'circle'
                                ),

                                html.Div(
                                    id = 'x-axis-filter-div',
                                    style={
                                    'display': 'flex',
                                    'flexDirection': 'row',
                                    'alignItems': 'center',
                                    'alignSelf': 'flex-end'
                                    },
                                    children = x_axis_filter(all_filter_dict)
                                )
                                
                                

                            ]
                            
                            

                        ),

                        #paragraph
                        html.Span('Bubble Size = Quantity', style={'textAlign': 'left', 'width': '90%', 'marginLeft': 'auto', 'marginRight': 'auto'})
                        
                        
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
