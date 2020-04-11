from app import app
from flask import render_template, request
import io
import os
import base64

@app.route("/")
def index():
    return render_template('main.html')
    #return "Hello Flask!"

# @app.route("/pitest",methods=['GET','POST'])
# def test_pi():
#     if(request.method == 'GET'):
#         return data
#     else:
#         data = request.data.decode('utf-8')
#     print(data)
    
@app.route("/show_image",methods=['GET'])
def show_image():
    return render_template('main.html')

@app.route("/upload_image",methods=['POST'])
def upload_image():
    print(type(request.data))
    img_bytes = base64.b64decode(request.data)
    #buffer = io.BytesIO(request.data)
    path = os.path.join('app','static','img','test.jpg')
    with open(path,'wb+') as f:
        #f.write(buffer.getvalue())
        f.write(img_bytes)
    return "done"
    #return render_template('main.html')
    #img = Image.open(io.BytesIO(request.data))

