from flask import Flask
import picamera
import time

app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

#print(app.config.keys())

#camera = picamera.PiCamera()
#camera.resolution = (int(app.config['X_RES']),int(app.config['Y_RES']))
#camera.start_preview()
#print("warming up camera")
#time.sleep(2)

from app import views
