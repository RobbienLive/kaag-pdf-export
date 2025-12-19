"""
KAAG PDF Exports Package
A reusable Python package for generating styled PDF exports.
"""
from setuptools import setup, find_namespace_packages

setup(
    name="kaag-pdf-exports",
    version="0.2.9",
    description="Centralized PDF export styling for KAAG projects",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="KAAG Development Team",
    packages=find_namespace_packages(include=["kaag_pdf*"]),
    include_package_data=True,
    package_data={
        "kaag_pdf": ["assets/fonts/*.ttf", "assets/images/*"],
    },
    install_requires=[
        "reportlab>=4.0.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
