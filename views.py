# coding=utf-8
import random
import shutil
import subprocess
import time
from wsgiref.util import FileWrapper

from django.shortcuts import render

from uploads import pip_download
from uploads.core.forms import NameForm
import os
from django.http import HttpResponse


def home(request):
    return render(request, 'core/home.html')


DOWNLOAD_TMP_PATH = "/media/yonatanz/yz/tmp/"
