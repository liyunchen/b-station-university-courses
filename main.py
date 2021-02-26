# -*- coding: utf-8 -*-

## 李运辰 2021-2-18

import requests
from lxml import etree
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts.charts import Pie
import pandas as pd
import json
from stylecloud import gen_stylecloud
import jieba

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',}

###饼状图
def pie(name,value,picname,tips):
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(name, value)],
            # 饼图的中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标
            # 默认设置成百分比，设置成百分比时第一项是相对于容器宽度，第二项是相对于容器高度
            center=["35%", "50%"],
        )
            .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])  # 设置颜色
            .set_global_opts(
            title_opts=opts.TitleOpts(title=""+str(tips)),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="70%", orient="vertical"),  # 调整图例位置
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render(str(picname)+".html")
    )

###柱形图
def bars(name,dict_values):

    # 链式调用
    c = (
        Bar(
            init_opts=opts.InitOpts(  # 初始配置项
                theme=ThemeType.MACARONS,
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="cubicOut"  # 初始动画延迟和缓动效果
                ))
        )
            .add_xaxis(xaxis_data=name)  # x轴
            .add_yaxis(series_name="up主昵称", yaxis_data=dict_values)  # y轴
            .set_global_opts(
            title_opts=opts.TitleOpts(title='李运辰', subtitle='up视频数',  # 标题配置和调整位置
                                      title_textstyle_opts=opts.TextStyleOpts(
                                          font_family='SimHei', font_size=25, font_weight='bold', color='red',
                                      ), pos_left="90%", pos_top="10",
                                      ),
            xaxis_opts=opts.AxisOpts(name='up主昵称', axislabel_opts=opts.LabelOpts(rotate=45)),
            # 设置x名称和Label rotate解决标签名字过长使用
            yaxis_opts=opts.AxisOpts(name='大学生学习视频视频数'),

        )
            .render("up主大学生学习视频视频数.html")
    )







dataset  = pd.read_csv('Bili\\lyc大学课程.csv',encoding="gbk")
title = dataset['title'].tolist()
url = dataset['url'].tolist()
watchnum = dataset['watchnum'].tolist()
dm = dataset['dm'].tolist()
uptime = dataset['uptime'].tolist()
upname = dataset['upname'].tolist()


##"大学生学习视频播放量排名"  &&  大学生学习视频弹幕量排名"
def analysis1(data_dict,piename):
    itemNames = []
    datas = []
    for i in range(len(data_dict) - 1, len(data_dict) - 13, -1):
        itemNames.append(data_dict[i][0])
        datas.append(data_dict[i][1])
    pie(itemNames, datas, piename, piename)

#分析1:  & 分析2
def getdata1_2():
    watchnum_dict = {}
    dm_dict = {}
    for i in range(0, len(watchnum)):
        if "万" in watchnum[i]:
            watchnum[i] = int(float(watchnum[i].replace("万", "")) * 10000)
        else:
            watchnum[i] = int(watchnum[i])

        if "万" in dm[i]:
            dm[i] = int(float(dm[i].replace("万", "")) * 10000)
        else:
            dm[i] = int(dm[i])

        watchnum_dict[title[i]] = watchnum[i]
        dm_dict[title[i]] = dm[i]

    ###从小到大排序
    watchnum_dict = sorted(watchnum_dict.items(), key=lambda kv: (kv[1], kv[0]))
    dm_dict = sorted(dm_dict.items(), key=lambda kv: (kv[1], kv[0]))
    #分析1：大学生学习视频播放量排名"
    analysis1(watchnum_dict,"大学生学习视频播放量排名")
    #分析2：大学生学习视频弹幕量排名
    analysis1(dm_dict,"大学生学习视频弹幕量排名")

#分析3: up主大学生学习视频视频数
def getdata3():
    upname_dict = {}
    for key in upname:
        upname_dict[key] = upname_dict.get(key, 0) + 1
        ###从小到大排序
    upname_dict = sorted(upname_dict.items(), key=lambda kv: (kv[1], kv[0]))
    itemNames = []
    datas = []
    for i in range(len(upname_dict) - 1, len(upname_dict) - 21, -1):
        itemNames.append(upname_dict[i][0])
        datas.append(upname_dict[i][1])
    #绘图
    bars(itemNames,datas)


#分析4: 大学课程名称词云化
def getdata4():

    text = "".join(title)
    with open("stopword.txt","r", encoding='UTF-8') as f:
        stopword = f.readlines()
    for i in stopword:
        print(i)
        i = str(i).replace("\r\n","").replace("\r","").replace("\n","")
        text = text.replace(i, "")
    word_list = jieba.cut(text)
    result = " ".join(word_list)  # 分词用 隔开
    # 制作中文云词
    icon_name = 'fab fa-qq'
    """
    # icon_name='',#国旗
    # icon_name='fas fa-dragon',#翼龙
    icon_name='fas fa-dog',#狗
    # icon_name='fas fa-cat',#猫
    # icon_name='fas fa-dove',#鸽子
    # icon_name='fab fa-qq',#qq
    """
    gen_stylecloud(text=result, icon_name=icon_name, font_path='simsun.ttc', output_name="大学课程名称词云化.png")  # 必须加中文字体，否则格式错误

#分析1:  & 分析2
#getdata1()
#分析3: up主大学生学习视频视频数
#getdata3()
#分析4：大学课程名称词云化
#getdata4()



