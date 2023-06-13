from enum import Enum
from fastapi import FastAPI, File, UploadFile
import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from starlette.responses import StreamingResponse
import uvicorn

app = FastAPI(debug=True)  # Create a new FastAPI app instance

# Define an Enum class to represent the possible categories for an item


class BeanQuality(str, Enum):
    good = "good"
    bad = "bad"


# Load the pre-trained model
new_model = tf.keras.models.load_model('deploy-model-pmskt/model_bean_condition.h5')

# Define the predict endpoint


@app.post("/predict", response_model=BeanQuality)
async def predict(file: UploadFile = File(..., description="Image file to predict")):
    def preprocess_image(image):
        img = cv2.resize(image, (224, 224))
        img = img / 255.0
        return img

    def predict_image(image):
        predictions = new_model.predict(np.expand_dims(image, axis=0))
        predicted_label = int(round(predictions[0][0]))

        # Print the predicted label
        print(f"{'bad' if predicted_label == 0 else 'good'} bean.")

        # Load and display the image
        plt.imshow(image)
        plt.title(
            f"Predicted: {'bad' if predicted_label == 0 else 'good'} bean")
        plt.axis('off')
        plt.show()

        if predicted_label == 0:
            return BeanQuality.bad
        else:
            return BeanQuality.good

    # Read the image file
    img = cv2.imdecode(np.fromstring(await file.read(), np.uint8), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Preprocess and predict the image
    img = preprocess_image(img)
    result = predict_image(img)

    return result
