from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator


class coordinate():

    def update(self,x,y,page):
        self.x = x
        self.y = y
        self.page = page


def get_file_name(input_file):
    fp = open(input_file, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)
    name = ''
    true = 0
    for page_num,page in enumerate(pages):
        interpreter.process_page(page)
        layout = device.get_result()
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                if 'Form' in lobj.get_text() and name == '':
                    x = lobj.get_text()
                    x = x.strip('Form')
                    x = x.strip('\n')
                    if len(x) > 1:
                        name = "".join(x.split())
                        return name
                    else:
                        true = 1
                        continue
                if true == 1 and name == '':
                    true = 0
                    name = "".join(lobj.get_text().split())
                    return name
    

def find_text(input_file):
    fp = open(input_file, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)
    count = 0
    signature  = coordinate()
    date_sign = coordinate()
    name = ''
    true = 0
    for page_num,page in enumerate(pages):
        print('Processing next page...')
        interpreter.process_page(page)
        layout = device.get_result()
        
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                if 'Form' in lobj.get_text() and name == '':
                    x = lobj.get_text()
                    x = x.strip('Form')
                    x = x.strip('\n')
                    if len(x) > 1:
                        name = "".join(x.split())
                    else:
                        true = 1
                        continue
                if true == 1 and name == '':
                    true = 0
                    name = "".join(lobj.get_text().split())
                if 'Sign Here' in lobj.get_text():
                    x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
                    print('At %r is text: %s' % ((x, y), text))
                    signature.update(x,792-y,page_num)
                    count = count + 1
                if 'Date Here' in lobj.get_text():
                    x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
                    print('At %r is text: %s' % ((x, y), text))
                    date_sign.update(x,792-y,page_num)
                    count = count + 1
                if count == 2:
                    return name,signature,date_sign
    return name, signature,date_sign


        
   
