from setuptools import find_packages, setup

setup(
    name="datahopper",
    version="0.1.0",
    description="Python package for data engineering and data wrangling",
    license="MIT",
    author="Tomas Carvalho",
    author_email="tomas.jpeg@gmail.com",
    url="https://github.com/tomasoak/datahopper",
    python_requires=">=3.8.*",
    packages=find_packages(include=["datahopper", "datahopper.*"]),
    install_requires=["pandas>=1.4", "numpy>=1.22"],
)
