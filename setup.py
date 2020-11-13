from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
     name='ldfparser',
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
     install_requires = ['lark-parser>=0.10.0', 'bitstruct'],
     python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4',
     py_modules=['lin','parser'],
     classifiers=[
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: 3.7",
         "Programming Language :: Python :: 3.8",
         "Programming Language :: Python :: 3.9",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     project_urls={
        "Documentation": "https://github.com/c4deszes/ldfparser/tree/master/README.md",
        "Source Code": "https://github.com/c4deszes/ldfparser",
     }
 )
