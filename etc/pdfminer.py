##----------------------------------Using PDF Miner--------------------------------------------------

# from pdfminer3.layout import LAParams, LTTextBox
# from pdfminer3.pdfpage import PDFPage
# from pdfminer3.pdfinterp import PDFResourceManager
# from pdfminer3.pdfinterp import PDFPageInterpreter
# from pdfminer3.converter import PDFPageAggregator
# from pdfminer3.converter import TextConverter
# import io

# resource_manager = PDFResourceManager()
# fake_file_handle = io.StringIO()
# converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
# page_interpreter = PDFPageInterpreter(resource_manager, converter)

# with open('file3.pdf', 'rb') as fh:

#     for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
#         page_interpreter.process_page(page)
#         # print("PAGE: ", page)

#     text = fake_file_handle.getvalue()

# # close open handles
# converter.close()
# fake_file_handle.close()

# print(text)

##----------------------------------------Using PyPdf & pdfminer------------------------------------------------------------



import PyPDF2
PDFFile = open("file3.pdf",'rb')

PDF = PyPDF2.PdfFileReader(PDFFile)
pages = PDF.getNumPages()
key = '/Annots'
uri = '/URI'
ank = '/A'
rect='/Rect'

urlLoc=[]

for page in range(pages):
    if(page==14):
        # print("Current Page: {}".format(page))
        pageSliced = PDF.getPage(page)
        pageObject = pageSliced.getObject()
        # print("Page object: ", pageObject)
        #print(pageObject)
        if key in pageObject.keys():
            ann = pageObject[key]
            for a in ann:
                u = a.getObject()
                #print(u)
                if uri in u[ank].keys():
                    urlLoc.append((u[ank][uri], u[rect]))
                    
                    # print(float(u[rect][1]))
                    # print(u[ank][uri])
                    # print()
print("Number of URLs = {}".format(len(urlLoc)))
# print(urlLoc, "\n")

import math
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator

import re

fp = open('file3.pdf', 'rb')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = PDFPage.get_pages(fp)

pat = "([0-9]+\.)+"

elementLoc=[]
final_elements=[]

pagecount=0
for page in pages:
    if(pagecount==14):
        # print('Processing next page...')
        interpreter.process_page(page)
        layout = device.get_result()
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                x1, y1, x2, y2, text = lobj.bbox[0], lobj.bbox[1], lobj.bbox[2], lobj.bbox[3], lobj.get_text()
                elementLoc.append((lobj.get_text(), lobj.bbox))
                versions = re.findall(pat, lobj.get_text())
                if (len(versions) > 1):
                    final_elements.append(versions[1])
                else:
                    final_elements.append(versions)
                # print(type(lobj.bbox[0]))
                # print('At %r is text: %s' % ((x1, y1, x2, y2), text))
    pagecount+=1

# print(elementLoc)

final=[]

for i in urlLoc:
    found=0
    for j in range(len(elementLoc)):
        # if( ((math.ceil(float(i[1][0])) == math.ceil(j[1][0]))  and (math.ceil(float(i[1][1])) == math.ceil(j[1][1]))) or ((math.ceil(float(i[1][1])) == math.ceil(j[1][1]))  and (math.ceil(float(i[1][2])) == math.ceil(j[1][2]))) ):
        # if( ((round(float(i[1][0]) / j[1][0]) == 1) and  (round(float(i[1][1]) / j[1][1]) == 1)) or ((round(float(i[1][1]) / j[1][1]) == 1) and  (round(float(i[1][2]) / j[1][2]) == 1))):
        if( ((round(float(i[1][0])) == round(elementLoc[j][1][0]))  and (round(float(i[1][1])) == round(elementLoc[j][1][1]))) or ((round(float(i[1][1])) == round(elementLoc[j][1][1]))  and (round(float(i[1][2])) == round(elementLoc[j][1][2]))) ):

            #final[elementLoc[j][0]]=i[0]
            final.append((elementLoc[j][0], i[0]))
            # final.append((final_elements[j], i[0]))

            # print(type(elementLoc[j][0]))
            found=1
            break
    if(found==0):
        print("Url not matched: ", i)

print("Number of mapped URLs = {}\n".format(len(final)))
for i in final:
    print("{} : {}\n".format(i[0], i[1]))



all_versions = "".join(i[0] for i in final)

from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# print(all_versions)


pattern="[0-9]+\.[0-9]+"

groups =[]
def group(string, index):
    #print(string)
    if len(groups)==0:
      matched=re.search(pattern, string)
      if(bool(matched) == 1):
        groups.append([string +":"+str(index)])
        return     
    
    else:
            matched=re.search(pattern, string)
            if(bool(matched)==0):
              return
            else:
              pat=matched.group(0)
              #print("AAAAA.",pat) 
              pat=pat.replace('.', '\.')             
              for i in range(len(groups)):       
                check = re.search( pat, groups[i][0].split(":")[0])
                #print(groups[i][0],pat)
                if ( (bool(check)==1) or (similar(string, groups[i][0].split(":")[0]) > 0.85) ):
                  #print("BBBBB.",pat,string,check.group(0))
                  if(string not in [j.split(":")[0] for j in groups[i]]):   
                    #   [j.split(":")[0] for j in groups[i]]
                    groups[i].append(string + ":" + str(index))
                    return 
              groups.append([string + ":" + str(index)])
                  

               


T = [t.strip() for t in all_versions.split("\n") if t]

for i in range(len(T)):
    group(T[i], i)

print(len(groups))

for i in groups:
    print(i)

## -------------------------------------------------------------------------------------------------------------------------
