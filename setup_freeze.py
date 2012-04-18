#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: hogelog
'''

from cx_Freeze import setup, Executable

setup(name="kestrel-cli",
      version="0.0.1",
      description="kestrel command-line interface",
      license="MIT",
      author="hogelog",
      author_email="hogelog@hogel.org",
      url="http://github.com/hogelog/kestrel-cli",
      package_dir={"kestrelcli": "kestrelcli"},
      packages=["kestrelcli"],
      keywords=["kestrel cli commandline"],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Topic :: Utilities"
      ],
      options={"build_exe": {
        "packages": ["os"], "excludes": ["tkinter"]
        }
      },
      executables=[Executable("kestrelcli/cli.py", targetName="kestrel-cli.exe", base="Console")])
