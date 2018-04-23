from setuptools import setup, find_packages

version = '0.1'
setup(
    name="invindex",
    version=version,
    description="A high performance pure python module that helps in"
                "computing the no of documents a word is present and "
                "no of documents where two words cooccur in a set of documents"
    keywords='invindex',
    author='Deep Compute, LLC',
    author_email="contact@deepcompute.com",
    url="https://github.com/deep-compute/invindex",
    download_url="https://github.com/deep-compute/invindex/tarball/%s" % version,
    license='MIT License',
    install_requires=[
        'numpy==1.11.0',
        'tables==3.4.2',
        'basescript==0.1.15',
        'deeputil==0.1.2',
        'funcserver==0.2.17',
    ],
    package_dir={'invindex': 'invindex'},
    packages=find_packages('.'),#FIXME: doubt
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2.7.12",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    test_suite='test.suitefn',
    entry_points={
        "console_scripts": [
            "invindex = invindex:main",
        ]
    }

)
