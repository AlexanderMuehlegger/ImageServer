from flask import Flask, request, render_template, jsonify
from flask_restful import Api, Resource
from sqlalchemy import Column, Integer, Text, DateTime, create_engine, LargeBinary
import paho.mqtt.client as mqtt
import time

from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

import keys

app = Flask(__name__)
api = Api(app)

Base = declarative_base()
metadata = Base.metadata

engine = create_engine(r'sqlite:///.\images.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)

client = mqtt.Client('RaspberryPi')
client.username_pw_set(keys.username, keys.pw)
client.connect(keys.ip, port=keys.port)

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

    def getJson(self):
        return {
            'ID': str(self.ID),
            'Titel': self.Titel,
            'Description': self.Description,
            'Device': self.Device,
            'Date': self.Date,
            'Imagename': self.Imagename,
            'UPLOAD_FOLDER' : self.Upload_folder
        }

def notify_users():
    client.publish("foto/taken/dev0", "A new image has been uploaded!!!!")

class ImageFile(Resource):
    def get(self, id):
        image = Image.query.get(id)
        if image is None:
            return {'Response' : '404: Das Bild mit der ID: %d konnte nicht gefunden werden!' % id}
        return image.getJson()
    def put(self, id):
        print(id)
        image = Image(Titel=request.form['Titel'], Description=request.form['Description'], Device=request.form['Device'],
                      Date=request.form['Date'], Imagename=request.form['Imagename'], Upload_folder=request.form['UPLOAD_FOLDER'])
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
