import setuptools


setuptools.setup(
    name="fast_file_transfer",  # Replace with your own username
    version="0.0.1",
    author="Ryan Wicks",
    author_email="rwicks@2grobotics.com",
    description="Tool for copying packages from remote systems quickly.",
    url="",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "zstandard",
    ],
    tests_require=[
        "pytest",
    ],
    test_suite="pytest",
    entry_points={
        'console_scripts': ['DecompressServer=fast_file_transfer.decompress_server:main',
                            'CompressClient=fast_file_transfer.compress_client:main', ]
    },
)
