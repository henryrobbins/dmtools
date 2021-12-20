from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dmtools",
    version="0.5.0",
    author="Henry Robbins",
    author_email="hwr26@cornell.edu",
    description="A Python package providing low-level tools for working with "
                "digital media programmatically.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henryrobbins/dmtools.git",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy>=1.19',
        'imageio>=2.9',
        'imageio-ffmpeg>=0.4.5',
        'scipy>=1.6',
        'typing>=3.7'
    ],
    extras_require= {
        "dev": ['pytest>=5',
                'mock>=3',
                'coverage>=4.5',
                'tox>=3']
    },
    python_requires='>=3.5',
)