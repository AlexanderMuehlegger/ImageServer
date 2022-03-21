import base64
from io import BytesIO
from time import sleep

import requests

host = 'http://localhost:5000/image'
# from picamera import PiCamera

def decode_image(file_name, raw):
    raw_64 = data.encode('utf-8')
    #while open(file_name, "rb") as file:
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


response = requests.get(r"%s/%s" % (host, '1')).json()
print(response)