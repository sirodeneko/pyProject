from datetime import timezone, timedelta

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from project.web.entity.areaInfo import models
from project.web.utils import updata


def index(request):
    versions = models.Versions.objects.last()
    # 如果没有数据 就去拿数据
    if versions is None:
        return fetch(request)

    area_infos = models.AreaInfo.objects.filter(v_id=versions).order_by("-max_num")

    # for item in area_infos:
    #     print(item.name)

    context = {
        'data': area_infos,
        'i': 0,
    }
    return render(request, 'info_index.html', context)


def fetch(request):
    data = updata.getData()
    # 开启事务
    with transaction.atomic():
        version = models.Versions.objects.create()
        list_to_insert = []
        for row in data["Rows"]:
            item = models.AreaInfo(
                code=row["CODE"],
                name=row["NAME"],
                address=row["ADDRESS"],
                des=row["DES"],
                time=row["TIME"],
                grade=row["GRADE"],
                t_time=row["T_TIME"],
                max_num=row["MAX_NUM"] if row["MAX_NUM"] != "" else 0,
                ssd=row["SSD"],
                num=row["NUM"] if row["NUM"] != "" else 0,
                type=row["TYPE"],
                t_code=row["T_CODE"],
                v_id=version,
            )
            list_to_insert.append(item)
        # 批量插入
        models.AreaInfo.objects.bulk_create(list_to_insert)

    # 查询数据
    area_infos = models.AreaInfo.objects.filter(v_id=version).order_by("-max_num")

    context = {
        'data': area_infos,
        'i': 0,
    }

    return render(request, 'info_index.html', context)


def get_area_list():
    versions = models.Versions.objects.last()
    area_infos = models.AreaInfo.objects.filter(v_id=versions).order_by("-max_num")
    return area_infos


def get_single_chart(request):
    # 获取传过来的code 编号
    t_code = request.GET.get('code', default='-1')
    # id逆序取前7个
    v_list = models.Versions.objects.order_by("-id").all()[:7]
    vv_list = []
    vt_list = []
    # 获取vv_list(拿到版本号，用于之后in查询）
    # 获取vt_list(时间列表）
    for item in v_list:
        vv_list.append(item.id)
        # utc时区格式化为东八区（+8h)
        vt_list.append((item.v_time + timedelta(hours=8)).strftime("%m-%d %H"))
    # 反转（因为是逆序查询出来的）
    vt_list.reverse()
    # in查询出数据
    area_infos = models.AreaInfo.objects.filter(v_id__in=vv_list, code=t_code).all()
    context = {
        'name_list': get_area_list(),  # 名字列表
        'data': area_infos,  # 主要的数据
        'tName': area_infos[0].name,  # 获取当前的名字
        'tTime': vt_list,  # 时间列表
        'i': 0,
    }
    return render(request, 'singleChart.html', context)


def get_multi_chart(request):
    # 拿到参数列表
    t_code = request.GET.getlist('code', default=[])
    # 判断是否为空
    if t_code is []:
        context = {
            'name_list': get_area_list(),
        }
        return render(request, 'multiChart.html', context)

    # 老规矩
    v_list = models.Versions.objects.order_by("-id").all()[:7]
    vv_list = []
    vt_list = []
    for item in v_list:
        vv_list.append(item.id)
        # utc时区格式化为东八区（+8h)
        vt_list.append((item.v_time + timedelta(hours=8)).strftime("%m-%d %H"))

    vt_list.reverse()
    areas_infos = []
    # 对于每个参数code都进行一次查询 丢到areas_infos中去
    for i_code in t_code:
        areas_infos.append(models.AreaInfo.objects.filter(v_id__in=vv_list, code=i_code).all())

    # 获取每个对应的名字，因为在模板中不方便获取这个值
    t_name_list = []
    for item in areas_infos:
        t_name_list.append(item.first().name)
    context = {
        'name_list': get_area_list(),
        't_name_list': t_name_list,
        'data': areas_infos,
        'tTime': vt_list,
        'i': 0,
    }
    return render(request, 'multiChart.html', context)
