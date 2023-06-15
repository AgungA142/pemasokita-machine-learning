FROM tensorflow/tensorflow:latest-gpu

# copy necessary files for the container
COPY requirements.txt .
COPY main.py .

# install dependencies
RUN pip install -r requirements.txt

# expose port
EXPOSE 8081

# finally run the application inside the container 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]