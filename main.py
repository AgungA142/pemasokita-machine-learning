import uvicorn
from fastapi import FastAPI, Response, UploadFile
import cv2
import tensorflow as tf
from PIL import Image
from io import BytesIO
import numpy as np
from enum import Enum

# initiate an app
app = FastAPI()
new_model = tf.keras.models.load_model('bean_condition_saved_model')
# create a greeting message for an endpoint '/'
# we use neither path nor query parameters in this endpoint

class BeanQuality(str, Enum):
    good = "good"
    bad = "bad"

def preprocess_image(image):
    img = cv2.resize(image, (224, 224))
    img = img / 255.0
    return img

def predict_condition(image):
    preprocessed_image = preprocess_image(image)
    predictions = new_model.predict(np.expand_dims(preprocessed_image, axis=0))
    predicted_label = int(round(predictions[0][0]))

    print(f"{'bad' if predicted_label == 0 else 'good'} bean.")

    if predicted_label == 0:
        return BeanQuality.bad
    else:
        return BeanQuality.good


@app.get('/')
async def greeting():
    return 'Hello World!'

@app.post("/predict_condition", response_model=BeanQuality)
async def predict_condition_endpoint(uploaded_file: UploadFile, response: Response):
    if uploaded_file.content_type not in ["image/jpeg", "image/png"]:
        response.status_code = 400
        return "File is Not an Image"

    image = np.array(Image.open(BytesIO(uploaded_file.file.read())))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = predict_condition(image)

    return result


  
# run the app on defined host and port
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)