from pdfminer3.pdfparser import PDFParser
from pdfminer3.pdfdocument import PDFDocument
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfpage import PDFTextExtractionNotAllowed
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfdevice import PDFDevice
from pdfminer3.layout import LAParams
from pdfminer3.converter import PDFPageAggregator
import pdfminer3

# Open a PDF file.
fp = open('file3.pdf', 'rb')

# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)

# Create a PDF document object that stores the document structure.
# Password for initialization as 2nd parameter
document = PDFDocument(parser)

# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()

# Create a PDF device object.
device = PDFDevice(rsrcmgr)

# BEGIN LAYOUT ANALYSIS
# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)

def parse_obj(lt_objs):

    # loop over the object list
    for obj in lt_objs:

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer3.layout.LTTextBoxHorizontal):
            print(obj.bbox, obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_'))

        # if it's a container, recurse
        elif isinstance(obj, pdfminer3.layout.LTFigure):
            parse_obj(obj._objs)

# loop over all pages in the document
pagecount=0
for page in PDFPage.create_pages(document):
    pagecount+=1
    if(pagecount==16):
    # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # extract text from this object
        parse_obj(layout._objs)