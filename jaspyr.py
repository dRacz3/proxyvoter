import requests
endline = '\n'

with open('proxies.txt') as file:
    proxies = [ f'http://{address.replace(endline, "")}' for address in file.readlines()]
print(f'Loaded : {proxies}')

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

        except Exception as e:
            print(f"Failed to vote from {p}, error : {e}")
    vote()

print('Finsihed voting for jasper!')