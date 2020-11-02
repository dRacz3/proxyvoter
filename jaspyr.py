import requests
import threading
endline = '\n'

with open('proxies.txt') as file:
    proxies = [ f'http://{address.replace(endline, "")}' for address in file.readlines()]
print(f'Loaded : {proxies}')

sucess_list = []

request_threads = []
for p in proxies:
    print(f"Voting from {p}")
    proxy = {
        "http": p,
    }

    iwoteforjasperlink = 'http://ebadta.hu/verseny/votegw.php?nid=779'
    def vote():
        try:
            r = requests.get(iwoteforjasperlink, proxies=proxy, timeout=15)

            print(r.content.decode())
            print(r)
            sucess_list.append(p)
        except Exception as e:
            print(f"Failed to vote from {p}, error : {e}")
    t = threading.Thread(target=vote)
    request_threads.append(t)
    t.start()


[t.join() for t in request_threads]
print('Finsihed voting for jasper!')
print(sucess_list)