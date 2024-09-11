import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, datetime, timedelta
import json
import base64
import pandas as pd
import numpy as np
from collections import defaultdict
import time
import logging
from functools import reduce
from collections import OrderedDict

color_map = {
		"Profit":"#8497B0",
		"Profit Ratio": "#3693AC",
		"Discount": "#F4B183",
        "Days to Ship": "#BFBFBF",
        "Quantity": "#339966",
        "Returned": "#FF0000",
        "Sales": "#B381D9",
	}


def generate_combo_charts(data_dict, x_axis=None, y_axis=None):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    ys = y_axis 
    keys = list(data_dict.keys())
    for y, k in zip(ys, keys):
        data = data_dict[k]
        try:
            x_axis=data['Order Date']
        except:
            try:
                x_axis=data['Month']
            except:
                x_axis=data['Year']

        if y in ['Profit Ratio']: #simple differentiator between line and bar chart types
            txt_list = data[y]
            fig.add_trace( 
                go.Scatter(x=x_axis, y=data[y], marker_color=color_map[y], mode='lines+markers+text',
            text=[str(round(d*100, 1)) + "%" for d in txt_list], name=y), secondary_y=False
                )


        else :
            txt_list = data[y]
            
            fig.add_trace(
                go.Bar(x=x_axis, y=data[y], marker_color=color_map[y],
                text=[str(round((d/1000), 1))+"K" if d/1000 >=1 and d/1000 < 500 
                else str(round((d/1000000), 1))+"M" if d/1000000 >=0.5 else round(d, 1) for d  in txt_list],
                name=y), secondary_y=True, 
                )
            

    fig.update_yaxes(visible=False, showticklabels=False, automargin=False)
    fig.update_layout(autosize=False, plot_bgcolor ="white",paper_bgcolor = "white", height=230, width=875.5,
        showlegend=True,
        legend=dict(yanchor="bottom",y=-0.6,xanchor="right",x=0.6, orientation="h"),
        legend_title_text='')
    fig.update_layout(margin_l=0)
    fig.update_layout(margin_r=0)
    fig.update_layout(margin_b=0)
    fig.update_layout(yaxis_title=None, xaxis_title=None)
    fig.update_layout(font_size=11)
    fig.update_layout(margin=dict(b=0, t=10, l=0, r=0))
    

    return fig


def generate_single_charts(data, y_axis=None):
    try:
        x_axis=data['Order Date']
    except:
        try:
            x_axis=data['Month']
        except:
            x_axis=data['Year']
    txt_list = data[y_axis]
    fig = go.Figure(go.Bar(x=x_axis, y=data[y_axis], marker_color = color_map[y_axis], name = y_axis,
        text=[str(round((d/1000), 1))+"K" if d/1000 >=1 and d/1000 < 500 
        else str(round((d/1000000), 1))+"M" if d/1000000 >=0.5 else round(d,1) for d  in txt_list])
    )
    

    fig.update_yaxes(visible=False, showticklabels=False, automargin=False)
    fig.update_layout(plot_bgcolor ="white",paper_bgcolor = "white",
        showlegend=True,
        legend=dict(yanchor="bottom",y=-0.9,xanchor="right",x=0.6, orientation="h"),
        legend_title_text='')
    fig.update_traces(hoverinfo="none", hovertemplate=None, textfont_size=11,
        textposition="outside", cliponaxis=False)
    fig.update_layout(margin_l=0)
    fig.update_layout(margin_r=0)
    fig.update_layout(margin_b=0)
    fig.update_layout(yaxis_title=None, xaxis_title=None)
    fig.update_layout(font_size=11)
    fig.update_layout(margin=dict(b=10, t=10, l=0, r=0))

    return fig


def generate_bubble_chart(data, x_axis=None, y_axis=None, color=None, size=None):
    fig = px.scatter(data, x=x_axis, y=y_axis, color=color, size=size)
    # fig.update_yaxes(visible=False, showticklabels=False, automargin=False)
    fig.update_layout(plot_bgcolor ="white",paper_bgcolor = "white",
        showlegend=True,
        legend=dict(yanchor="bottom",y=-0.6,xanchor="right",x=0.6, orientation="h"),
        legend_title_text='')
    # fig.update_traces(hoverinfo="none", hovertemplate=None, textfont_size=11,
    #     textposition="outside", cliponaxis=False)
    fig.update_layout(margin_l=0)
    fig.update_layout(margin_r=0)
    fig.update_layout(margin_b=0)
    fig.update_layout(yaxis_title=None, xaxis_title=None)
    fig.update_layout(font_size=11)
    fig.update_layout(margin=dict(b=10, t=10, l=0, r=0))

    return fig





