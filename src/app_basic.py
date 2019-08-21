import os
from flask import Flask, render_template, request
import argparse
import datetime
import pprint
import shutil

# [START storage_upload_file]
from google.cloud import storage

__author__ = 'Dang'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
bucket_name = 'file-input-kpmg'
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    filename = 'key.json'
    destination = "/".join([APP_ROOT, filename])
    storage_client = storage.Client.from_service_account_json(destination)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def download_blob(bucket_name, source_file_name, destination_blob_name):
    blobs = storage_client.list_blobs(bucket_name)


@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        file.save(destination)
        upload_blob('file-input-kpmg',destination,filename)
        print('finish')
    for file in request.files.getlist("signature"):
        print(file)
        filename = 'signature.pdf'
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        file.save(destination)
        upload_blob('file-input-kpmg',destination,filename)
        print('finish')
    shutil.rmtree(target)
    return render_template("complete.html")


app.route("/download", methods=['GET'])
def download():
    
    return render_template("complete.html")
if __name__ == "__main__":
    app.run(port=4555, debug=False)