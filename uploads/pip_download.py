import os
import re
import shutil
import subprocess
import sys
from multiprocessing import Process

# package_install_path = raw_input()
package_name = "bokeh"
package_install_path = "/home/yonatanz/Documents/tmp/py_packages5/"

os_platform = "win_amd64"
abi = "cp36m"

install_file_path = os.path.dirname(os.path.realpath(__file__)) + "/install_all_packages.py"


def peform_pip_download(package_name, package_install_path, os_platform, abi, args=list()):
    import pip
    from pip._internal import pep425tags

    py_ver = re.sub("\D", "", abi)

    # source-code hacks
    pep425tags.get_platform = lambda: os_platform  # set here
    pep425tags.get_abi_tag = lambda: abi  # set here
    sys.version_info = tuple([int(d) for d in py_ver])  # read to check version
    res = pip._internal.main(['download', package_name, '-d', package_install_path] + args)
    shutil.copy(install_file_path, package_install_path)  # install path
    print(args[-1])
    return res


def pip_download(package_name, package_install_path, os_platform, abi):
    # now downloading all source (for other platforms to use) no need for hacks
    # install all in source
    procs = []
    p1 = Process(target=peform_pip_download,
                 args=(package_name, package_install_path + "/sources/", os_platform, abi, ["--no-binary=:all:"]))

    p1.start()
    procs.append(p1)
    # shutil.copy(install_file_path, package_install_path + "/sources/"[-1])  # install path

    if os_platform == 'linux_win_amd64':
        p = Process(target=peform_pip_download, args=(package_name, package_install_path + "/win_amd64/",
                                                      'win_amd64', abi))  # install all in requested os
        p.start()
        procs.append(p)

        p = Process(target=peform_pip_download, args=(package_name, package_install_path + "/manylinux1_x86_64/",
                                                      "manylinux1_x86_64", abi))  # install all in requested os
        p.start()
        procs.append(p)

    else:
        p = Process(target=peform_pip_download, args=(package_name, package_install_path,
                                                      os_platform, abi))  # install all in requested os
        p.start()
        procs.append(p)

    res = True
    for p in procs:
        p.join()
        if p.exitcode != 0:
            res = False

    print("all packages are now installed :)")
    return res
