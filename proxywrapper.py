from typing import List

import requests
import json

fetch_url = 'https://gimmeproxy.com/api/getProxy?get=true&maxCheckPeriod=3600'

def fetch_gimme_proxy():
    r = requests.get(fetch_url, timeout = 2)
    try:
        r_content = json.loads(r.content.decode())
        proxy_url= f'http://{r_content["ip"]}:{r_content["port"]}'
        return proxy_url
    except Exception as e:
        print(f'Failed to get a proxy this time. {r.content}')
        return None


def get_proxies_from_file(filename : str) -> List[str]:
    endline = '\n'
    with open(filename) as file:
        lines = list(dict.fromkeys(file.readlines()))
        proxies = [f'http://{address.replace(endline, "")}' for address in lines]
    return proxies
