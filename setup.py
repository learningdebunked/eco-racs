from setuptools import setup, find_packages

setup(
    name="carbon-aware-checkout",
    version="0.1.0",
    author="Kapil Poreddy",
    author_email="poreddykapil@ieee.org",
    description="Carbon-Aware Checkout: AI System for Real-Time Basket-Level Emissions Scoring",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/carbon-aware-checkout",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
