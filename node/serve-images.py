import http.client
from redis import StrictRedis
import argparse
from camera.Camera import Camera
import cfg
import threading
import logging
import atexit
import time
import base64
from PIL import Image
import io

#initialization
#get message broker ip from args

parser = argparse.ArgumentParser(description = 'Server pi images')
parser.add_argument('web_ip', type = str, nargs = 1,
                    help = 'ip addr of web server')

args = parser.parse_args()
web_ip = args.web_ip[0]

logging.basicConfig(level = logging.DEBUG)

web_conn = None
redis_conn = None
status_thread = None
post_thread = None
cam = None

"""
Check status on 
"""
def check_status(conn):
    while True:
        web_conn.request("GET","/get_status")
        r1 = conn.getresponse()
        #logging.debug(r1.status)
        data = r1.read().decode()
        #logging.debug(data)
        if data == 'False':
            cfg.status = False
        else:
            cfg.status = True

"""
Publish image to pubsub
"""
def post_image(redis,cam):

    while True:
        if cfg.status == True:
            logging.debug("decoded: Start")
            frame = cam.get_frame()
            redis_conn.publish("label", frame)
        else:
            logging.debug("decoded: Stop")

        #relinquish control of the GIL
        time.sleep(0)

"""
Clean-up operations on program exit
"""
def cleanup():
    #perform cleanup operations
    pass

#register cleanup function
atexit.register(cleanup)

#connect to web server
web_conn = http.client.HTTPConnection(web_ip)

#connect to redis pubsub
redis_conn = StrictRedis.from_url("redis://{}:6379/0".format(web_ip), decode_responses = False)

#create camera object
cam = Camera()

#initialize threads
status_thread = threading.Thread(target = check_status, args = (web_conn,))
post_thread = threading.Thread(target = post_image, args = (redis_conn, cam))

#start threads
status_thread.start()
post_thread.start()


