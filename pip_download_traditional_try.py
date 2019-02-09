import os
import re
import subprocess
import sys

import pip
from pip._internal import pep425tags


# package_install_path = raw_input()
package_install_path = "/home/yonatanz/Documents/tmp/py_packages1/"

os_platform = "win_amd64"
abi = "cp36m"
imp = abi[:2]
ver = abi[2:]
py_ver = re.sub("\D", "", abi)

print(subprocess.call(["pip3", 'download', "bokeh", '-d', package_install_path,
                       "--no-binary=:all:"]))

def is_package_file(fname):
    return fname.endswith(".tar.gz") or fname.endswith(".whl") or fname.endswith(".zip")


folder_package_files = [fname for fname in os.listdir(package_install_path) if is_package_file(fname)
                        and os.path.isfile(os.path.join(package_install_path, fname))]

unique_packages = set([fname.split("-")[0] for fname in folder_package_files])
whl_packages = set([fname.split("-")[0] for fname in folder_package_files if fname.endswith(".whl")])
tar_packages = set(
    [fname.split("-")[0] for fname in folder_package_files if fname.endswith(".tar.gz") or fname.endswith(".zip")])

# assert tar_packages == unique_packages, "all packages should have tars"

for fname in folder_package_files:
    package_name = "-".join(fname.split("-")[:-1])
    if fname.endswith(".whl") or fname.endswith(".zip"):
        package_version = fname[:-4].split("-")[-1]
    else:  # fname.endswith(".tar.gz")
        package_version = fname.split(".tar.gz")[0].split("-")[-1]
    #  "--platform", "win_amd64",
    res = pip._internal.main(["pip3", 'download', package_name + "==" + package_version, '-d', package_install_path,
                              "--no-deps", "--implementation", imp, "--python-version", ver,
                              "--abi", abi])
    print(res)

folder_package_files = [fname for fname in os.listdir(package_install_path) if is_package_file(fname)]

unique_packages = set([fname.split("-")[0] for fname in folder_package_files])
whl_packages = set([fname.split("-")[0] for fname in folder_package_files if fname.endswith(".whl")])
tar_packages = set(
    [fname.split("-")[0] for fname in folder_package_files if fname.endswith(".tar.gz") or fname.endswith(".zip")])

install_from_source = tar_packages.difference(whl_packages)
assert tar_packages == unique_packages, "all packages should have tars"


def do_install_from_src(fname):
    return fname.split("-") in install_from_source and fname.endswith(".whl")


from_source_fnames = [fname for fname in folder_package_files if do_install_from_src(fname)]
from_whl_fnames = [fname for fname in folder_package_files if not do_install_from_src(fname)]

print("install from src")
print(from_source_fnames)

print("install from whl")
print(from_whl_fnames)