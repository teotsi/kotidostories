# kotidostories

[![Build Status](https://travis-ci.com/teotsi/kotidostories.svg?token=fryzzCEs33gMM5e386ed&branch=master)](https://travis-ci.com/teotsi/kotidostories)

Flask-based online stories API. WIP. Backend of a project developed for INF183 course(Information Systems Application Development), at Athens University of Economics and Business.

Designed to communicate with a Nuxt.js frontend but it should work with any framework that supports HTTP-only cookies.
Implemented features:
 * User Authentication using HTTP-Only Cookie. This allows users to register, login, logout, and perform tasks that require authentication(such as posting stories and interacting with others.)
 * Upload post, edit post, delete post
 * Get user by username
 * Comment on post
 * Reset password via email (Using a token that expires after 30 minutes)
 
### Setting up dev environment

Simply create a new virtual enviroment (Python 3.6-3.7) and then run the following commands:

```pip install -U pip
pip install -Ur requirements.txt
pip install -e .
```

After that, just run `python -m run` for now.

To enable password reset via email, set Environment Variables `EMAIL_FOR_FLASK` and `EMAIL_PASS` for your OS. They are not included in the configuration for obvious reasons.


To skip Travis/CI tests, just add [ci skip] at the end of your commit message.
