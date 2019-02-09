#!/usr/bin/env bash
read pip_dir_path

#package_install_path = "/home/yonatanz/Documents/tmp/py_packages5/"

for filename in $pip_dir_path/*.*;  do
    echo $filename
    pip3 install $filename
done
