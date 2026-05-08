#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RenameFlow - Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = ""
readme_path = this_directory / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding='utf-8')

setup(
    name="renameflow",
    version="1.0.0",
    author="RenameFlow Team",
    author_email="renameflow@example.com",
    description="🔄 Lightweight Batch File Renaming Tool - 轻量级批量文件重命名工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/RenameFlow",
    license="MIT",
    py_modules=["renameflow"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "renameflow=renameflow:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Desktop Environment :: File Managers",
    ],
    python_requires=">=3.8",
    keywords="rename, batch, files, cli, tool, utility",
)
