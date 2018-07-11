#!/usr/bin/env python
# coding=utf-8


from setuptools import setup
from aliyun import __version__

setup(
    name='aliyun-dns-manager',
    version=__version__,
    author='fangwentong',
    author_email='fangwentong2012@gmail.com',
    license='MIT',
    packages=['aliyun'],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': ['aliyun-dns-manager=aliyun.dns_cli:main']
    },
    install_requires=['aliyun-python-sdk-alidns==2.0.6', 'PyYAML==3.12']
)
