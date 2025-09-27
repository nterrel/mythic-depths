from setuptools import setup, find_packages

setup(
    name="mythic-depths",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "mythic-depths=game:main",  # Replace `game:main` with your entry point
        ],
    },
)