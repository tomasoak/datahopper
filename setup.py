from setuptools import setup, find_packages

setup(
  author="Tomas Carvalho",
  description="Complete package for data wrangling in python.",
  name="ds_toolkit",
  version="0.1.0",
  packages=find_packages(include=["ds_toolkit", "ds_toolkit.*"])
)