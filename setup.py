from setuptools import setup, find_packages

setup(
    name="data_hopper",
    version="0.1.0",
    description="Package for data wrangling in python.",
    license='MIT',
    author="Tomas Carvalho",
    author_email="tomas.jpeg@gmail.com",
    url="https://github.com/tomasoak/data_hopper",
    python_requires=">=3.8.*",
    packages=find_packages(include=["data_hopper", "data_hopper.*"]),
    install_requires=["pandas>=1.4", "numpy>=1.22"]
)
