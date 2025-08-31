from setuptools import setup, find_packages

setup(
    name="youtube-info-app",
    version="1.0.0",
    description="YouTube Video Information App",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "requests==2.31.0",
        "gunicorn==21.2.0",
    ],
    python_requires=">=3.8",
)
