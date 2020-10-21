# python setup.py sdist
# python -m twine upload dist/*
 
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
     name='ldfparser',  
     version='0.5.0-snapshot',
     author="Balazs Eszes",
     author_email="c4deszes@gmail.com",
     description="LDF Language support for Python",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/c4deszes/ldfparser",
     packages = find_packages(),
     package_data = { '': ['*.lark'] },
     license = 'MIT',
     keywords = ['LIN', 'LDF'],
     install_requires = ['lark-parser', 'bitstruct'],

     py_modules=['lin','parser'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     project_urls={
        "Documentation": "https://github.com/c4deszes/ldfparser/tree/master/README.md",
        "Source Code": "https://github.com/c4deszes/ldfparser",
     }
 )
