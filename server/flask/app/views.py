from app import app
from app import redis_store
from flask import render_template, request, Response, stream_with_context
#from app import sse
import io
import os
import base64
import json

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
    img_bytes = base64.b64decode(request.data)
    #TODO: this label will be assigned in the classifier service
    path = os.path.join('app','static','img','test.jpg')
    with open(path,'wb+') as f:
        f.write(img_bytes)
    publish(str(redis_store.get('image_counter')))
    redis_store.incr('image_counter')
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
