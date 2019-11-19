import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PolyCalc", # Replace with your own username
    version="1.0",
    author="Michael Angel",
    author_email="mike00632@gmail.com",
    description="Python Computer Algebra System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mike006322/PolynomialCalculator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)