from setuptools import find_packages, setup
from pathlib import Path


cwd = Path(__file__).parent
long_description = (cwd / "README.md").read_text()

setup(
    name="unbelievaboat",
    version="1.2.0",
    author="yoggys",
    author_email="yoggies@yoggies.ovh",
    description="Wrapper for UnbelievaBoat API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoggys/unbelievaboat",
    packages=find_packages(),
    install_requires=[
        "aiohttp ~= 3.8.4",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords=["python", "unb", "unbelievaboat", "api", "wrapper", "async", "asyncio"],
)
