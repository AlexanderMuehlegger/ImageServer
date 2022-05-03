from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from flask import Flask, request, render_template, jsonify
from flask_restful import Api, Resource
from msrest.authentication import CognitiveServicesCredentials
from sqlalchemy import Column, Integer, Text, DateTime, create_engine, LargeBinary
import paho.mqtt.client as mqtt
import time

from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

import ids, uuid, requests

allowedLanguages = [
    'en', 'de', 'it'
]

headers = {
    'Ocp-Apim-Subscription-Key': ids.sub_key_transl,
    'Ocp-Apim-Subscription-Region': ids.transl_location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

translation_url = ids.endpoint_translation + '/translate'

app = Flask(__name__)
api = Api(app)

Base = declarative_base()
metadata = Base.metadata

engine = create_engine(r'sqlite:///.\images.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)

client = mqtt.Client('RaspberryPi')
client.username_pw_set(ids.username, ids.pw)
client.connect(ids.ip, port=ids.port)

@app.route("/")
def index():
    return render_template("index.html")

class Image(Base):
    __tablename__ = 'Image'

    ID = Column(Integer, primary_key=True)
    Titel = Column(Text)
    Description = Column(Text)
    Device = Column(Text)
    Date = Column(Text)
    Imagename = Column(Text)
    Upload_folder = Column(Text)
    ReadText = Column(Text)
    Translation = Column(Text)

    def getJson(self):
        return {
            'ID': str(self.ID),
            'Titel': self.Titel,
            'Description': self.Description,
            'Device': self.Device,
            'Date': self.Date,
            'Imagename': self.Imagename,
            'UPLOAD_FOLDER' : self.Upload_folder,
            'Text' : self.ReadText,
            'Translation' : self.Translation
        }

def notify_users():
    client.publish("foto/taken/dev0", "A new image has been uploaded!!!!")

def translate(into, text):
    if len(text) == 0:
        return {'Response' : '500: No Text provided!'}

    if into in allowedLanguages:
        params = {
            'api-version' : '3.0',
            'to' : str(into)
        }
    body = [{
        'text' : str(text)
    }]
    if params is not None:
        result = requests.post(translation_url, params=params, headers=headers, json=body)
        return result.json()

def get_image_text(image):
    text = []
    computervision = ComputerVisionClient(ids.endpoint_vision, CognitiveServicesCredentials(ids.sub_key_vision))
    response = computervision.read_in_stream(open(image, 'rb'), raw=True)

    read_operation = response.headers['Operation-Location']
    operation_id = read_operation.split("/")[-1]

    while(True):
        read_result = computervision.get_read_result(operation_id)
        if read_result.status not in ['notStarted', "running"]:
            break
        time.sleep(1)

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                text.append(line.text)

    if len(text) != 0:
        return text

    return {'Response' : 'No Text Detected!'}

class ImageFile(Resource):
    def get(self, id):
        image = Image.query.get(id)
        if image is None:
            return {'Response' : '404: Das Bild mit der ID: %d konnte nicht gefunden werden!' % id}
        return image.getJson()
    def put(self, id):
        print(id)

        text = get_image_text('.' + request.form['UPLOAD_FOLDER'] + '/' + request.form['Imagename'])
        translation = translate('en', text)

        image = Image(Titel=request.form['Titel'], Description=request.form['Description'], Device=request.form['Device'],
                      Date=request.form['Date'], Imagename=request.form['Imagename'], Upload_folder=request.form['UPLOAD_FOLDER'],
                      Translation={'Text' : str(translation)}, ReadText={'Text' : str(text)})
        print("DB access")
        db_session.add(image)
        db_session.flush()
        notify_users()
        return {'Response': '200: Bild wurde gespeichert'}
    def delete(self, id):
        image = Image.query.get(id)
        if image is None:
            return {'Response' : '404: Das Bild mit der ID: %d konnte nicht gefunden werden' % id}
        db_session.delete(image)
        db_session.flush()
        return {'Response' : '202: Das Bild mit ID: %d wurde erfolgreich gelöscht' % id}

class ImageFiles(Resource):
    def get(self):
        images = Image.query.all()
        if images == None:
            return {"Response" : "500 : Something went wrong while loading the Image info!"}

        response = []
        for i in images:
            response.append(i.getJson())
        # return {"Response" : "200 : %s" % response}
        return jsonify({"Response" : response})

api.add_resource(ImageFile, '/image/<int:id>')
api.add_resource(ImageFiles, '/images')


if __name__ == '__main__':
    app.run(debug=True)
