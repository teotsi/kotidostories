import os

from bs4 import BeautifulSoup
from flask import jsonify

from kotidostories import es
from kotidostories.models import Post
from kotidostories.utils.general_utils import serialize


def es_enabled(func):
    def wrap(*args, **kwargs):
        if os.environ.get('ES_ENABLED', default=False):
            return func()
        else:
            return {}
    return wrap


def clean_content(text):
    soup = BeautifulSoup(text, features='html.parser')
    print(text)
    return soup.get_text(separator=' ').replace('\xa0', ' ')


def get_match_query(size, text):
    return {
        "from": 0, "size": size,
        "query": {
            "match": {
                "content": text
            }
        }
    }


@es_enabled
def get_more_like_this_query(text, size=None):
    if size is None:
        size = 5
    return {  # body of MLT query
        "from": 0, "size": size,  # specifying the number of texts to be retrieved
        "query": {
            "more_like_this": {
                "fields": [
                    "title",
                    "content",
                    "user"
                ],
                "like": text,  # specifying the string to be used
                "min_term_freq": 1,
                "min_doc_freq": 1,
                "max_query_terms": 25
            }
        }
    }


@es_enabled
def index_post(post):
    body = {
        "title": post.title,
        "content": clean_content(post.content),
        "user": post.user.username
    }
    result = es.index(index="kot_front", id=post.id,
                      body=body)


@es_enabled
def get_suggestion(text=None, size=None, id=None):
    if size is None:
        size = 5
    if text is None:
        text = ''
    if id:
        post = Post.query.filter_by(id=id).first()
        text = post.content
    query = get_more_like_this_query(text, size)
    try:
        results = es.search(index="kot_front", body=query)
        print(results)
        posts = [Post.query.filter_by(id=result["_id"]).first() for result in results['hits']['hits']]
        posts = [post for post in posts if post is not None]
        return jsonify(serialize(posts))
    except:
        return {}


@es_enabled
def update_index(post):
    body = {
        "doc": {
            "title": post.title,
            "content": post.content
        }
    }
    es.update(index="kot_front", id=post.id, body=body)


@es_enabled
def delete_post_from_index(id):
    es.delete(index='kot_front', id=id, doc_type='_doc')
