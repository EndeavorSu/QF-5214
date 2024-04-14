"""
plot line
"""

import numpy as np
import pandas as pd
from typing import NoReturn, Dict

from pyecharts.charts import Line
from pyecharts import options as opts


# color list
colors = ['#569ED2', '#31C5EA', '#ABCFE9', '#D5E3EA', '#63A0A1', '#5EBE80']
# color list for left y-axis
l_colors = colors[:-2]
# color list for right y-axis
r_colors = colors[-2:]


def transform_freq(dt_idx, freq):
    if freq == 'd':
        return list(map(lambda x: x.strftime('%Y-%m-%d'), dt_idx))
    elif freq == 'm':
        return list(map(lambda x: x.strftime('%Y-%m'), dt_idx))
    elif freq == 'y':
        return list(map(lambda x: x.strftime('%Y'), dt_idx))
    else:
        raise ValueError("Invalid frequency. Please use 'd', 'm', or 'y'.")
        

def plot_line(title: str, df:pd.DataFrame, col_dict:Dict, freq: str) -> NoReturn:
    """
    plot_line function is used to plot a line chart and save it to a specified path.

    Parameters:
    - title: str, the title of the line chart.
    - df: pd.DataFrame, the DataFrame containing the data.
    - col_dict: Dict, Keys are axis flags ('0': left or '1': right) and values are column names .
    - save_path: str, the path where the line chart will be saved. 

    Returns:
    - line: pyecharts.charts.Line, the plotted line chart object.

    """
    # prepare data
    # x-axis
    datetime_index = df.index.tolist()
    datetime_index = transform_freq(datetime_index, freq)

    # y-axis
    col_split = [col_dict.get(i, None) for i in range(2)]
    df_lst = [df[cols] for cols in col_split if cols is not None]
    
    ymax_lst, ymin_lst = (
        [
            round(np.max(df.to_numpy()) * 1.1)
            for df in df_lst], 
        [
            round(np.min(df.to_numpy()) * 1.1) if (df.to_numpy() < 0).any() else round(np.min(df.to_numpy()) * 0.8)
            for df in df_lst
        ]
    )
    
    data_lst = [df.to_dict(orient='list') for df in df_lst]

    # base
    line = (
        Line(init_opts=opts.InitOpts(bg_color='white', height='400px', width='600px'))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title,
                                      pos_top='top',
                                      pos_left='center'
                                     ),
            tooltip_opts=opts.TooltipOpts(trigger='axis', 
                                          formatter="{c}"
                                         ),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30),
                                     min_='dataMin',
                                     max_='dataMax'
                                    ),
            yaxis_opts=opts.AxisOpts(name='value',
                                     min_=ymin_lst[0],
                                     max_=ymax_lst[0],
                                     axislabel_opts=opts.LabelOpts(formatter='{value}', interval=5),
                                    ),
            datazoom_opts=opts.DataZoomOpts(type_='slider',
                                            range_start=0,
                                            range_end=100,
                                            is_realtime=True,
                                            pos_bottom='0%'
                                           ),
            legend_opts=opts.LegendOpts(is_show=True,
                                        pos_top='10%',
                                        orient='horizontal',
                                        border_width=0,
                                        item_gap=5)
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .add_xaxis(xaxis_data=datetime_index)
    )

    if len(data_lst) == 2:
        line = line.extend_axis(yaxis=opts.AxisOpts(name='value',
                                                    min_=ymin_lst[1],
                                                    max_=ymax_lst[1],
                                                    splitline_opts=opts.SplitLineOpts(is_show=False))
                               )

    # add y_axis
    for yaxis_index, data_dict in enumerate(data_lst):
        
        for idx, (name, da) in enumerate(data_dict.items()):
            
            if yaxis_index == 0:
                color = l_colors[idx % len(l_colors)]
            else:
                color = r_colors[idx % len(r_colors)]
                
            series_name = name + ' (right)' if yaxis_index == 1 else name
            
            line = line.add_yaxis(series_name=series_name,
                                  y_axis=[round(i, 4) for i in da],
                                  yaxis_index=yaxis_index,
                                  is_symbol_show=False,
                                  itemstyle_opts=opts.ItemStyleOpts(color=color),
                                  linestyle_opts=opts.LineStyleOpts(width=2)
                                 )

    # save chart
    line.render('../output_html/{}.html'.format(title))

    return line