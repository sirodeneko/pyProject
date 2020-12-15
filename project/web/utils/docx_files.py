import json
import os
import re
import urllib.request


def docx_files_names():
    file_path = './static/reports/'
    files = os.listdir(file_path)
    names = []
    for item in files:
        if item.endswith('.docx'):
            names.append(item)
    return names

