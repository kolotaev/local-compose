import requests
import threading
import time
import random


def run(port):
    for _ in range(1000):
        requests.get(f'http://localhost:%d/%f' % (port, random.random()))
        time.sleep(random.random())


t1 = threading.Thread(target=run, args=(9010, ))
t2 = threading.Thread(target=run, args=(9020, ))


t1.start()
t2.start()
