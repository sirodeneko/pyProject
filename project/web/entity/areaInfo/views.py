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
    t_code = request.GET.get('code', default='-1')
    area_infos = models.AreaInfo.objects.filter(code=t_code).reverse().all()[:7]
    context = {
        'name_list': get_area_list(),
        'i': 0,
    }
    return render(request, 'singleChart.html', context)
