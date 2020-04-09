# Guide

## Requirements
To set up a development environment, first create a new virtual environment. Make sure you are running Python 3.6 and higher. 

## Cloning and installing
Then you can clone the project like so:
```
git clone https://github.com/teotsi/kotidostories.git
```
Then, you will need to install the required packages and run the setup:
```
cd kotidostories
pip install -Ur requirements.txt
pip install -e .
```

## Environment variables
Kotidostories uses a few environment variables too. If you are planning on testing the password reset endpoints, as well as save user pictures in the correct folders, you will need to set the following variables:
  * `EMAIL_FOR_FLASK` : the email address that will respond to reset requests.
  * `EMAIL_PASS`: the password for the email address above.
  * `PIC_FLASK`: this will be the project folder **relative** to your current working directory.

## Testing

We use [pytest](https://docs.pytest.org/en/latest/) for now. You can run it after the setup using the following commands:

```
pytest -s  # normal tests
pytests -s --cov=kotidostories # tests plus coverage report
```

