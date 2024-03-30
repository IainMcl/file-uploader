# File Upload
## Overview
An API to handle large file uploads with scalability.

Features
List the key features of your project.

Ping Endpoint: Provides a simple endpoint to check if the server is running.
File Upload Endpoint: Allows users to upload files to the server.


## Technologies Used
* FastAPI
* RabbitMQ 
* PostgreSQL 
* Docker


## How to Run
Open in a dev container by cloning 

```bash
git clone https://github.com/IainMcl/file-uploader.git
```

This dev container will contain the necesary things to develop the app.

This container will include docker so the app can be run using 

``` bash
docker-compose up
```

The `--build` argument can be added to rebuild including the latest changes.

To test the api make a get request to `http://localhost:8080/ping`.

## Prerequisites

Python 3.11
Docker
Installation
Clone the repository: https://github.com/IainMcl/file-uploader.git

