#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: hogelog
'''

from setuptools import setup

setup(name="kestrel-cli",
      version="0.0.1",
      description="kestrel command-line interface",
      license="MIT",
      author="hogelog",
      author_email="hogelog@hogel.org",
      url="http://github.com/hogelog/kestrel-cli",
      install_requires=["pykestrel"],
      package_dir={"kestrelcli": "kestrelcli"},
      packages=["kestrelcli"],
      entry_points={
          "console_scripts": {
              "kestrel-cli = kestrelcli.cli:main"
          },
      },
      keywords=["kestrel cli commandline"],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Topic :: Utilities"
      ])
