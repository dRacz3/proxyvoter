import logging
import threading

import requests
import time
import pandas as pd
import random

from proxywrapper import get_proxies_from_file

def vote_link(nid):
    return f'http://ebadta.hu/verseny/votegw.php?nid={nid}'

def get_doggo_page(nid):
    return f'http://ebadta.hu/verseny/versenyzo.php?nid={nid}'

def start_mass_vote(nid, proxies, logger = None, timeout = 60):
    logger.info(f'start_mass_vote called with nid: {nid}')
    request_threads = []
    success_count = 0
    success_map = {}
    for p in proxies:
        if p is None:
            continue
        proxy = {
            "http": p,
        }


        def vote():
            nonlocal success_count
            nonlocal logger

            try:
                try:
                    _ = requests.get(get_doggo_page(nid), proxies=proxy, timeout=5)
                except Exception as e:
                    logger.info(f'Failed to fetch site, but will try to vote anyway. {e}')
                time.sleep(random.randint(1,3000) / 1000)
                r = requests.get(vote_link(nid), proxies=proxy, timeout=timeout)
                if r.status_code == 200:
                    logger.info(f'{p} seems to be reliable.')
                if '1' == r.content.decode():
                        logger.info('Vote succeeded!')
                        success_count = success_count + 1
                else:
                    logger.warning(f'Voting failed with : {r.content.decode()}')

            except Exception as e:
                logger.info(f"Failed to vote from {p}, error : {e}")

        t = threading.Thread(target=vote)
        request_threads.append(t)
        t.start()

    while len(request_threads) != len(proxies):
        print('Waiting until all threads start..')
        time.sleep(0.5)
    [t.join() for t in request_threads]
    result = pd.DataFrame.from_records(success_map)
    result.to_json(f'voting-result-{nid}.json')
    logger.info(f'Finished, {success_count}/{len(proxies)} succeeded vote.')


if __name__ == '__main__':

    logger = logging.getLogger('VOTER')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    from nids import JASPER_NID, COLOMBUS
    proxy_list = get_proxies_from_file('proxies.txt')
    logger.info(f'Loaded {len(proxy_list)} unique proxies from file')
    start_mass_vote(JASPER_NID, proxy_list, timeout=180, logger=logger)
