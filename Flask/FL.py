from Flask import Flask,jsonify
from Flask import request
app= Flask(__name__)
@app.route("/rishabh/sipani")
def hello_world():
    return "<p>Hello World!<p>"

@app.route("/prediction",methods=["POST"])
def getprediction():
    data=request.get_json()
    print(data["Sepal length"])
    return jsonify({"message":"JSON data recieved","data":data}),200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)