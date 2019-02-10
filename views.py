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


def get_name(request):
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
            pip_download.pip_download(form.cleaned_data['package'], package_folder, os_ver, abi)
            shutil.make_archive(package_folder, 'zip', package_folder + "/")

            shutil.rmtree(package_folder)

            for filename in os.listdir(DOWNLOAD_TMP_PATH):
                if filename.endswith(".zip"):  #
                    filepath = DOWNLOAD_TMP_PATH + filename
                    creation_time = os.path.getmtime(filepath)
                    hours, rest = divmod(time.time() - creation_time, 3600)
                    if hours >= 2:
                        shutil.rmtree(filepath)
                else:
                    continue

            wrapper = FileWrapper(open(package_folder + ".zip", 'rb'))
            print("hello world")
            print(package_folder + ".zip")
            response = HttpResponse(wrapper, content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(rand_name)

            return response

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'core/pip_downloader.html', {'form': form})