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



def donut_chart(data, _type, bgcolor="white"):
    if _type == 'discount':
        color = '#C55A11'
        fig = px.pie(data, values='Values', names='Status', hole=.8, color='Status',
        color_discrete_map ={'Actual':color, 'Difference':'#F2F2F2'}, height=70)
    else:
        color = '#68D78D'
        fig = px.pie(data, values='Values', names='Status', hole=.8, color='Status',
        color_discrete_map ={'Actual':color, 'Difference':'#F2F2F2'}, height=70)

    try:
        rate = data[data['Status']=='Actual']['Values'].values[0]
        succ_rate = round(rate,3)*100
    except:
        succ_rate = 0
    fig.update_layout( annotations=[dict(text=str(round(succ_rate, 3))+"%", x=0.5, y=0.5, 
    font_size=14, font_color=color,showarrow=False)])
    fig.update_layout(plot_bgcolor =bgcolor, paper_bgcolor = bgcolor, showlegend=False)

    fig.update_traces(textinfo='none', hoverinfo="none", hovertemplate=None)
    fig.update_layout(margin_l=0)
    fig.update_layout(margin_r=0)
    fig.update_layout(margin_b=0)
    fig.update_layout(margin_t=0)

    return fig