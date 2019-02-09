import re
import subprocess
import sys

import pip
from pip._internal import pep425tags

# package_install_path = raw_input()
package_name = "bokeh"
package_install_path = "/home/yonatanz/Documents/tmp/py_packages5/"

os_platform = "win_amd64"
abi = "cp36m"


def pip_download(package_name, package_install_path, os_platform, abi):
    py_ver = re.sub("\D", "", abi)
    # source-code hacks
    pep425tags.get_platform = lambda: os_platform  # set here
    pep425tags.get_abi_tag = lambda: abi  # set here
    sys.version_info = tuple([int(d) for d in py_ver])  # read to check version
    # now downloading all source (for other platforms to use) no need for hacks
    if "3" in py_ver:
        pip_ver = "pip3"
    else:
        pip_ver = "pip2"
    # install all in source
    print(subprocess.call([pip_ver, 'download', package_name, '-d', package_install_path + "sources/",
                           "--no-binary=:all:"]))
    # install all in requested os
    print(pip._internal.main(['download', package_name, '-d', package_install_path]))
    print("all packages are now installed :)")
