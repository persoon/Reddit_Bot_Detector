import requests
import json
from datetime import datetime

query = 'https://api.pushshift.io/reddit/search/submission/?subreddit=league_of_legends'

page = requests.get('https://api.pushshift.io/reddit/search/submission/?author=persoon&subreddit=hearthstone&sort=asc')

data = json.loads(page.content.decode("utf-8"))['data']


def to_string(post):
    ret = ''

    ret += get_time(post['created_utc']).strftime("%A, %B %d, %Y %I:%M:%S")
    return ret


# returns datetime object from value
def get_time(n):
    return datetime.fromtimestamp(n)

class Query:

    # search_terms --- list of search terms as strings
    request = 'https://api.pushshift.io/reddit/search/submission/?'

    def __init__(self, author=None, subreddit=None, sort=None):
        # author=persoon&subreddit=hearthstone&sort=asc
        if author is not None:
            self.request += 'author=' + author

        if subreddit is not None:
            self.request += '&subreddit=' + subreddit

        if sort is not None:
            self.request += '&sort=' + sort

    def results(self):
        print(self.request)
        temp = requests.get(self.request).content.decode("utf-8")
        #print(temp)
        #temp2 = json.loads(temp)
        #print(temp2)
        return json.loads(temp)['data']


query = Query(author='persoon', subreddit='Hearthstone', sort='asc')
print(to_string(query.results()[0]))
