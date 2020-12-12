import random

from pyecharts.charts import Bar, Line
from pyecharts import options as opts

# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot


# 生成随机字符串
def generate_random_str(random_length=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(random_length):
        random_str += base_str[random.randint(0, length)]
    return random_str


def random_color():
    color_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += color_arr[random.randint(0, 14)]
    return "#" + color


def create_single(t_time, areas_info):
    html_name = './project/web/temp/' + generate_random_str(random_length=10) + '.html'
    png_name = './project/web/temp/' + generate_random_str(random_length=10) + '.png'
    line = Line()
    line.add_xaxis(t_time)
    line.add_yaxis(
        'visitor flow',
        [item.num for item in areas_info],
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_='min', name='最大流量'),
                opts.MarkLineItem(type_='max', name='最小流量'),
            ],
            linestyle_opts=opts.LineStyleOpts(width=1, color='#FF0000', opacity=0.5, type_='dashed')
        ),
    ),

    # options
    line.set_global_opts(
        title_opts=opts.TitleOpts(title='single data per hour', subtitle=areas_info[0].name, pos_right="center"),
        legend_opts=opts.LegendOpts(pos_top='bottom', pos_left="center"),
        xaxis_opts=opts.AxisOpts(name='time', name_location='middle', name_gap=20,
                                 splitline_opts=opts.SplitLineOpts(is_show=False)),
        yaxis_opts=opts.AxisOpts(name='visitor flow', position='center', name_location='middle', name_gap=40,
                                 splitline_opts=opts.SplitLineOpts(is_show=False)),
    )
    line.set_series_opts(
        label_opts=opts.LabelOpts(
            is_show=True,
            position='top'
        ),
    )

    # 输出保存为图片
    make_snapshot(snapshot, line.render(html_name), png_name)
    return png_name


def create_multi(t_time, areas_infos):
    html_name = './project/web/temp/' + generate_random_str(random_length=10) + '.html'
    png_name = './project/web/temp/' + generate_random_str(random_length=10) + '.png'
    line = Line()
    line.add_xaxis(t_time)
    for areas_info in areas_infos:
        line.add_yaxis(
            areas_info[0].name,
            [item.num for item in areas_info],
        ),

    # options
    line.set_global_opts(
        title_opts=opts.TitleOpts(title='Multi-attraction Data Comparison', subtitle='data per hour',
                                  pos_right="center"),
        legend_opts=opts.LegendOpts(pos_top='bottom', pos_left="center"),
        xaxis_opts=opts.AxisOpts(name='time', name_location='middle', name_gap=20, boundary_gap=False,
                                 splitline_opts=opts.SplitLineOpts(is_show=False)),
        yaxis_opts=opts.AxisOpts(name='visitor flow', position='center', name_location='middle', name_gap=40,
                                 splitline_opts=opts.SplitLineOpts(is_show=False)),
    )
    line.set_series_opts(
        label_opts=opts.LabelOpts(
            is_show=True,
            position='top'
        ),
        areastyle_opts=opts.AreaStyleOpts(
            opacity=0.5,
            color=random_color(),
        )
    )

    # 输出保存为图片
    make_snapshot(snapshot, line.render(html_name), png_name)
    return png_name
