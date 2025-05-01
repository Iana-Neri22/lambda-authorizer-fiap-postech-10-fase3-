from setuptools import setup, find_packages

setup(
    name="lambda-authorizer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyJWT",
    ],
) 