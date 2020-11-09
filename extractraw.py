import re


ip_port_regex = "((\d{1,3}.){3}\d{1,3}:\d{2,15})"
pattern = re.compile(ip_port_regex)

with open('scratch.txt') as f:
    data = f.read()
ip_list = pattern.findall(data)

for ip in ip_list:
    print(ip[0])