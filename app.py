import json
import logging
import threading
import time

from flask import Flask

from InVariableLogger import FIFOIO
from nids import COLOMBUS
from proxywrapper import get_proxies_from_file

app = Flask(__name__)

### Create the logger
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

### Setup the console handler with a FIFOIO object
log_capture_string = FIFOIO(1024 ** 2)
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.DEBUG)

### Optionally add a formatter
formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] %(levelname)s - %(message)s </br>')
ch.setFormatter(formatter)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] %(levelname)s - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)

### Add the console handler to the logger
logger.addHandler(ch)

from rq import Queue
from worker import conn

q = Queue(connection=conn)

from jaspyr import start_mass_vote


@app.route('/')
def hello_world():
    return '''Hello stranger, vanna vote for some doggos? Checkout /vote/nid !'''


@app.route('/vote/<nid>')
def vote(nid):
    proxy_list = get_proxies_from_file('proxies.txt')
    result = q.enqueue(start_mass_vote,
                       kwargs={
                           "nid": nid, "proxies": proxy_list, "timeout": 15}
                       )
    return f'{result}, {log_capture_string.getvalue()}'


@app.route('/logs')
def logs():
    return log_capture_string.getvalue()


if __name__ == '__main__':
    from rq import Queue
    from worker import conn

    q = Queue(connection=conn)

    app.run(threaded=True, port=5000)
