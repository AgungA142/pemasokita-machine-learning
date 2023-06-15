FROM python:3.10.10-slim

# Copy necessary files for the container
COPY requirements.txt .
COPY main.py .

# Install dependencies
RUN pip install opencv-python numpy matplotlib
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8081

# finally run the application inside the container 
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["uvicorn", "main:app", "--workers", "1", "--timeout-keep-alive", "0", "--port", "8081", "--host", "0.0.0.0"]
