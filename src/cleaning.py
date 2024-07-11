import re


def remove_urls(s):
    return re.sub(r'http\S+', '', s)


# TODO
def remove_usernames(s):
    return
