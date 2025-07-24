from flask import Flask, request
import boto3

app = Flask(__name__)

# Replace with your actual bucket name and region
BUCKET_NAME = 'global-ai-impact-project'  # <-- change this!
AWS_REGION = 'ap-south-1'

s3 = boto3.client('s3', region_name=AWS_REGION)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        return f"Uploaded {file.filename} to S3 bucket {BUCKET_NAME}", 200
    return "No file provided", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

