"""Dependencies for `persistent`."""

from setuptools import setup, find_packages


setup(
    name="persistent",
    description="A proof-of-concept persistent chatbot implementation",
    long_description=open("README.markdown", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    version="0.0.1",
    author="David Udell",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
)
