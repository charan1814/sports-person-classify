from flask import Flask,request,jsonify
import util
from flask_cors import CORS 

app = Flask(__name__)
CORS(app,resources={
    r"/*":{"origins":"*"}
})

@app.route("/classify_image",methods=['POST'])
def classify_image():
    image=request.json.get("image_data")

    response=jsonify(util.classify_image(image))
    
    response.headers.add('Access-Control-Allow-Origin','*')
    
    return response
if  __name__  == "__main__":
     print("python flask server is running")
     util.load_saved_artifacts()
     app.run(debug=True,port=5001)