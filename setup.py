import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitcoin-easy",
    version="0.0.6",
    author="darosior",
    author_email="darosior@protonmail.com",
    description="Bitcoin for humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/darosior/bitcoin-easy",
    keywords='bitcoin blockchain address key bip', 
    packages=setuptools.find_packages(),
    install_requires=[
        'hashlib',
        'math',
        'time',
        'requests',
        'py_ecc',
        'scrypt',
        'pycrypto'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
