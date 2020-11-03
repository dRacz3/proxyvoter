import logging
import threading

import requests

from proxywrapper import get_proxies_from_file

logger = logging.getLogger('VOTER')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s -%(threadName)s | %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def vote_link(nid):
    return f'http://ebadta.hu/verseny/votegw.php?nid={nid}'


def start_mass_vote(nid, proxies):
    request_threads = []
    success_count = 0
    for p in proxies:

        if p is None:
            continue
        proxy = {
            "http": p,
        }

        def vote():
            nonlocal success_count
            try:
                logger.info(f"Voting from {p} started")
                r = requests.get(vote_link(nid), proxies=proxy, timeout=90)
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

    [t.join() for t in request_threads]
    logger.info(f'Finished, {success_count}/{len(proxies)} succeeded vote.')


if __name__ == '__main__':
    JASPER_NID = 779
    start_mass_vote(JASPER_NID, get_proxies_from_file("proxies.txt"))
