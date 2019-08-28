import os
from flask import Flask, render_template, request,send_file,Response,url_for
import argparse
import datetime
import pprint
import shutil
import sys
import zipfile

# [START storage_upload_file]
from google.cloud import storage

__author__ = 'Dang'

app = Flask(__name__,template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, "/".join([APP_ROOT, 'pdftest']))

import main
filename = 'key.json'
destination = "/".join([APP_ROOT, filename])
storage_client = storage.Client.from_service_account_json(destination)

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
        filename = 'signature.png'
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        file.save(destination)
        upload_blob('file-input-kpmg',destination,filename)
        print('finish')
    main.main(bucket_name)
    shutil.rmtree(target)
    return render_template("downloads.html")


@app.route('/file-downloads/')
def file_downloads():
	try:
		return render_template('downloads.html')
	except Exception as e:
		return str(e)
@app.route('/return-files/' ,methods=['GET', 'POST'])
def return_files():
    x = 1
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blobs = storage_client.list_blobs(bucket_name)
        for blob in blobs:
            if 'zip' in blob.content_type :
                destination_uri = "/".join([APP_ROOT, blob.name])
                blob.download_to_filename(destination_uri)
                print('Exported {} to {}'.format(
                        blob.name, destination_uri))
                return send_file(destination_uri,as_attachment=True, attachment_filename=blob.name)
    except Exception as e:
        return str(e)

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

if __name__ == '__main__':
    app.run()