import os
import sys

from jamstack import __version__
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist")
    os.system("twine upload dist/* --skip-existing")
    sys.exit()

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="jamstack",
    version=__version__,
    description="Jamstack in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jamstackpy/jamstack",
    author="Abdur-Rahmaan Janhangeer",
    author_email="arj.python@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="jamstack static",
    packages=["jamstack"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=open(
        os.path.join(here, "requirements.txt"), encoding="utf-8"
    )
    .read()
    .split("\n"),
    project_urls={
        "Bug Reports": "https://github.com/jamstackpy/jamstack/issues",
        "Source": "https://github.com/jamstackpy/jamstack",
    },
    entry_points={"console_scripts": ["jamstack=jamstack.__main__:main"]},
)
