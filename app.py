import dash
import pandas as pd
from dash import Dash, html, dcc, no_update, dash_table, no_update
from dash.dependencies import Input, Output, State
from dash.dash_table.Format import Format
from dash.dash_table import FormatTemplate
import plotly.express as px
from dash.exceptions import PreventUpdate
from datetime import datetime
from sys import exit
from libraries.helpers import *
from models import *
from libraries.graph.chart_generator import *
from libraries.home.chart_generator import *
from libraries.graph.graph_layout import week_filter, month_filter, quarter_filter, year_filter, segment_filter, ship_mode_filter, customer_name_filter, category_filter, \
sub_category_filter, prod_name_filter, y_axis_filter, x_axis_filter
from libraries.table.table_layout import postalcode_filter, region_filter, state_filter
from collections import defaultdict
from functools import reduce
from collections import OrderedDict
import dash_bootstrap_components as dbc
from time import sleep
import warnings
warnings.filterwarnings("ignore")
import waitress
import os

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

base_dir = os.getcwd()
system_path = base_dir+'/sample-store-app'

BS = 'assets/bootstrap.min.css'
datepicker = 'assets/datepicker.css'

#initialize dash app with scripts and css
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, BS, datepicker],
    meta_tags = [{
        'name':'viewport',
        'content':'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'
    }],
    use_pages=True
)




#main app layout of the single page web app
app.layout = \
    html.Div(
        style ={
            'backgroundColor':'#F2F2F2',
            'width':'100%', 
            'height':'100vh',
            'overflowY': 'scroll',
            'position':'relative'
                },
        children = 
            [
            dash.page_container
            ]
        )


def update_table_page(updated_tbl_data, updated_filt_dict):
    postalcode_filter_updated = postalcode_filter(updated_filt_dict)
    region_filter_updated = region_filter(updated_filt_dict)
    state_filter_updated = state_filter(updated_filt_dict)

    table_updated = dash_table.DataTable(
                        data=updated_tbl_data.to_dict('records'),
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
                            for i in updated_tbl_data.columns
                        ],
                        fixed_rows={'headers': True},
                        style_table={
                            'height':'180px',
                            'overflowY': 'auto'
                        },
                        style_data_conditional=()
                    )
    return table_updated, postalcode_filter_updated, region_filter_updated, state_filter_updated, no_update, False, False


def update_page(updated_data, updated_filt_dict, _y_axis, _x_axis):
    
    bubble_data = pd.DataFrame(data = {
        _x_axis: list(updated_data[_x_axis][_x_axis]),
        _y_axis: list(updated_data[_y_axis][_y_axis]),
        'Quantity': list(updated_data['Quantity']['Quantity']),
        'Ship Mode': list(updated_data['Ship Mode']['Ship Mode']),
    })

    updated_data = handle_aggregation(updated_data)
    
    profit_fig = generate_combo_charts(data_dict= {'Profit':updated_data['Profit'], 'Profit Ratio': updated_data['Profit Ratio']},
                                    y_axis=['Profit', 'Profit Ratio'])
    discount_fig = generate_single_charts(updated_data['Discount'], y_axis='Discount')
    days_to_ship_fig = generate_single_charts(updated_data['Days to Ship'], y_axis='Days to Ship')
    quant_ret_fig = generate_combo_charts(data_dict= {'Quantity':updated_data['Quantity'], 'Returned': updated_data['Returned']},
                                    y_axis=['Quantity', 'Returned'])
    sales_fig = generate_single_charts(updated_data['Sales'], y_axis='Sales')
    bubble_fig = generate_bubble_chart(bubble_data, x_axis=_x_axis, y_axis=_y_axis, color='Ship Mode', size='Quantity')

    week_filter_updated = week_filter(updated_filt_dict)
    quarter_filter_updated = quarter_filter(updated_filt_dict)
    month_filter_updated = month_filter(updated_filt_dict)
    year_filter_updated = year_filter(updated_filt_dict)
    
    segment_filter_updated = segment_filter(updated_filt_dict)
    ship_mode_filter_updated = ship_mode_filter(updated_filt_dict)
    customer_name_filter_updated = customer_name_filter(updated_filt_dict)
    category_filter_updated = category_filter(updated_filt_dict)
    sub_category_filter_updated = sub_category_filter(updated_filt_dict)
    prod_name_filter_updated = prod_name_filter(updated_filt_dict)

    y_axis_updated = y_axis_filter(updated_filt_dict)
    x_axis_updated = x_axis_filter(updated_filt_dict)

    return week_filter_updated, month_filter_updated, quarter_filter_updated, year_filter_updated, \
    profit_fig, discount_fig, days_to_ship_fig, quant_ret_fig, sales_fig, bubble_fig, \
    segment_filter_updated, ship_mode_filter_updated, customer_name_filter_updated, category_filter_updated, sub_category_filter_updated, prod_name_filter_updated, \
    y_axis_updated, x_axis_updated


