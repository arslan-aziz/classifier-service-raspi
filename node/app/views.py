from app import app
from app import camera
from flask import Response, request, stream_with_context, render_template
#import gevent
import requests
import time
import io
import base64
import argparse
from app.camera.Camera import Camera


@app.route('/')
def index():
    return render_template("index.html")


def genFeed(cam):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n' + \
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream')
def stream():
    return Response(genFeed(Camera()),
                    mimetype = 'multipart/x-mixed-replace; boundary=frame')

# @app.route("/stream")
# def stream():
#     def generator():
#         while True:
#             time.sleep(int(app.config['PERIOD'])/1000)
#             img = io.BytesIO()
#             camera.capture(img,'jpeg')
#             img_encoded = str(base64.b64encode(img.getvalue()),encoding='utf-8') #encode bytes data
#             print("sending image")
#             yield "data:{value}\n\n".format(value=img_encoded)

    # return Response(
    #     generator(),
    #     mimetype='text/event-stream',
    # )

