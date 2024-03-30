from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from io import BytesIO
import pika
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    # Allow all origins, you may want to restrict this in production
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    """
    Health check endpoint
    """
    return {"ping": "pong"}


def process_file(file_data: BytesIO, filename: str, metadata: dict):
    """
    Process the file and send metadata to RabbitMQ

    :param file_data: BytesIO: File data
    :param filename: str: File name
    :param metadata: dict: Metadata of the file
    """
    logger.info("Processing file: %s", filename)
    time = datetime.now()
    time_ext = time.strftime("%Y%m%d%H%M%S")
    write_file_path = f"uploads/{time_ext}{filename}"
    metadata["write_file_path"] = write_file_path
    metadata["processed_start_time"] = time.isoformat()
    with open(write_file_path, "wb") as f:
        f.write(file_data.getvalue())

    logger.info("File %s processed", filename)
    # Send metadata to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )
    channel = connection.channel()

    channel.queue_declare(queue='upload')

    channel.basic_publish(
        exchange='',
        routing_key='upload',
        body=json.dumps(metadata)
    )

    connection.close()

    logger.info("Metadata: %s", metadata)


@app.post("/upload/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Upload file and start processing

    :param background_tasks: BackgroundTasks: FastAPI background tasks
    :param file: UploadFile: File to upload
    """
    try:
        resp = {"message": "File upload started"}
        file_data = BytesIO(await file.read())
        metadata = {"filename": file.filename, "content_type": file.content_type,
                    "file_size": file.size}
        background_tasks.add_task(
            process_file, file_data, file.filename, metadata)
        return JSONResponse(status_code=200, content=resp)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error uploading file: {str(e)}"})
