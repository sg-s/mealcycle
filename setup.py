from setuptools import find_packages, setup

setup(
    name="mealcycle",
    version="22.12.8",
    packages=find_packages(exclude=("tests", "docs")),
    description="Meal cycler",
    url="https://github.com/sg-s/mealcycle",
    author="Srinivas Gorur-Shandilya",
    author_email="code@srinivas.gs",
    install_requires=["pandas>=1.3.2", "streamlit", "watchdog"],
    extras_require={
        "dev": [
            "interrogate>=1.0",
            "pytest",
            "black",
        ]
    },
)
