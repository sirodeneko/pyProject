from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from project.web.entity.areaInfo import views
from project.web.utils import docx_files


def index(request):
    return render(request, 'index.html')


def top(request):
    return render(request, 'top.html')


def menu(request):
    return render(request, 'menu.html')


def default(request):
    return render(request, 'default.html')


def multi_chart(request):
    context = {
        'name_list': views.get_area_list(),
        'i': 0,
    }
    return render(request, 'multiChart.html', context)


def single_chart(request):
    context = {
        'name_list': views.get_area_list(),
    }
    return render(request, 'singleChart.html', context)


def docx_report(request):
    context = {
        'name_list': views.get_area_list(),
        'show_box': False,
    }
    return render(request, 'docxReport.html', context)


def email(request):
    context = {
        'name_list': docx_files.docx_files_names(),
    }
    return render(request, 'emailIndex.html', context)
