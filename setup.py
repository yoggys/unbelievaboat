from pathlib import Path

from setuptools import find_packages, setup

cwd = Path(__file__).parent
long_description = (cwd / "README.md").read_text()

setup(
    name="unbelievaboat",
    version="2.1.1",
    author="yoggys",
    author_email="yoggies@yoggies.dev",
    description="Wrapper for UnbelievaBoat API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoggys/unbelievaboat",
    packages=find_packages(),
    install_requires=[
        "aiohttp ~= 3.9.2",
        "typing_extensions ~= 4.12.2",
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
