import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import warnings
from libraries.helpers import *
warnings.filterwarnings("ignore")




def preprocess_data(orders, start_date, end_date):
    orders['Order Date'] = [datetime.strptime(order_date, '%m/%d/%Y').date() for order_date in list(orders['Order Date'])]
    orders['Ship Date'] = [datetime.strptime(ship_date, '%m/%d/%Y').date() for ship_date in list(orders['Ship Date'])]

    orders = orders.sort_values(['Order Date'], ascending=True)

    max_date = max(orders['Order Date'])
    
    if (start_date == '') and (end_date == ''):
        start_date = max_date
        end_date = max_date
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    range_list = pd.date_range(start_date, end_date, freq='d')
    range_list = [datetime.date(each_date) for each_date in range_list]
    orders = orders[orders['Order Date'].isin(range_list)]
    orders['Month'] = [day.strftime('%b') + '-' + day.strftime('%Y') for day in orders['Order Date']]
    orders['Week'] = ['Wk-'+ str(day.isocalendar().week) + '-' + day.strftime('%Y') for day in orders['Order Date']]
    month_num = [day.strftime('%m') for day in orders['Order Date']]
    y = [day.strftime('%Y') for day in orders['Order Date']]
    orders['Quarter'] = get_quarter(month_num, y)
    orders['Year'] = y

    return orders


def filter_orders_tbl(orders, postalcode='All', region='All', state='All'):
    if postalcode!='All':
        orders = orders[orders['Postal Code']==postalcode]
    if region!='All':
        orders = orders[orders['Region']==region]
    if state!='All':
        orders = orders[orders['State']==state]

    return orders


def filter_orders(orders, segment, ship_mode, customer_name, category, sub_category, product_name, week, month, quarter, year):
    if week != 'All':
        orders = orders[orders['Week']==week]
    if month != 'All':
        orders = orders[orders['Month']==month]
    if quarter != 'All':
        orders = orders[orders['Quarter']==quarter]
    if year != 'All':
        orders = orders[orders['Year']==year]
    if segment != 'All':
        orders = orders[orders['Segment']==segment]
    if ship_mode != 'All':
        orders = orders[orders['Ship Mode']==ship_mode]
    if customer_name != 'All':
        orders = orders[orders['Customer Name']==customer_name]
    if category != 'All':
        orders = orders[orders['Category']==category]
    if sub_category != 'All':
        orders = orders[orders['Sub-Category']==sub_category]
    if product_name != 'All':
        orders = orders[orders['Product Name']==product_name]

    return orders


