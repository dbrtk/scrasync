import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = []
with open('requirements.txt', 'r') as _file:
    for package in _file.readlines():
        package = package.strip()
        if package:
            install_requires.append(package)


setup(
    name="scrasync",
    version="0.0.1",
    author="Dominik Bartkowski",
    author_email="dominik.bartkowski@gmail.com",
    description="Scraping web pages asynchronously.",
    license="BSD",
    keywords="web scraper asyncio",
    url="http://dbrtk.net",
    packages=['scrasync', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        'Natural Language :: English',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',

        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',

    ],
    install_requires=install_requires,

)
