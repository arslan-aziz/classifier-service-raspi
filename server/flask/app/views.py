from app import app
from app import redis_store
from flask import render_template, request, Response
import io
import os
import base64

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
    redis_store.publish('label',str(redis_store.get('image_counter')))
    redis_store.incr('image_counter')
    return "done"

# @app.route("/image_count",methods=['GET'])
# def get_count():
#     return """
#     <!doctype html>
#     <TITLE> {c} </TITLE>
#     <BODY> {c} </BODY>
#     """.format(c=redis_store.get('image_counter'))


@app.route("/stream")
def stream():
    def event_stream():
        pubsub = redis_store.pubsub()
        pubsub.subscribe('label')
        for message in pubsub.listen():
            print('message received')
            yield 'data: {c}\n\n'.format(c=message['data'])
    return Response(event_stream(),mimetype="text/event-stream")





