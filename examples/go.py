import requests
import threading
import time
import random


def run(port):
    while True:
        rand = random.random()
        requests.get(f'http://localhost:%d/%f' % (port, rand))
        time.sleep(rand)


t1 = threading.Thread(target=run, args=(9010, ))
t2 = threading.Thread(target=run, args=(9020, ))


t1.start()
t2.start()
