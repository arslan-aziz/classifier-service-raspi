from app import app
from app import redis_state
from app import redis_pubsub
from flask import render_template, request, Response, stream_with_context
import io
import os
import json
import requests
import time
import base64
from PIL import Image

#TODO: how to pass a dictionary according to SSE standard?
def publish(data):
    msg_json = json.dumps({"data":data,"type":"message"})
    return redis_store.publish('label',msg_json)

"""
Route index:
HTML page displaying updated video stream using client-side JS SSE.
"""
@app.route("/")
def index():
    return render_template('test.html')

@app.route("/get_an_image", methods = ['GET'])
def get_an_image():
    msg = redis_pubsub.get("image")
    img = Image.open(io.BytesIO(msg))
    img.save(app.root_path  + "/static/img/test.jpg")
    return render_template("image.html")

@app.route("/get_status", methods = ['GET'])
def check_state():
    if time.time() - float(redis_state.get('last_stream')) > 10:
        return "False"
    else:
        return "True"

@app.route("/stream")
def stream():
    @stream_with_context
    def generator():
        #initialize time on connection
        redis_state.set('last_stream',str(time.time()))
        pubsub = redis_pubsub.pubsub()
        pubsub.subscribe('label')
        for msg in pubsub.listen():
            redis_state.set('last_stream',str(time.time()))
            #ignore subscribe messages
            if(msg['type']) == "message":
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + msg['data'] + b'\r\n'
                )

                # app.logger.debug(str(type(msg['data'])))
                # img_encoded = base64.b64encode(msg['data']).decode('ascii')
                # app.logger.debug(str(type(img_encoded)))
                # yield "data:{value}\n\n".format(value = img_encoded)

    # return Response(
    #     generator(),
    #     mimetype='text/event-stream',
    # )

    return Response(generator(),
                    mimetype = 'multipart/x-mixed-replace; boundary=frame')