#side bar callback
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas-backdrop", "n_clicks"),
    State("offcanvas", "is_open"),
)
def toggle_offcanvas(n1, is_open):
    """
    function that toggles on or off the sidebar for page navigation
    params:
    n1: number of clicks
    is_open: boolean flag of whether True or false
    """
    if n1:
        return not is_open
    return is_open


# #interactive callbacks
@app.callback(
    Output("week-filter-div", "children"),
    Output("month-filter-div", "children"),
    Output("quarter-filter-div", "children"),
    Output("year-filter-div", "children"),
    Output("profit-fig", "figure"),
    Output("discount-fig", "figure"),
    Output("days-to-ship-fig", "figure"),
    Output("quantity-vs-returns-fig", "figure"),
    Output("sales-fig", "figure"),
    Output("bubble-fig", "figure"),
    Output("segment-filter-div", "children"),
    Output("ship-mode-filter-div", "children"),
    Output("customer-name-filter-div", "children"),
    Output("category-filter-div", "children"),
    Output("sub-category-filter-div", "children"),
    Output("prod-name-filter-div", "children"),
    Output("y-axis-filter-div", "children"),
    Output("x-axis-filter-div", "children"),
    #inputs
    Input("segment-filter", "value"),
    Input("ship-mode-filter", "value"),
    Input("customer-name-filter", "value"),
    Input("category-filter", "value"),
    Input("sub-category-filter", "value"),
    Input("product-name-filter", "value"),
    Input("y-axis-filter", "value"),
    Input("x-axis-filter", "value"),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date'),
    Input("week-filter", "value"),
    Input("month-filter", "value"),
    Input("quarter-filter", "value"),
    Input("year-filter", "value"),
    #States
    State("segment-filter", "value"),
    State("ship-mode-filter", "value"),
    State("customer-name-filter", "value"),
    State("category-filter", "value"),
    State("sub-category-filter", "value"),
    State("product-name-filter", "value"),
    State("y-axis-filter", "value"),
    State("x-axis-filter", "value"),
    State('date-range-picker', 'start_date'),
    State('date-range-picker', 'end_date'),
    State("week-filter", "value"),
    State("month-filter", "value"),
    State("quarter-filter", "value"),
    State("year-filter", "value"), prevent_initial_call=True)
