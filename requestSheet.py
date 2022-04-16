import base64
from io import BytesIO
from time import sleep
from datetime import date
import requests

host = 'http://localhost:5000/image'


# from picamera import PiCamera

def decode_image(file_name, raw):
    raw_64 = data.encode('utf-8')
    # while open(file_name, "rb") as file:
    #   decoded_image = base64.decodebytes(data_base64)
    #  file.write(decoded_image)


def encode_image(raw):
    encoded_image = base64.b64encode(raw)
    return encoded_image.decode('utf-8')


my_stream = BytesIO()
# camera = PiCamera()
# camera.start_preview()

sleep(10)

# camera .capture(my_stream, 'png')
data = my_stream.getvalue()

encoded = encode_image(data)

print(f"{host}/9999")

response = requests.put(f"{host}/9999999", data={
    "Date": str(date.today()),
    "Description": "Beautifull upload",
    "Device": "Raspberry Cam",
    "ID": "-1",
    "Imagename": "image232323.png",
    "Titel": "Beautifull Picture",
    "UPLOAD_FOLDER": "/picture/"
}).json()
print(response)

response = requests.get(f"{host}/{1}").json()
print(response)
