import re
import subprocess
import sys
from multiprocessing import Process



# package_install_path = raw_input()
package_name = "bokeh"
package_install_path = "/home/yonatanz/Documents/tmp/py_packages5/"

os_platform = "win_amd64"
abi = "cp36m"


def peform_pip_download(args, os_platform, abi):
    import pip
    from pip._internal import pep425tags

    py_ver = re.sub("\D", "", abi)

    # source-code hacks
    pep425tags.get_platform = lambda: os_platform  # set here
    pep425tags.get_abi_tag = lambda: abi  # set here
    sys.version_info = tuple([int(d) for d in py_ver])  # read to check version
    return pip._internal.main(args)


def pip_download(package_name, package_install_path, os_platform, abi):
    # now downloading all source (for other platforms to use) no need for hacks
    # install all in source
    procs = []
    p1 = Process(target=peform_pip_download,
                args=(['download', package_name, '-d', package_install_path + "/sources/",
                       "--no-binary=:all:"], os_platform, abi))
    p1.start()
    procs.append(p1)

    if os_platform == 'linux_win_amd64':
        p = Process(target=peform_pip_download, args=(['download', package_name, '-d', package_install_path + "/win_amd64/"],
                                                      'win_amd64', abi))    # install all in requested os
        p.start()
        procs.append(p)

        p = Process(target=peform_pip_download, args=(['download', package_name, '-d', package_install_path + "/manylinux1_x86_64/"],
                                                      "manylinux1_x86_64", abi))    # install all in requested os
        p.start()
        procs.append(p)

    else:
        p = Process(target=peform_pip_download, args=(['download', package_name, '-d', package_install_path],
                                                      os_platform, abi))    # install all in requested os
        p.start()
        procs.append(p)

    res = True
    for p in procs:
        p.join()
        if p.exitcode != 0:
            res = False

    print("all packages are now installed :)")
    return res
