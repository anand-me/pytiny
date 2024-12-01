from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytiny",
    version="0.1.0",
    author="Akshay Anand",
    author_email="me.akanand@gmail.com",
    description="A lightweight URL shortener library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anand-me/pytiny",
    package_dir={"": "src"},  # This tells setuptools that packages are under src directory
    packages=find_packages(where="src"),  # This will find all packages under src
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
        "qrcode>=7.3.1",
        "pillow>=8.0.0",  # Required for QR code generation
        "gunicorn>=20.1.0",
        "python-dotenv>=0.19.0"
    ],
    entry_points={
        "console_scripts": [
            "pytiny=pytiny.cli:main",
            "pytiny-web=pytiny.web:app.run"
        ],
    },
)
