import http.client
import redis
import argparse
from camera.Camera import Camera
import cfg
import threading
import logging
import atexit

#initialization
#get message broker ip from args

parser = argparse.ArgumentParser(description = 'Server pi images')
parser.add_argument('web_ip', type = str, nargs = 1,
                    help = 'ip addr of web server')
parser.add_argument('redis_ip', type = str, nargs = 1,
                    help = 'ip addr of redis pubsub')

args = parser.parse_args()
web_ip = args.web_ip[0]
redis_ip = args.redis_ip[0]

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
        logging.debug(r1.status)
        data = r1.read()
        logging.debug(data)

        #based on response, set cfg var

"""
"""
def post_image(redis,cam):
    while True:
        if cfg.status == True:
            #post image
            pass

"""
"""
def cleanup():
    #perform cleanup operations
    pass

#register cleanup function
atexit.register(cleanup)

#connect to web server
web_conn = http.client.HTTPConnection(web_ip)

#connect to redis pubsub

#create camera object
cam = Camera()

#initialize threads
status_thread = threading.Thread(target = check_status, args = (web_conn,))
post_thread = threading.Thread(target = post_image, args = (redis_conn, cam))

#start threads
status_thread.start()


