from app import app
from app import camera
from flask import Response, request, stream_with_context
#import gevent
import requests
import picamera
import time
import io
import base64
import argparse

@app.route("/")
def stream():
    @stream_with_context
    def generator():
        while True:
            time.sleep(app.config['PERIOD']/1000)
            img = io.BytesIO()
	        camera.capture(img,'jpeg')
	        img_encoded = str(base64.b64encode(img.getvalue()),encoding='utf-8') #encode bytes data
	        yield "data:{value}\n\n".format(value=img_encoded)

    return Response(
        generator(),
        mimetype='text/event-stream',
    )

