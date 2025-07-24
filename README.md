# AI_impact_datapipeline
# AI Impact Project REST API

This project provides a basic Flask REST API to upload files to an AWS S3 bucket.

## Features

- Upload files via HTTP POST
- Stores files in your specified S3 bucket
- Hit lambda trigger that automatically capture a new file upload in S3 transform it using ETL script to tranform and upload transform data back to S3
- QuickSight is used for data visualization

## How to Use

1. Start the API:
    ```
    python restapi.py
    ```

2. Upload a file using a tool like `curl`:
    ```
    curl -F "file=@Global_AI_Content_Impact_Dataset.csv" http://localhost:5000/upload
    ```

## Configuration

- Set your S3 bucket name and AWS region in `restapi.py`:
    ```python
    BUCKET_NAME = 'global-ai-impact-project'
    AWS_REGION = 'ap-south-1'
    ```

## Requirements

- Python 3.x
- Flask
- boto3
- AWS credentials configured

## Files

- `restapi.py`: Main API source
