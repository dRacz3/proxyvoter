import requests


import os


def get(URL):
    API_KEY = os.getenv('SCRAPESTACK_API_KEY')
    if API_KEY is None:
        print('No API KEY PROVIDED IN ENV, PLEASE SET `SCRAPESTACK_API_KEY` to your API token')
    scrapestack_request_url = f'http://api.scrapestack.com/scrape?access_key={API_KEY}&url={URL}'
    r = requests.get(scrapestack_request_url)
    print(r)
    print(r.content)
    return r



if __name__ == '__main__':
    from nids import JASPER_NID
    from jaspyr import vote_link

    for i in range(999):
        print(get(vote_link(JASPER_NID)))