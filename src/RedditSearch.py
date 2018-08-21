# Contains the url for pushshift.io (Reddit db)
# Allows us to ignore the limitation of 500 entries at a time by performing multiple consecutive queries
# TODO: more than 500 entries at a time
# TODO: fill out all parameters we might want to use
# TODO: option to print output to CSV file for later use
import json
import requests


class RedditSearch:
    request = 'https://api.pushshift.io/reddit/search/submission/?'

    def __init__(self, author=None, subreddit=None, sort=None):
        count = 0

        if author is not None:
            self.request += 'author=' + author
            count += 1

        if subreddit is not None:
            if count > 0:
                self.request += '&'
            self.request += 'subreddit=' + subreddit
            count += 1

        if sort is not None:
            if count > 0:
                self.request += '&'
            self.request += 'sort=' + sort
            count += 1
    
    def results(self):
        print(self.request)
        temp = requests.get(self.request).content.decode("utf-8")
        return json.loads(temp)['data']
