import setuptools
from glob import glob
from os.path import basename
from os.path import splitext


def long_description():
    with open("readme.md", "r", encoding='utf-8') as fh:
        return fh.read()


def requires_from_file(filename):
    with open(filename) as f:
        return f.read().splitlines()


setuptools.setup(
    name="dymdao",
    version="0.1.0",
    author="umaxyon",
    author_email="umaxyon@gmail.com",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/umaxyon/dymdao",
    packages=setuptools.find_packages('src'),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires_from_file('requirements.txt')
)
