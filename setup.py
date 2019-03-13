from setuptools import setup, find_packages

setup(
    name="MacOSVersions",
    version="1.0.0",
    description="All macOS version list",
    author="sebastian",
    author_email="seba@cloudnative.co.jp",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml"
    ],
    entry_points={
        "console_scripts": [
        ]
    },
)
