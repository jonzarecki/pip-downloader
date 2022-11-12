import re
import sys
from multiprocessing import Process
from typing import NamedTuple

# package_install_path = raw_input()
package_name = "bokeh"

os_platform = "win_amd64"
abi = "cp36m"


def perform_pip_download(package_name, package_install_path, os_platform, abi, args=list()):
    import pip._internal
    from pip._vendor.distlib import util
    import pip._vendor.distlib.wheel as whl

    py_ver = re.sub(r"\D", "", abi)
    # source-code hacks
    util.get_platform = lambda: os_platform  # set here
    whl.ABI = abi  # lambda: abi  # set here
    # vi = Mock()
    sys_info = NamedTuple('sys_info', [('major', int), ('minor', int)])
    vi = sys_info(*[int(d) for d in py_ver])
    sys.version_info = vi  # tuple([int(d) for d in py_ver])  # read to check version
    res = pip._internal.main(['download', package_name, '-d', package_install_path] + args)
    return res


def pip_download(package_name, package_install_path, os_platform, abi):
    # now downloading all source (for other platforms to use) no need for hacks
    # install all in source

    procs = []
    p1 = Process(target=perform_pip_download,
                 args=(package_name, package_install_path + "/sources/", os_platform, abi, ["--no-binary=:all:"]))

    p1.start()
    procs.append(p1)

    if os_platform == 'linux_win_amd64':
        p = Process(target=perform_pip_download, args=(package_name, package_install_path + "/win_amd64/",
                                                      'win_amd64', abi))  # install all in requested os
        p.start()
        procs.append(p)

        p = Process(target=perform_pip_download, args=(package_name, package_install_path + "/manylinux1_x86_64/",
                                                      "manylinux1_x86_64", abi))  # install all in requested os
        p.start()
        procs.append(p)

    else:
        p = Process(target=perform_pip_download, args=(package_name, package_install_path,
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
