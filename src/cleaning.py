import re


def remove_urls(string):
    return re.sub(r'http\S+', '', string)


def remove_usernames(string):
    return re.sub(r'/u/[A-Za-z0-9_-]+', '', string)