def update_chart(segment, ship_mode, customer_name, category, sub_category, product_name, y_axis_input, x_axis_input, start_date, end_date, week, month, quarter, year, 
                    segment_state, ship_mode_state, customer_name_state, category_state, sub_category_state, product_name_state, 
                    y_axis_state, x_axis_state,
                    start_date_state, end_date_state, week_state, month_state, quarter_state, year_state):
    try:
        changed_inputs_list = dash.callback_context.triggered #type --> dict
        res = defaultdict(list)
        {res[key].append(sub[key]) for sub in changed_inputs_list for key in sub}
        changed_inputs_dict = dict(res) #type --> dict list
        if len(changed_inputs_dict['prop_id'])==1:
            changed_id_input = changed_inputs_dict['prop_id'][0].split('.')[0] #type --> list

            #date filter
            if changed_id_input == 'date-range-picker':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date, end_date=end_date, week=week_state, month=month_state, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)
            
            #week filter
            if changed_id_input == 'week-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week, month=month_state, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)

            #month filter
            if changed_id_input == 'month-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)

            #quarter filter
            if changed_id_input == 'quarter-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month_state, quarter=quarter, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)
                
            #year filter
            if changed_id_input == 'year-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month_state, quarter=quarter_state, year=year)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)

            #segment filter
            if changed_id_input == 'segment-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)

            #ship mode filter
            if changed_id_input == 'ship-mode-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)

            #customer name filter
            if changed_id_input == 'customer-name-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)

            #category filter
            if changed_id_input == 'category-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)

            #sub-category name filter
            if changed_id_input == 'sub-category-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)

            #product name filter
            if changed_id_input == 'product-name-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_state)
            
            #y_axis filter
            if changed_id_input == 'y-axis-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_input, x_axis_state)

            #x_axis filter
            if changed_id_input == 'x-axis-filter':
                page_data_clbk, all_dict_clbk = load_n_transform(segment=segment_state, ship_mode=ship_mode_state, customer_name=customer_name_state, category=category_state, 
                sub_category=sub_category_state, product_name=product_name_state, x_axis=x_axis_state, y_axis=y_axis_state,
                start_date=start_date_state, end_date=end_date_state, week=week_state, month=month, quarter=quarter_state, year=year_state)

                return update_page(page_data_clbk, all_dict_clbk, y_axis_state, x_axis_input)
        
    except:

        empty_bar_df = pd.DataFrame({'N/A':[0], 'Month':['N/A']})
        empty_fig = generate_single_charts(empty_bar_df['N/A'], y_axis='N/A')

        empty_bubble_df = pd.DataFrame(data = {'Sales': [0], 'Profit': [0], 'Quantity': ['N/A'], 'Ship Mode': ['N/A'],})
        empty_bubble_fig = generate_bubble_chart(empty_bubble_df, x_axis='Sales', y_axis='Profit', color='Ship Mode', size='Quantity')
        
        return no_update, no_update, no_update, no_update, \
        empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_bubble_fig, \
        no_update, no_update, no_update, no_update, no_update, no_update, \
        no_update, no_update


@app.callback(
    Output("table-data", "children"),
    Output("postal-code-filter-div", "children"),
    Output("region-filter-div", "children"),
    Output("state-filter-div", "children"),
    Output("download-table-data-as-csv", "data"),
    Output("alert-incomplete", "is_open"),
    Output("alert-duplicate", "is_open"),
    #inputs
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date'),
    Input("postalcode-filter", "value"),
    Input("region-filter", "value"),
    Input("state-filter", "value"),
    Input('export-data-button', 'n_clicks'), 
    Input('add-data-button', 'n_clicks'),
    Input('input_postalcode', 'value'),
    Input('input_region', 'value'),
    Input('input_state', 'value'),
    Input('input_quantity', 'value'),
    Input('input_sales', 'value'),
    # Input("close-incomplete", "n_clicks"),
    #States
    State('date-range-picker', 'start_date'),
    State('date-range-picker', 'end_date'),
    State("postalcode-filter", "value"),
    State("region-filter", "value"), 
    State("state-filter", "value"), prevent_initial_call=True)
