from flask import Flask,jsonify,request
from flask_cors import CORS
import base64
from readFile import *
app= Flask(__name__)
CORS(app)
readFileHandler = readFile()

@app.route('/upload_file',methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({
        "message": "Error! No se ha enviado archivo"
        })
    file = request.files['file']
    file_content=file.read().decode('utf-8')
    # print(file_content)
    readFileHandler.read_xml(file_content)
    return jsonify({
        "message": "El archivo fue cargado y leido exitosamente"
        }) 


if __name__=="__main__":
    app.run(threaded=True,port=5000,debug=True)