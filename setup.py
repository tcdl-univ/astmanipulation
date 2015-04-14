from setuptools import setup, find_packages

setup(name="ASTManipulation",
      version="0.0.1",
      description="Ast manipulation for the ast library",
      author="Ernesto Bossi",
      author_email="bossi.ernestog@gmail.com",
      url="",
      license="BSD",
      py_modules=find_packages(exclude=('test')),
      keywords="Memory Database",
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Environment :: Console",
                   "Topic :: Database",
                   "License :: OSI Approved :: BSD License"],
      requires=[]
)