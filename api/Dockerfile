# Use an official Python runtime as a base image
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 8080

ENV ENVIRONMENT=development

# run on host 0.0.0.0 to make accessible from outside the container on localhost
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
