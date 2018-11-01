import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitcoin-utils",
    version="0.0.1",
    author="darosior",
    author_email="darosior@protonmail.com",
    description="Useful Bitcoin functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/darosior/bitcoin-utils",
    keywords='bitcoin blockchain address key bip' 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
