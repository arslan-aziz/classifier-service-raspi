from app import app
from app import redis_store
from flask import render_template, request, Response, stream_with_context
#from app import sse
import io
import os
import base64
import json
import requests
import logging
from sseclient import SSEClient

#TODO: how to pass a dictionary according to SSE standard?
def publish(data):
    msg_json = json.dumps({"data":data,"type":"message"})
    return redis_store.publish('label',msg_json)

@app.route("/")
def index():
    return render_template('main.html')

@app.route("/upload_image",methods=['POST'])
def upload_image():
    print(type(request.data))
    #img_bytes = base64.b64decode(request.data)
    publish(request.data) #string of byte64 encoded image
    """
    path = os.path.join('app','static','img','test.jpg')
    with open(path,'wb+') as f:
        f.write(img_bytes)
    publish(str(redis_store.get('image_counter')))
    redis_store.incr('image_counter')
    """
    return "done"       

@app.route("/start_stream",methods=['GET'])
def start_stream():
    
    URL = "http://192.168.1.23:8080/"
    session = requests.Session()
    messages = session.get(URL,stream=True)
    app.logger.debug("receiving stream")

    for msg in messages.iter_lines():
        publish(msg)

    #messages = SSEClient(URL)
    # for msg in messages:
    #     if msg.event=='message':
    #         #app.logger.debug(str(type(msg.data)))
    #         #app.logger.debug(msg.data)
    #         publish(msg.data)
    #r = requests.get("http://192.168.1.23:8080/",stream=True)
    #for line in r.iter_content():
        #print("original" + str(type(line)),flush=True)
        #print("")
        #print("decoded" + str(type(line.decode())),flush=True)
        #if line:
            #publish(line)
            #print(line.content)
            #app.logger.debug(str(type(line)))    
            #publish()
            #publish(json.loads(line.decode('utf-8')))
    return "done"

@app.route("/stream")
def stream():
    @stream_with_context
    def generator():
        pubsub = redis_store.pubsub()
        pubsub.subscribe('label')
        for msg in pubsub.listen():
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
