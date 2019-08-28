import pickle
from fpdf import FPDF
from PyPDF2 import PdfFileWriter,PdfFileReader
import os
from pathlib import Path
class PDF:
    watermark_file = "tuto3.pdf"
    def __init__(self, name, signature, date):
        self.name = name
        self.signature = signature
        self.date = date

    def create_signature(self,signature_file):
        pdf=FPDF('P','pt',(612 ,792))
        pdf.add_page()
        pdf.set_font('Times','',10.0)
        if len(self.date.__dict__) > 0:
            pdf.set_xy(self.date.x,self.date.y)
            pdf.cell(2.5,0.0,'08/14/2019')

        pdf.image(signature_file,self.signature.x,self.signature.y,90)
        pdf.output(PDF.watermark_file, 'F')



    def sign_document(self,input_file,output_file_path):
            # Number of pages in input document
        input_file = PdfFileReader(open(input_file, "rb"))
        output_file = PdfFileWriter()
        page_count = input_file.getNumPages()
        watermark = PdfFileReader(open(PDF.watermark_file, "rb"))
        # Go through all the input file pages to add a watermark to them
        for page_number in range(page_count):
            # merge the watermark with the page
            input_page = input_file.getPage(page_number)
            if page_number ==   self.signature.page:
                input_page.mergePage(watermark.getPage(0))
            # add page from input file to output document
            output_file.addPage(input_page)

        # finally, write "output" to document-output.pdf
        with open(output_file_path, "wb") as outputStream:
            output_file.write(outputStream)

    @classmethod
    def export_location(cls,obj,name):
        with open('obj/'+ name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def import_location(cls,name):
        name = name + '.pkl'
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        filepath =  "/".join([APP_ROOT,name])
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    pass


#pdf = PDF()
#pdf.location = {
#    'value': 1,
#    'location':2
#    }
#PDF.location_data['test1'] = pdf

#PDF.export_location(PDF.location_data,'locations_data')
