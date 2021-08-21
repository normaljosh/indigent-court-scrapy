import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indigent-court-scrapy",
    version="0.1.0",
    author="Open Austin",
    author_email="info@open-austin.org",
    description="Scrapers for collecting data about appointed counsel in Texas courts",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="",
    project_urls={"Bug Tracker": "", "Documentation": "",},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["scrapy"],
    python_requires=">=3.8",
)
