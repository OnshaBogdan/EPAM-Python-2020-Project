from setuptools import setup
from setuptools import find_packages

setup(name='employee-management',
      version='1.0',
      author='Bohdan Onsha',
      author_email='onsha.bogdan@gmail.com',
      url='https://github.com/OnshaBogdan/EPAM-Python-2020-Project',
      packages=find_packages(),
      scripts=['manage.py']
      )
