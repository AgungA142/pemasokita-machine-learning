FROM python:3.10.10-slim

# copy necessary files for the container
COPY requirements.txt .
COPY main.py .

# install dependencies
RUN pip install opencv-python
RUN pip install numpy matplotlib
RUN pip install -r requirements.txt

# expose port
EXPOSE 8080

# finally run the application inside the container 
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["uvicorn", "main:app", "--workers", "1", "--timeout-keep-alive", "0", "--port", "8080", "--host", "0.0.0.0"]
