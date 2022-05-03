import base64
import time
from io import BytesIO
from time import sleep

import requests, uuid
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

import ids

host = 'http://localhost:5000/image/'
# from picamera import PiCamera

def decode_image(file_name, raw):
    pass
    #raw_64 = data.encode('utf-8')
    #while open(file_name, "rb") as file:
     #   decoded_image = base64.decodebytes(data_base64)
      #  file.write(decoded_image)

def encode_image(raw):
    encoded_image = base64.b64encode(raw)
    return encoded_image.decode('utf-8')


def temp():
    my_stream = BytesIO()
    # camera = PiCamera()
    # camera.start_preview()

    sleep(10)

    # camera .capture(my_stream, 'png')
    data = my_stream.getvalue()

    encoded = encode_image(data)

    response = requests.get(r"%s/%s" % (host, '1')).json()
    print(response)

result = requests.put(host + '1', data={
    "Titel": "Test",
    "Description": "This is test",
    "Device": "Laptop",
    "Date": "2022-03-21",
    "Imagename": "test.png",
    "UPLOAD_FOLDER": "/pics/test"
})

print(result)


# final_url = ids.endpoint_translation + '/translate'
# params = {
#     'api-version' : '3.0',
#     'from' : 'en',
#     'to' : 'de'
# }
#
# headers = {
#     'Ocp-Apim-Subscription-Key': ids.sub_key_transl,
#     'Ocp-Apim-Subscription-Region': ids.transl_location,
#     'Content-type': 'application/json',
#     'X-ClientTraceId': str(uuid.uuid4())
# }
#
# body = [{
#     'text' : 'Good morning everyone!'
# }]
#
# result = requests.post(final_url, params=params, headers=headers, json=body)
# print(result.json())
#
# computervision = ComputerVisionClient(ids.endpoint_vision, CognitiveServicesCredentials(ids.sub_key_vision))
# readimage_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Blocksatz-Beispiel_deutsch%2C_German_text_sample_with_fully_justified_text.svg/800px-Blocksatz-Beispiel_deutsch%2C_German_text_sample_with_fully_justified_text.svg.png'
# response = computervision.read(readimage_url, raw=True)
#
# read_operation = response.headers["Operation-Location"]
# operation_id = read_operation.split("/")[-1]
#
# while True:
#     read_result = computervision.get_read_result(operation_id)
#     if read_result.status not in ["notStarted", "running"]:
#         break
#     time.sleep(1)
#
#
# if read_result.status == OperationStatusCodes.succeeded:
#     for text_result in read_result.analyze_result.read_results:
#         for line in text_result.lines:
#             print(line.text)
#

