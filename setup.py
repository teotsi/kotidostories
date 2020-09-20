import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kotidostories",
    version=os.environ.get('TRAVIS_TAG', 'dev'),
    author="TXC",
    author_email="teotsi@gmail.com",
    description="stories for kotidis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teotsi/kotidostories",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=['Flask==1.1.2',
                      'Flask-SQLAlchemy==2.4.1',
                      ],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
)
