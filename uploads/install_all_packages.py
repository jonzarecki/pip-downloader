import os
import subprocess

directory = os.path.dirname(os.path.realpath(__file__))
for filename in os.listdir(directory):
    if filename.endswith(".whl") or filename.endswith(".tar.gz") or filename.endswith(".zip"):
        filepath = os.path.join(directory, filename)
        subprocess.call(["pip3", 'install', filepath])
        # subprocess.call(["twine", 'upload', filepath, ])
