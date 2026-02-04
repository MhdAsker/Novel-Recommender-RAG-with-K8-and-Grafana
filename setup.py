from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="BOOK-RECOMMENDER",
    version="0.1",
    author="Asker",
    packages=find_packages(),
    install_requires = requirements,
)