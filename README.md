# PemasoKita Deployed Model using Fast API

there are 3 model in this repository which is used to detect the condition of the coffee bean, the type of the coffee bean, and the roast level of a coffee bean. the model will classify an image to differentiate a good condition bean or bad condition bean, a robusta,arabika,or liberika type of bean, and a raw medium,or dark roast of the coffee bean.

# FastAPI USAGE

Documentation: https://fastapi.tiangolo.com

Source Code: https://github.com/tiangolo/fastapi

To run this file, do
```bash
uvicorn main:app
```
or
```bash
uvicorn main:app --reload
```
to automatically restart the kernel everytime there's a change saved inside `main.py`

# Using The App
1. clone this repository 
2. download the model in this link: https://drive.google.com/drive/folders/1N7EMzV63SgdF6qKa2lFg2Z7nY4dSLfeK?usp=sharing
3. save the downloaded model in the same directory as the **main.py** file
4. run app using the command mentioned before
### 1. Index
Endpoint: GET `/upload` <br>

The main page to use the app, upload an image and click the button to use the model and see the result.

Documentation:
![WhatsApp Image 2023-06-16 at 20 43 24](https://github.com/suryanurjaman/pemasokita-machine-learning/assets/76623119/8fce47fc-0839-41a4-9faa-eca27b149d29)
![WhatsApp Image 2023-06-16 at 20 44 19](https://github.com/suryanurjaman/pemasokita-machine-learning/assets/76623119/a11254a6-d169-423b-88a9-73818a80ab81)


**NOTE**: the key.json is for deployment purpose it access the service account on the google cloud to download the condition model directly to the same directory as *main.py* along with the other file, for now the deployed model on the cloud service is only the condition model for deployment testing purpose of the cloud computing



