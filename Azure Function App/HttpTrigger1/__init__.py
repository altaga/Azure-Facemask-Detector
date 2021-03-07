import logging
from tflite_runtime.interpreter import Interpreter
import azure.functions as func
import time
import cv2
import numpy as np
import base64

face_cascade = cv2.CascadeClassifier('HttpTrigger1/haarcascade_frontalface_default.xml')
interpreter = Interpreter("HttpTrigger1/converted_model_opt.tflite")
interpreter.allocate_tensors()

def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('flag')
    try:
        if name:
            image = req.get_body()  # raw data with base64 encoding
            decoded_data = base64.b64decode(image)
            np_data = np.fromstring(decoded_data,np.uint8)
            frame = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
            if(frame.shape[1] > frame.shape[0]):
                width = int(640)
                height = int(480)
                dim = (width, height)
                frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            else:
                width = int(480)
                height = int(640)
                dim = (width, height)
                frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.045,5, minSize=(100, 100))
            marker = 0
            predict=0
            # Loop face detection
            for (x,y,w,h) in faces:
                if(w>109): # Detecting only the closest faces
                    # Taking the processing times to get the FPS
                    start_time = time.time()
                    # Processing the image to go through the TFlite model
                    raw_data = []
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_gray = cv2.resize(roi_gray, (64,64), interpolation = cv2.INTER_AREA)
                    roi_gray = roi_gray/255.0
                    raw_data.append(roi_gray)
                    raw_data = np.array(raw_data, dtype="float32")
                    raw_data = np.expand_dims(raw_data, axis=3)
                    # Passing the image through the neural network.
                    input_index = interpreter.get_input_details()[0]["index"]
                    output_index = interpreter.get_output_details()[0]["index"]
                    interpreter.set_tensor(input_index, raw_data)
                    interpreter.invoke()
                    predictions = interpreter.get_tensor(output_index)
                    predict=np.argmax(predictions[0])
                    if(predict):
                        predict="Facemask ON"
                    else:
                        predict="Facemask OFF"
                    #print("FPS: ", 1.0 / (time.time() - start_time))
                    return func.HttpResponse(f"{predict}")
                else:
                    return func.HttpResponse(f"No Face Detected")
        else:
            return func.HttpResponse(f"Flag Error")
    except:
        return func.HttpResponse(f"Request Error")
