import re


def remove_urls(string):
    return re.sub(r'http\S+', '', string)


# TODO
def remove_usernames(string):
    return
