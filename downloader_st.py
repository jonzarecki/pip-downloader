import os
import pathlib
import random
import shutil
import time
from wsgiref.util import FileWrapper

import streamlit as st

import pip_download

ABI_VERSION = (
	'cp38m',
	'cp37m',
	'cp36m',
	'cp35m',
	'cp27m',
)
OS_CHOICES = (
	'linux_win_amd64',
	'win_amd64',
	'manylinux1_x86_64',
	'win32',
	# ('none', 'none - can try if no wheel exists')
)
# HACK This only works when we've installed streamlit with pipenv, so the
# permissions during install are the same as the running process
STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / 'static'
# We create a downloads directory within the streamlit static asset directory
# and we write output files to it
DOWNLOAD_TMP_PATH = (STREAMLIT_STATIC_PATH / "downloads/").as_posix() + "/"
if __name__ == '__main__':
	st.set_page_config(layout="centered")
	st.header("Pip Downloader")

	package = st.text_input(label='Package name')

	abi = st.selectbox(options=ABI_VERSION, label='Python version', index=1)
	os_ver = st.selectbox(options=OS_CHOICES, label='OS')
	c1, c2, c3 = st.columns(3)

	if c2.button("Start Download"):
		# process the data in form.cleaned_data as required
		rand_name = str(int(time.time())) + "-" + str(random.random())[2:]
		package_folder = DOWNLOAD_TMP_PATH + rand_name
		res = pip_download.pip_download(package, package_folder, os_ver, abi)

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
			with open(package_folder + ".zip", "rb") as f:
				c2.download_button(label="Download package zip!",
								   data=f,
								   file_name=package + '_' + os_ver + "-" + abi + '-' + '.zip',
								   mime="application/zip")
		else:
			shutil.rmtree(package_folder, ignore_errors=True)
			st.error('Package not found')
