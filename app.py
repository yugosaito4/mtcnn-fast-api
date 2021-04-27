from fastapi import FastAPI,Form
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from mtcnn import MTCNN

import cv2
import base64
import numpy as np


app = FastAPI()

detector = MTCNN()

class Meta(BaseModel):
    image: str = None
    bbox: List[float] = None
    score : float = None
    text: str = None
    audio: str = None

@app.get('/')
def say_hi():
    return{"hello world"}


@app.post('/predict')
def post_data_v1(
    image_base64: str = Form(...)
    ):
    content = base64.b64decode(image_base64)
    nparr = np.fromstring(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print(img.shape)
    Result = detector.detect_faces(img)
    output = []

    for i in range(len(Result)):
        boundingbox = Result[i]['box']
        score = Result[i]['confidence']
        # [x1,y1:x2:y2]
        cropped_img = img[boundingbox[1]:boundingbox[1] + boundingbox[3],boundingbox[0]:boundingbox[0]+boundingbox[2]]
        retval, buffer = cv2.imencode('.jpg', cropped_img)
        derived_b64_str = base64.b64encode(buffer)
        output.append({
                "bbox": boundingbox,
                "score" : score,
                "text": None,
                "audio": None,
                "image" : derived_b64_str
        })
    return output

app.post('/meta')
def get_meta(): 
    return {
        "arguments": [
            
        ]}