def update_tbl(start_date, end_date, pcode, reg, st, n_clicks_export, n_clicks_add, 
                    pcode_input, reg_input, st_input, quantity_input, sales_input,
                    # n_clicks_close_incomplete,
                    start_date_state, end_date_state, pcode_state, reg_state, st_state):
    # try:
    changed_inputs_list = dash.callback_context.triggered #type --> dict
    res = defaultdict(list)
    {res[key].append(sub[key]) for sub in changed_inputs_list for key in sub}
    changed_inputs_dict = dict(res) #type --> dict list
    if len(changed_inputs_dict['prop_id'])==1:
        changed_id_input = changed_inputs_dict['prop_id'][0].split('.')[0] #type --> list

        #date filter
        if changed_id_input == 'date-range-picker':
            tbl_clbk, all_dict_clbk = load_n_transform_to_tbl(postalcode=pcode_state, region=reg_state, state=st_state, start_date=start_date, end_date=end_date)
            return update_table_page(tbl_clbk, all_dict_clbk)

        #postal code filter
        if changed_id_input == 'postalcode-filter':
            tbl_clbk, all_dict_clbk = load_n_transform_to_tbl(postalcode=pcode, region=reg_state, state=st_state, start_date=start_date_state, end_date=end_date_state)
            return update_table_page(tbl_clbk, all_dict_clbk)

        #region filter
        if changed_id_input == 'region-filter':
            tbl_clbk, all_dict_clbk = load_n_transform_to_tbl(postalcode=pcode_state, region=reg, state=st_state, start_date=start_date_state, end_date=end_date_state)
            return update_table_page(tbl_clbk, all_dict_clbk)

        #state filter
        if changed_id_input == 'state-filter':
            tbl_clbk, all_dict_clbk = load_n_transform_to_tbl(postalcode=pcode_state, region=reg_state, state=st, start_date=start_date_state, end_date=end_date_state)
            return update_table_page(tbl_clbk, all_dict_clbk)

        #export data button
        if changed_id_input == 'export-data-button':
            tbl_clbk, all_dict_clbk = load_n_transform_to_tbl(postalcode=pcode_state, region=reg_state, state=st_state, start_date=start_date_state, end_date=end_date_state)
            
            return no_update, no_update, no_update, no_update, dcc.send_data_frame(tbl_clbk.to_csv, "table_data.csv"), False, False

        if changed_id_input in ['input_postalcode', 'input_region', 'input_state', 'input_quantity', 'input_sales']:
            return no_update, no_update, no_update, no_update, no_update, False, False
        #add data button
        if changed_id_input == 'add-data-button':
            if all(x for x in [pcode_input, reg_input, st_input, quantity_input, sales_input]):
                tbl_clbk, all_dict_clbk = load_n_transform_to_tbl(postalcode=pcode_state, region=reg_state, state=st_state, start_date=start_date_state, end_date=end_date_state)
                
                if pcode_input not in list(tbl_clbk['Postal Code']):
                    try:
                        old_data = pd.read_csv('data/new_data.csv')
                    except:
                        old_data = pd.DataFrame()

                    new_data = pd.DataFrame(data={
                        'Postal Code': [pcode_input],
                        'Region': [reg_input],
                        'State': [st_input],
                        'City': ['N/A'],
                        'Returned': [0],
                        'Quantity': [quantity_input],
                        'Sales': [sales_input],
                        'Discount': [0]
                    })

                    if len(old_data) > 0:
                        new_data = pd.concat([new_data, old_data])

                    new_data.to_csv('data/new_data.csv', index=None)
                    time.sleep(1) #to ensure data is written before read again
                else:
                    return no_update, no_update, no_update, no_update, no_update, False, True
            else:
                return  no_update, no_update, no_update, no_update, no_update, True, False


                
            tbl_clbk, all_dict_clbk = load_n_transform_to_tbl(postalcode=pcode_state, region=reg_state, state=st_state, start_date=start_date_state, end_date=end_date_state)
            
            return generate_table(tbl_clbk), postalcode_filter(all_dict_clbk), no_update, no_update, no_update, False, False

@app.callback(
    Output("metric-profit-fig", "figure"),
    Output("metric-discount-fig", "figure"),
    Output("total-quantity", "children"),
    Output("total-sales", "children"),
    Output("total-profit", "children"),
    #inputs
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date'),
    #States
    State('date-range-picker', 'start_date'),
    State('date-range-picker', 'end_date'), prevent_initial_call=True)
def update_metrics(start_date, end_date, start_date_state, end_date_state):
    # try:
    changed_inputs_list = dash.callback_context.triggered #type --> dict
    res = defaultdict(list)
    {res[key].append(sub[key]) for sub in changed_inputs_list for key in sub}
    changed_inputs_dict = dict(res) #type --> dict list
    if len(changed_inputs_dict['prop_id'])==1:
        changed_id_input = changed_inputs_dict['prop_id'][0].split('.')[0] #type --> list

        #date filter
        if changed_id_input == 'date-range-picker':
            key_metrics_clbk_dict = load_n_transform_metrics(start_date=start_date, end_date=end_date)
            
            total_quantity_updated = format(round(key_metrics_clbk_dict['Sales']/1000, 2), ",") + "K"
            total_sales_updated = "€" + format(round(key_metrics_clbk_dict['Quantity']/1000, 2), ",") + "K"
            total_profit_updated = "€" + format(round(key_metrics_clbk_dict['Profit']/1000, 2), ",") + "K"

            avg_discount_fig_updated = donut_chart(key_metrics_clbk_dict['Discount'], 'discount')
            profit_ratio_fig_updated = donut_chart(key_metrics_clbk_dict['Profit Ratio'], 'profit_ratio')
            return profit_ratio_fig_updated, avg_discount_fig_updated, total_quantity_updated, total_sales_updated, total_profit_updated

                


if __name__ == '__main__':
	# app.run_server(debug=True, host='0.0.0.0', port=3214)
    #app.debug = True
    waitress.serve(app.server, host="0.0.0.0", port=3214)
