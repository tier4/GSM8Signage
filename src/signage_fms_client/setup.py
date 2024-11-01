#!/usr/bin/env python3

import os

from setuptools import setup


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths


package_name = "signage_fms_client"
setup(
    name=package_name,
    version="0.1.0",
    package_dir={"": "src"},
    packages=[package_name],
    data_files=[
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/signage_fms_client.launch.xml"]),
        ("share/" + package_name + "/config", ["config/fms_client_param.yaml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    author="Kah Hooi Tan",
    maintainer="Kah Hooi Tan",
    maintainer_email="kahhooi.tan@tier4.jp",
    keywords=["ROS"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    description=("for fms client with signage"),
    license="TODO",
    entry_points={
        "console_scripts": [
            "signage_fms_client = signage_fms_client.signage_fms_client:main",
        ]
    },
)
