from flask import Flask, jsonify,request
app = Flask(__name__)

"""
The handler main is called at the default url, returns HTTP content (.html)
"""

@app.route("/hello") #this route is a URI endpoint
def helloHTML():
    return "Hello world!"

"""
The handler hello is called at the suburl /blah returns a json object
"""
@app.route("/helloJSON") #this route is a URI endpoint
def helloJSON():
    return jsonify({"about":"Hello World!"})

"""
The handler index accepts either GET or POST requests.
POST request: curl -H "Content-Type: application/json" -X POST -d '<JSON>' <URI>
"""
@app.route("/",methods=['GET','POST'])
def index():
    if(request.method == 'POST'):
        some_json = request.get_json()
        return jsonify(some_json),201 #returns response code 201
    else:
        return jsonify({"about":"Hello World!"})

"""
The handler get_mutliply10 accepts a GET request with a variable endpoint, and then operates on that variable
"""
@app.route('/multi/<int:num>',methods=['GET'])
def get_mutliply10(num):
    return jsonify({"result":num*10})

if __name__ == '__main__':
    app.run(debug=True)