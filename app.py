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
log_capture_string = FIFOIO(1024**2)
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

from jaspyr import start_mass_vote

class VotingExecutor:
    voting_queue = []

    def __init__(self):
        pass

    def push(self, job):
        logger.info(f'Job added: {job}')
        self.voting_queue.append(job)

    def loop(self):
        while True:
            logger.info("Checking queue..")
            if len(self.voting_queue) > 0:
                task = self.voting_queue.pop()
                logger.info(f"found new task, running it! {task}")
                task()
                logger.info("finished task")
            else:
                time.sleep(5)


VotingExecutorDAO = VotingExecutor()

@app.route('/')
def hello_world():
    return 'Hello stranger, vanna vote for some doggos?'


@app.route('/vote/<nid>')
def vote(nid):
    proxy_list = get_proxies_from_file('proxies.txt')[0:2]
    start_mass_vote(nid, proxy_list, logger=logger, timeout=20)
    return log_capture_string.getvalue()

@app.route('/logs')
def logs():
    return log_capture_string.getvalue()

@app.route('/queued_jobs')
def get_jobs():
    return str(VotingExecutorDAO.voting_queue)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    threading.Thread(target=VotingExecutorDAO.loop).start()
    app.run(threaded=True, port=5000)