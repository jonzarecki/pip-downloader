﻿# coding=utf-8
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


# TODO: path for each server (home/ec2)
DOWNLOAD_TMP_PATH = "/home/ec2-user/pip_downloader/tmp/"
if not os.path.exists(DOWNLOAD_TMP_PATH):  # not in ec2
    DOWNLOAD_TMP_PATH = "/media/yonatanz/yz/tmp/"

all_os_version = ['win_amd64', '']

def get_name(request):
    msg = ''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            rand_name = str(int(time.time())) + "-" + str(random.random())[2:]
            package_folder = DOWNLOAD_TMP_PATH + rand_name
            abi = form.cleaned_data['abi_ver']
            os_ver = form.cleaned_data['os_version']
            res = pip_download.pip_download(form.cleaned_data['package'], package_folder, os_ver, abi)

            file_count = sum([len([f for f in files if not f.endswith(".py")]) for r, d, files in os.walk(package_folder)])
            if file_count != 0:  # found package
                shutil.make_archive(package_folder, 'zip', package_folder + "/")

                shutil.rmtree(package_folder, ignore_errors=True)

                for filename in os.listdir(DOWNLOAD_TMP_PATH):
                    if filename.endswith(".zip"):  #
                        filepath = DOWNLOAD_TMP_PATH + filename
                        creation_time = os.path.getmtime(filepath)
                        hours, rest = divmod(time.time() - creation_time, 3600)
                        if hours >= 1:
                            os.remove(filepath)
                            shutil.rmtree(filepath, ignore_errors=True)
                    else:
                        continue

                wrapper = FileWrapper(open(package_folder + ".zip", 'rb'))
                print(package_folder + ".zip")
                response = HttpResponse(wrapper, content_type='application/force-download')
                response['Content-Disposition'] = 'inline; filename=' + form.cleaned_data['package'] + '_' + os_ver + \
                                                  "-" + abi + '-' + '.zip'

                return response
            else:
                shutil.rmtree(package_folder, ignore_errors=True)
                msg = 'Package not found'

    # if a GET (or any other method) we'll create a blank form
    form = NameForm()

    return render(request, 'core/pip_downloader.html', {'form': form, 'msg': msg})
