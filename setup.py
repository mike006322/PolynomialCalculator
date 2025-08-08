"""Setup script for PolynomialCalculator package."""

import setuptools
import os.path

# Get version from the main package
def get_version():
    """Extract version from version.py (single source of truth)."""
    version_file = os.path.join(os.path.dirname(__file__), 'version.py')
    try:
        with open(version_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('__version__'):
                    return line.split('=')[1].strip().strip('"\'')
    except FileNotFoundError:
        pass
    return "0.1.0"

# Read README for long description
def get_long_description():
    """Get long description from README.md."""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding='utf-8') as fh:
            return fh.read()
    return ""

setuptools.setup(
    name="PolynomialCalculator",
    version=get_version(),
    author="Michael Angel", 
    author_email="mike00632@gmail.com",
    description="A comprehensive Python Computer Algebra System for polynomial computations",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/mike006322/PolynomialCalculator",
    project_urls={
        "Bug Tracker": "https://github.com/mike006322/PolynomialCalculator/issues",
        "Documentation": "https://github.com/mike006322/PolynomialCalculator",
        "Source Code": "https://github.com/mike006322/PolynomialCalculator",
    },
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        # Core dependencies - always required
    ],
    extras_require={
        # Optional dependencies for advanced features
        'algebra': ['numpy>=1.18.0', 'scipy>=1.5.0'],
        'dev': ['pytest>=6.0.0', 'pytest-cov>=2.10.0'],
        'all': ['numpy>=1.18.0', 'scipy>=1.5.0', 'pytest>=6.0.0', 'pytest-cov>=2.10.0'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="algebra polynomial mathematics computer-algebra-system cas",
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "polycalc=polynomials.cli:main",
        ],
    },
)