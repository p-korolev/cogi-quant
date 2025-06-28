from pathlib import Path
from setuptools import find_packages, setup

this_dir = Path(__file__).resolve().parent
readme = (this_dir / "README.md").read_text(encoding="utf-8")

# setup metadata
setup(
    # pip install name
    name="cogi-quant",

    version="1.0.0",

    packages=find_packages(exclude=("tests", "docs", "examples")),

    # runtime dependencies
    install_requires=[
        "pandas>=1.5",
        "numpy>=1.24",
        "scipy>=1.10",
        "matplotlib>=3.7",
        "yfinance>=0.2"
    ],

    python_requires=">=3.9",
    author="Phillip Korolev",
    author_email="p.korolev1@outlook.com",
    url="https://github.com/p-korolev/cogi-quant",
    description="Toolkit for quantitative market analysis",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
    ],

    project_urls={
        "Source": "https://github.com/p-korolev/cogi-quant",
    },
)
