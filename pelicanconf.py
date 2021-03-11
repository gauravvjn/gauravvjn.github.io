#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Gaurav Jain'
SITENAME = 'GAURAV JAIN'

PATH = 'content'
OUTPUT_PATH = 'docs'

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
# FEED_RSS = 'feed/'
# FEED_RSS_URL = '/feed'
# RSS_FEED_SUMMARY_ONLY = True
# TAG_FEED_RSS = 'tag/{slug}/feed/'
# TAG_FEED_RSS_URL = 'tag/{slug}/feed/'

DIRECT_TEMPLATES = ['index', 'authors', 'categories', 'tags']

STATIC_PATHS = [
    'images',
    'extras/robots.txt',
]

EXTRA_PATH_METADATA = {
    'extras/robots.txt': {'path': 'robots.txt'},
}

ARTICLE_PATHS = ['articles']
ARTICLE_SAVE_AS = '{slug}.html'
ARTICLE_URL = '{slug}/'

PAGE_PATHS = ['pages']
PAGE_SAVE_AS = '{slug}.html'
PAGE_URL = '{slug}/'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}.html'

AUTHOR_URL = 'author/{slug}/'
AUTHOR_SAVE_AS = 'author/{slug}.html'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}.html'

TAGS_URL = 'tags/'
TAGS_SAVE_AS = 'tags/index.html'

PAGINATION_PATTERNS = [
    (1, '{url}', '{save_as}'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}.html'),
]

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = "pelican-themes/tuxlite_tbs"

# DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False

MENUITEMS = [
    ('About Me', '/about-me/'),
    ('Contact Me', '/contact-me/'),
    ('Python Jobs', '/python-jobs/'),
]

# Blogroll
LINKS = (
    # ('Learn Python in 10 minutes', 'https://www.gauravvjn.com/learn-python-in-10-minutes/'),
    ('Security in the Django App', 'https://www.gauravvjn.com/security-in-the-django-application/'),
    # ('Building a Simple Blockchain in Python', 'https://www.gauravvjn.com/building-a-simple-blockchain-in-python/'),
)

# Social widget
SOCIAL = (
    ('Facebook', 'https://www.facebook.com/gauravvjntech'),
    ('Linkedin', 'https://www.linkedin.com/in/gauravvjn'),
    ('Instagram', 'https://www.instagram.com/gauravvjn'),
    ('Twitter', 'https://www.twitter.com/gauravvjn'),
    ('Github', 'https://www.github.com/gauravvjn'),
)

POPULAR_TAGS = [
    'beginner',
    'django',
    'machine-learning',
    'datastructure',
    'security',
    'blockchain',
]

# PLUGIN_PATHS = ['pelican-plugins']

PLUGINS = ["sitemap"]
# PLUGINS = ['tipue_search.tipue_search']
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.5,
        "indexes": 0.5,
        "pages": 0.5
    },
    "changefreqs": {
        "articles": "daily",
        "indexes": "daily",
        "pages": "daily"
    }
}


from functools import partial


JINJA_FILTERS = {
    'sort_by_article_count': partial(sorted, key=lambda tags: len(tags[1]), reverse=True),
    'get_first_n_words': lambda content, n: ' '.join(content.split()[:n]),
}

from datetime import date
CURRENT_YEAR = date.today().year

LOAD_CONTENT_CACHE = False

import logging
LOG_FILTER = [(logging.WARN, 'Empty alt attribute for image %s in %s')]

# --------------------------- END common settings ---------------------------------

# Development conf
SITEURL = 'http://127.0.0.1:8000'
DEBUG = True
DEFAULT_PAGINATION = 3
