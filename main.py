from flask import Flask, request
from flask_restful import Api, Resource
from sqlalchemy import Column, Integer, Text, DateTime, create_engine, LargeBinary

from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

app = Flask(__name__)
api = Api(app)

Base = declarative_base()
metadata = Base.metadata

engine = create_engine(r'sqlite:///.\images.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)

class Image(Base):
    __tablename__ = 'Image'

    ID = Column(Integer, primary_key=True)
    Titel = Column(Text)
    Describtion = Column(Text)
    Device = Column(Text)
    Date = Column(Text)
    Picture = Column(Text)
    Upload_folder = Column(Text)

    def getJson(self):
        return {
            'ID': str(self.ID),
            'Title': self.Titel,
            'Describtion': self.Describtion,
            'Device': self.Device,
            'Date': self.Date,
            'Imagename': self.Picture,
            'UPLOAD_FOLDER' : self.Upload_folder
        }

class ImageFile(Resource):
    def get(self, id):
        image = Image.query.get(id)
        if image is None:
            return {'Response' : '404: Das Bild mit der ID: %d konnte nicht gefunden werden!' % id}
        return image.getJson()
    def put(self, id):
        image = Image.query.get(id)
        if image is not None:
            return {'Response' : '500: Ein Bild mit der ID: %d existiert bereits' % id}
        image = Image(Title=request.form['Title'], Description=request.form['Description'], Device=request.form['Device'],
                      Date=request.form['Date'], Imagename=request.form['Imagename'], Upload_folder=request.form['Upload_folder'])
        db_session.add(image)
        db_session.flush()
        return {'Response': '200: Bild wurde gespeichert'}
    def download(self, id):
        image = Image.query.get(id)
        if image is None:
            return {'Response' : '404: Das Bild mit der ID: %d konnte nicht gefunden werden' % id}
        db_session.delete(image)
        db_session.flush()
        return {'Response' : '202: Das Bild mit ID: %d wurde erfolgreich gelöscht' % id}

api.add_resource(ImageFile, '/image/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
