"""
Author: Tom Cuypers
"""

import setuptools

setuptools.setup(
    name="pylint_error_handling",
    # don't forget to update the releases.md file as well if you update this number
    version="0.1.0",
    author="Tom Cuypers",
    author_email="tcuypers@gmail.com",
    license='',
    description="A set of additional pylint rules we can use in our projects",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Commercial",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11, <3.13',
    install_requires=[
        "astroid>=3.2.2",
        "pylint>=3.0.0"
    ],
    zip_safe=False
)