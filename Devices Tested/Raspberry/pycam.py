from picamera import PiCamera
import time
import requests
import base64
key=""
with open('key.password', 'r') as file:
    key = file.read().replace('\n', '')

start = time.time()

camera = PiCamera()
camera.resolution = (640, 480) # Model Resolution
camera.start_preview()
camera.capture('/home/pi/Desktop/image.jpg')
camera.stop_preview()

encoded_string = ""

with open("/home/pi/Desktop/image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

url = "https://facemask-apim.azure-api.net/tensorpython37/HttpTrigger1?flag=read"

payload=encoded_string

headers = {
  'Host': 'facemask-apim.azure-api.net',
  'Ocp-Apim-Subscription-Key': key,
  'Ocp-Apim-Trace': 'true',
  'Content-Type': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
print(time.time() - start)
