from app import app
from app import redis_state
from app import redis_queue
from flask import render_template, request, Response, stream_with_context
import io
import os
import json
import requests
import logging
import time

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

# @app.route("/upload_image",methods=['POST'])
# def upload_image():
#     print(type(request.data))
#     #img_bytes = base64.b64decode(request.data)
#     publish(request.data) #string of byte64 encoded image
#     """
#     path = os.path.join('app','static','img','test.jpg')
#     with open(path,'wb+') as f:
#         f.write(img_bytes)
#     publish(str(redis_store.get('image_counter')))
#     redis_store.incr('image_counter')
#     """
#     return "done"       

@app.route("/get_status", methods = ['GET'])
def check_state():
    if time.time() - float(redis_state.get('last_stream')) > 10:
        return "stop"
    else:
        return "start"

@app.route("/stream")
def stream():
    @stream_with_context
    def generator():
        #initialize time on connection
        redis_state.set('last_stream',str(time.time()))
        pubsub = redis_store.pubsub()
        pubsub.subscribe('label')
        for msg in pubsub.listen():
            redis_state.set('last_stream',str(time.time()))
            msg_load = msg
            print(msg_load)
            #msg_load = json.loads(msg)
            #ignore subscribe messages
            if(msg_load['type']) == "message":
                yield "data:{value}\n\n".format(value=msg_load['data'])

    return Response(
        generator(),
        mimetype='text/event-stream',
    )
