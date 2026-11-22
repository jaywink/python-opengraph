import re
from setuptools import setup, find_packages

install_requires = ["beautifulsoup4>=4.3", "requests>=2.7"]

# Get version
# Tip fromhttps://stackoverflow.com/a/7071358/1489738
with open("opengraph/__version__.py") as version_file:
    version_string = version_file.read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_string, re.M)
if mo:
    __version__ = mo.group(1)
else:
    raise RuntimeError("Unable to find version string.")

setup(
    name="python-opengraph-jaywink",
    version=__version__,
    description="Python module to parse Open Graph metadata on web pages",
    url="https://github.com/jaywink/python-opengraph",
    license="MIT",
    author="Jason Robinson",
    author_email="mail@jasonrobinson.me",
    install_requires=install_requires,
    python_requires=">=3.10",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    keywords="opengraph")
