from fpdf import FPDF
from PyPDF2 import PdfFileWriter,PdfFileReader
from miner import find_text, get_file_name
from Class_PDF import PDF


#input_file = "mo-1120-sign.pdf"
#input_file = "f1120.pdf"

input_file_list = ["f1120_sign.pdf","mo-1120-sign.pdf"]

signature = '2.png'
location_file = 'locations_data'
data = PDF.import_location(location_file)

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

for i in input_file_list:
    sign_document(i,signature)

