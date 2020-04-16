from flask import Flask
import picamera
import time

app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('settings.py',silent=True)

camera = picamera.PiCamera()
camera.resolution = (app.config['XRES'],app.config['YRES'])
camera.start_preview()
print("warming up camera")
time.sleep(2)

from app import views