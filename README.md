# kotidostories

[![Build Status](https://travis-ci.com/teotsi/kotidostories.svg?token=fryzzCEs33gMM5e386ed&branch=master)](https://travis-ci.com/teotsi/kotidostories)

Flask-based online stories REST (for the most part) API. Work in progress. Backend of a project developed for INF183 course(Information Systems Application Development), at Athens University of Economics and Business.



Designed to communicate with a Nuxt.js frontend but it should work with any framework that supports HTTP-only cookies.
Implemented features:
 * User Authentication using JWT. This allows users to register, login, logout, and perform tasks that require authentication(such as posting stories and interacting with others.)
 * Get post,Upload post, edit post, delete post. Also apply query parameters to filter posts
 * Get user, register user, update user 
 * Comment on post, edit comment, delete comment
 * Add and update user/post image
 * Add reaction, edit reaction, delete reaction
 * Follow other users
 * Reset password via email (Using a token that expires after 30 minutes)
 
### Setting up dev environment

Simply create a new virtual enviroment (Python 3.6+) and then run the following commands:

```pip install -U pip
pip install -Ur requirements.txt
pip install -e .
```

After that, just run `python -m run` for now.

To enable password reset via email, set Environment Variables `EMAIL_FOR_FLASK` and `EMAIL_PASS` for your OS. They are not included in the configuration for obvious reasons.
Also, you wil need to set `PIC_FLASK` to the project subfolder in your current working directory. For example, if your file tree looks something
like `projects/kotidostories/...`, and you are working on `projects`, then `PIC_FLASK` should be set to `kotidostories`. It is not necessary,
but otherwise pictures will most likely not be served as intended.


There are endpoints like `suggest/` that make use of an Elasticsearch cluster. To take advantage of this feature, you will need to set another environment variable called `ES_HOST`. Otherwise the host will be `localhost`.


To skip Travis/CI tests, just add `[ci skip]` at the end of your commit message.

You can run tests using `pytest -s --cov=kotidostories`. It will also produce a basic coverage report db.

There is a test database to check the app. You can remove it by deleting it. When you start the app an empty database will be created automatically.
