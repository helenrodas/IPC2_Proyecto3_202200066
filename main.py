from flask import Flask,jsonify,request
from flask_cors import CORS
import base64
from readFile import *
app= Flask(__name__)
CORS(app)
readFileHandler = readFile()

@app.route('/upload_file_sentimientos',methods=['POST'])
def upload_file_sentimientos():
    if 'file' not in request.files:
        return jsonify({
        "message": "Error! No se ha enviado archivo"
        })
    file = request.files['file']
    file_content=file.read().decode('utf-8')
    # print(file_content)
    readFileHandler.read_xml_sentimientos(file_content)
    return jsonify({
        "message": "El archivo fue cargado y leido exitosamente"
        })

@app.route('/upload_file_mensajes',methods=['POST'])
def upload_file_mensajes():
    if 'file' not in request.files:
        return jsonify({
        "message": "Error! No se ha enviado archivo"
        })
    file = request.files['file']
    file_content=file.read().decode('utf-8')
    # print(file_content)
    readFileHandler.read_xml_mensajes(file_content)
    return jsonify({
        "message": "El archivo fue cargado y leido exitosamente"
        }) 

@app.route('/hashtags',methods=['GET'])
def hashtags_by_date():
    fechainicio = request.form.get('fechainicio')
    fechafinal = request.form.get('fechafinal')

    hashtags_count = readFileHandler.hashtags_by_date(fechainicio,fechafinal)
    return jsonify(hashtags_count)

@app.route('/menciones',methods=['GET'])
def mentions_by_date():
    fechainicio = request.form.get('fechainicio')
    fechafinal = request.form.get('fechafinal')

    mentions_count = readFileHandler.mentions_by_date(fechainicio,fechafinal)
    return jsonify(mentions_count)

@app.route('/consulta_sentimientos',methods=['GET'])
def consulta_sentimientos():
    fechainicio = request.form.get('fechainicio')
    fechafinal = request.form.get('fechafinal')

    sentimientos_count = readFileHandler.sentimientos_by_date(fechainicio,fechafinal)
    return jsonify(sentimientos_count)


if __name__=="__main__":
    app.run(threaded=True,port=5000,debug=True)