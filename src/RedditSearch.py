# Contains the url for pushshift.io (Reddit db)
# Allows us to ignore the limitation of 500 entries at a time by performing multiple consecutive queries
# TODO: more than 500 entries at a time
# TODO: fill out all parameters we might want to use
# TODO: option to print output to CSV file for later use
import json
import requests
from datetime import datetime


def get_time(n):
    return datetime.fromtimestamp(n)


class RedditSearch:
    request = 'https://api.pushshift.io/reddit/search/submission/?'

    def query(self, author=None, subreddit=None, sort=None, size=500, before_id=None, after_id=None, before=None, after=None):
        count = 0
        req = self.request

        if author is not None:
            req += 'author=' + author
            count += 1

        if subreddit is not None:
            if count > 0:
                req += '&'
            req += 'subreddit=' + subreddit
            count += 1

        # asc or desc
        if sort is not None:
            if count > 0:
                req += '&'
            req += 'sort=' + sort
            count += 1

        # number of posts
        if count > 0:
            req += '&'
        req += 'size=' + str(size)
        count += 1
        #else:
        #    print('ERROR: need more information for RedditSearch')
        #    exit(-1)

        # before_id and after_id don't do nuffin' >:(
        if before_id is not None:
            req += '&'
            req += 'before_id=' + before_id
            count += 1

        if after_id is not None:
            req += '&'
            req += 'after_id=' + after_id
            count += 1

        if before is not None:
            req += '&'
            req += 'before=' + str(before)
            count += 1

        if after is not None:
            req += '&'
            req += 'after=' + str(after)
            count += 1

        return req

    def results(self, total_size=500, author=None, subreddit=None, sort=None, before_id=None, after_id=None, before=None, after=None):
        print(self.request)
        temp = requests.get(self.request).content.decode("utf-8")
        f = open("reddit.csv", "w")
        f.write('')
        f.close()
        f = open("reddit.csv", "a")
        search = json.loads(temp)['data']
        last_utc = -1

        num_found = 0
        while num_found < total_size:
            size = 500
            if size > total_size - num_found:
                size = total_size - num_found

            if last_utc == -1:
                req = self.query(size=size, author=author, subreddit=subreddit, sort=sort, before_id=before_id,
                                 after_id=after_id, before=before, after=after)
            else:
                req = self.query(size=size, author=author, subreddit=subreddit, sort=sort, before_id=before_id,
                                 after_id=after_id, before=last_utc, after=after)

            search = json.loads(requests.get(req).content.decode("utf-8"))['data']
            csv = ""
            for j in range(0, len(search)):

                entry = search[j]
                title_clean = entry['title'].encode('unicode_escape').decode("utf-8")
                #title_clean = title_clean[2:len(title_clean)-1]
                csv = str(entry['created_utc']) + ',' + entry['subreddit'] + ',' + entry['author'] + ',' + title_clean + '\n'
                #print(csv)
                f.write(csv)
                if j == len(search)-1:
                    last_utc = entry['created_utc']

            num_found += size

            #f.write(csv)
