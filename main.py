from enum import Enum
from fastapi import FastAPI, Response, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import cv2
import tensorflow as tf
from PIL import Image
from io import BytesIO
import numpy as np
import uvicorn

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


class BeanQuality(str, Enum):
    good = "good"
    bad = "bad"


class BeanRoast(str, Enum):
    Raw = "Raw"
    MediumRoast = "Medium Roast"
    DarkRoast = "Dark Roast"
    LightRoast = "Light Roast"


class BeanType(str, Enum):
    Arabika = "Arabika"
    Robusta = "Robusta"
    liberica = "liberica"


def preprocess_image(image):
    img = cv2.resize(image, (224, 224))
    img = img / 255.0
    return img


def predict_roast(image):
    preprocessed_image = preprocess_image(image)
    predictions = new_model2.predict(
        np.expand_dims(preprocessed_image, axis=0))
    predicted_label = np.argmax(predictions)

    class_names = ['Raw', 'Medium Roast', 'Dark Roast', 'Light Roast']
    predicted_class = class_names[predicted_label]
    print(f"{predicted_class} bean.")

    if predicted_label == 0:
        return BeanRoast.Raw
    elif predicted_label == 1:
        return BeanRoast.MediumRoast
    elif predicted_label == 2:
        return BeanRoast.DarkRoast
    else:
        return BeanRoast.LightRoast


def predict_condition(image):
    preprocessed_image = preprocess_image(image)
    predictions = new_model.predict(np.expand_dims(preprocessed_image, axis=0))
    predicted_label = int(round(predictions[0][0]))

    print(f"{'bad' if predicted_label == 0 else 'good'} bean.")

    if predicted_label == 0:
        return BeanQuality.bad
    else:
        return BeanQuality.good


def predict_type(image):
    preprocessed_image = preprocess_image(image)
    predictions = new_model3.predict(
        np.expand_dims(preprocessed_image, axis=0))
    predicted_label = np.argmax(predictions)

    class_names = ['Arabika', 'Robusta', 'liberica']
    predicted_class = class_names[predicted_label]
    print(f"{predicted_class} bean.")

    if predicted_label == 0:
        return BeanType.Arabika
    elif predicted_label == 1:
        return BeanType.Robusta
    else:
        return BeanType.liberica


new_model = tf.keras.models.load_model('model_bean_condition.h5')
new_model2 = tf.keras.models.load_model('crop_classification_model-roast.h5')
new_model3 = tf.keras.models.load_model('model-arabika.h5')


@app.post("/predict_condition", response_model=BeanQuality)
async def predict_condition_endpoint(uploaded_file: UploadFile, response: Response):
    if uploaded_file.content_type not in ["image/jpeg", "image/png"]:
        response.status_code = 400
        return "File is Not an Image"

    image = np.array(Image.open(BytesIO(uploaded_file.file.read())))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = predict_condition(image)

    return JSONResponse({"result": result})


@app.post("/predict_roast", response_model=BeanRoast)
async def predict_roast_endpoint(uploaded_file: UploadFile, response: Response):
    if uploaded_file.content_type not in ["image/jpeg", "image/png"]:
        response.status_code = 400
        return "File is Not an Image"

    image = np.array(Image.open(BytesIO(uploaded_file.file.read())))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = predict_roast(image)

    return JSONResponse({"result": result})


@app.post("/predict_type", response_model=BeanType)
async def predict_type_endpoint(uploaded_file: UploadFile, response: Response):
    if uploaded_file.content_type not in ["image/jpeg", "image/png"]:
        response.status_code = 400
        return "File is Not an Image"

    image = np.array(Image.open(BytesIO(uploaded_file.file.read())))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = predict_type(image)

    return JSONResponse({"result": result})


@app.get("/upload")
async def get_html():
    return FileResponse("static/index.html", media_type="text/html")
