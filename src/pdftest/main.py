from fpdf import FPDF
from PyPDF2 import PdfFileWriter,PdfFileReader
from miner import find_text, get_file_name

import os
from Class_PDF import PDF
from google.cloud import storage
import zipfile

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#input_file = "mo-1120-sign.pdf"
#input_file = "f1120.pdf"

filename = 'key.json'
destination = "/".join([APP_ROOT, filename])
storage_client = storage.Client.from_service_account_json(destination)

input_file_list = ["f1120_sign.pdf","mo-1120-sign.pdf"]

signature = 'signature.png'
location_file = 'locations_data'
data = PDF.import_location(location_file)

#bucket_name = 'file-input-kpmg'
prefix = '/*.pdf'
dl_dir = ''

def main(bucket_name):
    list_of_file = []
    bucket = storage_client.get_bucket(bucket_name)
    blobs = storage_client.list_blobs(bucket_name)
    zip = zipfile.ZipFile('return.zip', 'w')
    for blob in blobs:
        if blob.content_type == 'application/pdf' and 'signed' not in blob.name:
            blob.download_to_filename(blob.name)
            list_of_file.append(blob.name)
        else:
            blob.download_to_filename(signature)
    for i in list_of_file:
        output_file = sign_document(i,signature)
        zip.write(output_file,compress_type=zipfile.ZIP_DEFLATED)
        #blob = bucket.blob(output_file)
        #blob.upload_from_filename(output_file)
    zip.close()
    blob = bucket.blob(zip.filename)
    blob.upload_from_filename(zip.filename)

def main2(folder_name):
    list_of_file = []
    bucket_name = 'file-input-kpmg'
    bucket = storage_client.get_bucket(bucket_name)
    zip = zipfile.ZipFile('return.zip', 'w')
    for file in os.listdir(folder_name):
        if file.endswith(".pdf"):
            list_of_file.append(file)
        elif file.endswith(".png"):
            file = signature
    for i in list_of_file:
        output_file = sign_document(i,signature)
        zip.write(output_file,compress_type=zipfile.ZIP_DEFLATED)
        #blob = bucket.blob(output_file)
        #blob.upload_from_filename(output_file)
    zip.close()
    blob = bucket.blob(zip.filename)
    blob.upload_from_filename(zip.filename)



#def download_blob(bucket_name, source_blob_name, destination_file_name):
#    """Downloads a blob from the bucket."""
#    bucket = storage_client.get_bucket(bucket_name)
#    blob = bucket.blob(source_blob_name)

#    blob.download_to_filename(destination_file_name)

#    print('Blob {} downloaded to {}.'.format(
#        source_blob_name,
#        destination_file_name))




def extract_data(input_file_list):
    for input_file in input_file_list:
        name,signature_coor,date_coor = find_text(input_file)
        WIP_file = PDF(name,signature_coor,date_coor)
        data[name] = WIP_file
    
    PDF.export_location(data,location_file)

def sign_document(input_file_path,signature_path):
    output_file_path = "signed" + input_file_path 
    name = get_file_name(input_file_path)
    data[name].create_signature(signature_path)
    data[name].sign_document(input_file_path,output_file_path)
    return output_file_path



if __name__ == '__main__':
    main()