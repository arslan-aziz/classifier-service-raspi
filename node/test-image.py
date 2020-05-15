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

parser = argparse.ArgumentParser(description = 'Server pi images')
parser.add_argument('web_ip', type = str, nargs = 1,
                    help = 'ip addr of web server')

args = parser.parse_args()
web_ip = args.web_ip[0]

logging.basicConfig(level = logging.DEBUG)

redis_conn = StrictRedis.from_url("redis://{}:6379/0".format(web_ip), decode_responses = False)
cam = Camera()
frame = cam.get_frame()
redis_conn.set("image", frame)


