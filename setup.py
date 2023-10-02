# -*- coding: utf-8 -*-
"""
streamlit-jupyter-magic setup
"""
import io
import os

import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(file, name="__version__"):
    """
    Get the version of the package from the given file by
    executing it and extracting the given `name`.
    """
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


__version__ = get_version(os.path.join(HERE, "streamlit_jupyter_magic/_version.py"))

with io.open(os.path.join(HERE, "README.md"), encoding="utf8") as fh:
    long_description = fh.read()

setup_args = dict(
    name="streamlit-jupyter-magic",
    version=__version__,
    url="https://github.com/comet-ml/streamlit-jupyter-magic",
    author="Streamlit Jupyter Magic Development Team",
    description="Manager for Jupyter streamlit servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "streamlit",
        "rich",
        "psutil",
        "matplotlib",
        "numpy",
    ],
    packages=[
        "streamlit_jupyter_magic",
    ],
    include_package_data=True,
    python_requires=">=3.7",
    license="Apache 2.0 License",
    platforms="Linux, Mac OS X, Windows",
    keywords=["data science", "python"],
    classifiers=[
        "License :: OSI Approved :: Apache 2.0 License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Jupyter",
    ],
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