def load_n_transform(segment='All', ship_mode='All', customer_name='All', category='All', sub_category='All', product_name='All', x_axis='Sales', y_axis='Profit',
start_date='', end_date='', week='All', month='All', quarter='All', year='All'):
    """
    function that takes all dashboard parameters and filters the data correctly
    params:
    start_date
    end_date
    week
    month
    quarter
    year
    segment
    ship_mode
    customer_name
    category
    sub_category
    product_name
    y_axis
    x_axis

    """
    requests = [segment, ship_mode, customer_name, category, sub_category, product_name, x_axis, y_axis]

    orders = pd.read_csv("data/orders.csv")
    returns = pd.read_csv("data/returns.csv")
    orders = pd.merge(orders, returns, left_on='Order ID', right_on='Order ID', how='left')
    
    orders = preprocess_data(orders, start_date, end_date)
    
    orders = filter_orders(orders, segment, ship_mode, customer_name, category, sub_category, product_name, week, month, quarter, year)

    segment_filtered = list(set(orders['Segment']))
    segment_filtered.sort()

    ship_mode_filtered = list(set(orders['Ship Mode']))
    ship_mode_filtered.sort()

    cust_name_filtered = list(set(orders['Customer Name']))
    cust_name_filtered.sort()

    category_filtered = list(set(orders['Category']))
    category_filtered.sort()

    sub_category_filtered = list(set(orders['Sub-Category']))
    sub_category_filtered.sort()

    prod_name_filtered = list(set(orders['Product Name']))
    prod_name_filtered.sort()

    orders['Days to Ship'] = [(ship_date - order_date).days for ship_date, order_date in zip(orders['Ship Date'], orders['Order Date']) ]

    orders['Profit Ratio'] = [profit/sales for profit, sales in zip(orders['Profit'], orders['Sales']) ]

    # orders_returned = orders[orders['Returned']=='Yes']
    orders['Returned'] = [1 if ret == 'Yes' else 0 for ret in orders['Returned']]
    
    metrics = ['Profit', 'Profit Ratio', 'Quantity', 'Sales', 'Returned', 'Discount', 'Days to Ship']

    all_data = {
        'Profit': orders[['Order Date', 'Month', 'Year', 'Profit']],
        'Profit Ratio': orders[['Order Date', 'Month', 'Year', 'Profit Ratio']],
        'Quantity': orders[['Order Date', 'Month', 'Year', 'Quantity']],
        'Sales': orders[['Order Date', 'Month', 'Year', 'Sales']],
        'Returned': orders[['Order Date', 'Month', 'Year', 'Returned']],
        'Discount': orders[['Order Date', 'Month', 'Year', 'Discount']],
        'Days to Ship': orders[['Order Date', 'Month', 'Year', 'Days to Ship']],
        'Ship Mode': orders[['Order Date', 'Month', 'Year', 'Ship Mode']]
    }

    all_dict = {
        'all_weeks': ['All'] + list(set(orders['Week'])),
        'all_months':  ['All'] + list(set(orders['Month'])),
        'all_quarters':['All'] + list(set(orders['Quarter'])),
        'all_years':['All'] +list(set(orders['Year'])),
        'all_segments': ['All'] + segment_filtered,
        'all_ship_modes': ['All'] + ship_mode_filtered,
        'all_customers': ['All'] + cust_name_filtered,
        'all_categories': ['All'] + category_filtered,
        'all_sub_categories': ['All'] + sub_category_filtered,
        'all_products': ['All'] + prod_name_filtered,
        'all_x_axis': [x_axis] + [xax for xax in metrics if xax not in [x_axis, y_axis, 'Quantity']],
        'all_y_axis': [y_axis] + [yax for yax in metrics if yax not in [y_axis, x_axis, 'Quantity']]
    }

    if all(x == 'All' for x in requests):
        # logger.info('successfully loaded and transformed request for user', extra={'request_details':requests})
        return all_data, all_dict
    
    else:
        all_dict_modified = {
            'all_weeks' : all_dict['all_weeks'] if week =='All' else [week, 'All'] + [each for each in all_dict['all_weeks'] if each not in [week, 'All']],
            'all_months' : all_dict['all_months'] if month =='All' else [month,'All'] + [each for each in all_dict['all_months'] if each not in [month, 'All']],
            'all_quarters': all_dict['all_quarters'] if quarter =='All' else [quarter, 'All']+[each for each in all_dict['all_quarters'] if each not in [quarter, 'All']],
            'all_years' : all_dict['all_years'] if year =='All' else [year, 'All']+[each for each in all_dict['all_years'] if each not in [year, 'All']],
            'all_segments' : all_dict['all_segments'] if segment =='All' else [segment, 'All'] + [each for each in all_dict['all_segments'] if each not in [segment, 'All']],
            'all_ship_modes' : all_dict['all_ship_modes'] if ship_mode =='All' else [ship_mode,'All'] + [each for each in all_dict['all_ship_modes'] if each not in [ship_mode, 'All']],
            'all_customers': all_dict['all_customers'] if customer_name =='All' else [customer_name, 'All']+[each for each in all_dict['all_customers'] if each not in [customer_name, 'All']],
            'all_categories' : all_dict['all_categories'] if category =='All' else [category, 'All']+[each for each in all_dict['all_categories'] if each not in [category, 'All']],
            'all_sub_categories' : all_dict['all_sub_categories'] if sub_category =='All' else [sub_category, 'All']+[each for each in all_dict['all_sub_categories'] if each not in [sub_category, 'All']],
            'all_products': all_dict['all_products'] if product_name =='All' else [product_name, 'All']+[each for each in all_dict['all_products'] if each not in [product_name, 'All']],
            'all_x_axis': [x_axis] + [xax for xax in metrics if xax not in [x_axis, y_axis, 'Quantity']],
            'all_y_axis': [y_axis] + [yax for yax in metrics if yax not in [y_axis, x_axis, 'Quantity']]
        }

        # logger.info('successfully loaded and transformed request for user', extra={'request_details':requests})
        return all_data, all_dict_modified


