from flask import Flask
import picamera
import time
from config.settings import BaseConfig

app = Flask(__name__)
app.config.from_object('BaseConfig')

print(app.config.keys())

camera = picamera.PiCamera()
camera.resolution = (app.config['X_RES'],app.config['Y_RES'])
camera.start_preview()
print("warming up camera")
time.sleep(2)

from app import views
