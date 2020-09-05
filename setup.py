# python setup.py sdist
# python -m twine upload dist/*
 
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='ldfparser',  
     version='0.2.0',
     author="Balazs Eszes",
     author_email="c4deszes@gmail.com",
     description="LDF Language support for Python",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/c4deszes/ldfparser",
     packages = ['ldfparser'],
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