def load_n_transform_to_tbl(postalcode='All', region='All', state='All', start_date='', end_date=''):
    requests = [postalcode, region, state]

    orders = pd.read_csv("data/orders.csv")
    returns = pd.read_csv("data/returns.csv")
    
    try:
        new_data = pd.read_csv("data/new_data.csv")
    except:
        new_data = pd.DataFrame()
    
    orders = pd.merge(orders, returns, left_on='Order ID', right_on='Order ID', how='left')
    
    orders = preprocess_data(orders, start_date, end_date)

    orders = filter_orders_tbl(orders, postalcode=postalcode, region=region, state=state)
    if len(new_data) > 0:
        new_data = filter_orders_tbl(new_data, postalcode=postalcode, region=region, state=state)


    orders['Returned'] = [1 if ret == 'Yes' else 0 for ret in orders['Returned']]
    relevant_cols = ['Postal Code', 'Region', 'State', 'City', 'Returned', 'Quantity', 'Sales', 'Discount']
    groupby_cols_rename =  {'Sum1':'Returned', 'Sum2':'Quantity', 'Sum3':'Sales', 'Average':'Discount'}
    orders_grouped = orders[relevant_cols].groupby(['Postal Code', 'Region', 'State', 'City']).agg(
        {'Returned':'sum', 'Quantity':'sum', 'Sales':'sum', 'Discount':'mean'}
        ).rename(columns=groupby_cols_rename).reset_index()

    if len(new_data) > 0:
        all_dict_tbl = {
            'all_postalcodes': ['All'] + list(set(orders_grouped['Postal Code'])) + list(set(new_data['Postal Code'])),
            'all_regions':  ['All'] + list(set(orders_grouped['Region'])) + list(set(new_data['Region'])),
            'all_states':['All'] + list(set(orders_grouped['State'])) + list(set(new_data['State']))
        }

        orders_grouped = pd.concat([new_data, orders_grouped])
    else:
        all_dict_tbl = {
            'all_postalcodes': ['All'] + list(set(orders_grouped['Postal Code'])),
            'all_regions':  ['All'] + list(set(orders_grouped['Region'])),
            'all_states':['All'] + list(set(orders_grouped['State']))
        }


    if all(x == 'All' for x in requests):
        # logger.info('successfully loaded and transformed request for user', extra={'request_details':requests})
        return orders_grouped, all_dict_tbl
    
    else:
        all_dict_tbl_modified = {
            'all_postalcodes' : all_dict_tbl['all_postalcodes'] if postalcode =='All' else [postalcode, 'All'] + [each for each in all_dict_tbl['all_postalcodes'] if each not in [postalcode, 'All']],
            'all_regions' : all_dict_tbl['all_regions'] if region =='All' else [region,'All'] + [each for each in all_dict_tbl['all_regions'] if each not in [region, 'All']],
            'all_states': all_dict_tbl['all_states'] if state =='All' else [state, 'All']+[each for each in all_dict_tbl['all_states'] if each not in [state, 'All']]
        }

        # logger.info('successfully loaded and transformed request for user', extra={'request_details':requests})
        return orders_grouped, all_dict_tbl_modified
    
def load_n_transform_metrics(start_date='', end_date=''):
    orders = pd.read_csv("data/orders.csv")
    returns = pd.read_csv("data/returns.csv")

    orders = pd.merge(orders, returns, left_on='Order ID', right_on='Order ID', how='left')
    orders = preprocess_data(orders, start_date, end_date)

    orders['Profit Ratio'] = [profit/sales for profit, sales in zip(orders['Profit'], orders['Sales']) ]

    avg_discount = sum(orders['Discount'])/len(orders)
    avg_discount_df = pd.DataFrame(data={
        'Values': [1-avg_discount, avg_discount],
        "Status": ['Difference', 'Actual']
    })

    profit_ratio = sum(orders['Profit Ratio'])/len(orders)
    profit_ratio_df = pd.DataFrame(data={
        'Values': [1-profit_ratio, profit_ratio],
        "Status": ['Difference', 'Actual']
    })

    all_metrics = {
        'Profit': sum(orders['Profit']),
        'Profit Ratio': profit_ratio_df,
        'Quantity': sum(orders['Quantity']),
        'Sales': sum(orders['Sales']),
        'Discount': avg_discount_df
    }

    return all_metrics