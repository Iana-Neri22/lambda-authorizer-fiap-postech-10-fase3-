from setuptools import setup, find_packages

setup(
    name="lambda-authorizer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyJWT==2.8.0",
        "pymysql==1.1.0",
        "python-dotenv==1.0.1",
    ],
) 