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
    p2 = Process(target=peform_pip_download,
                args=(['download', package_name, '-d', package_install_path + "/sources/",
                       "--no-binary=:all:"], os_platform, abi))
    p2.start()

    p1 = Process(target=peform_pip_download, args=(['download', package_name, '-d', package_install_path],
                                                  os_platform, abi))    # install all in requested os
    p1.start()
    p1.join()
    p2.join()
    print("all packages are now installed :)")

    res1 = p1.exitcode
    res2 = p2.exitcode
    return str(res1) + " " + str(res2)
