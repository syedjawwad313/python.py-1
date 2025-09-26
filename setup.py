from setuptools import setup, find_packages

setup(
    name="student-performance-dashboard",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "gunicorn==21.2.0",
    ],
    author="Syed Jawwad",
    description="A comprehensive Python application for managing student performance data",
    long_description=open("student_dashboard/README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/syedjawwad313/python.py-1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
