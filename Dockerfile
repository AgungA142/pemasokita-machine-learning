FROM python:3.10.10

WORKDIR /workspace

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Install OpenCV
RUN apt-get update && \
    apt-get install -y libgl1-mesa-dev && \
    pip install opencv-python

COPY . .

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

# CMD ["python", "main.py"]

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]
