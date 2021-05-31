# import pdfplumber
import math
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
import PyPDF2
import re
from collections import defaultdict
from difflib import SequenceMatcher

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


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

##Finding where divers section starts and ends-------------------------------------------------------------------------------------------------------------------------
# pdf=pdfplumber.open(r"file.pdf")
# subheaders = []
# inDrivers=False
# for i in range(len(pdf.pages)):
#     p = pdf.pages[i]
#     val = ''
#     for word in p.extract_words(x_tolerance=3, y_tolerance=10, extra_attrs=['size']):
#         if word['size']==18:
#             val = ' '.join([val, word['text']]).strip()
#         else:
#             if val != '':
#                 subheaders.append(val)
#                 if val == 'Drivers':
#                    start_idx = i+1
#                    inDrivers=True
#                 if ((val!="Drivers") and (inDrivers)):
#                     end_idx=i+1
#                     inDrivers=False
#                    #print(i)
#             val = ''

# print("'Drivers' subheading found on page: ",start_idx)
# print("Drivers section ends at page: ", end_idx)


PDFFile_for_pypdf = open("file4.pdf",'rb')
PDF_pypdf = PyPDF2.PdfFileReader(PDFFile_for_pypdf)
key = '/Annots'
uri = '/URI'
ank = '/A'
rect='/Rect'



fp_for_pdfminer = open('file4.pdf', 'rb')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages_for_pdf_miner = list(PDFPage.get_pages(fp_for_pdfminer))

start_idx = 17
end_idx = 20

page_contents = defaultdict(list)
all_groups = defaultdict(list)

for page in range(start_idx, end_idx+1):
    # print("Page {}:".format(page))

    urlLoc=[]
    pat = "([0-9]+\.)+"
    elementLoc=[]
    final_elements=[]
    final=[]
    ##get urls using pypdf-------------------------------------------------------------------------------------------------------------
    pageSliced = PDF_pypdf.getPage(page)
    pageObject = pageSliced.getObject()
    if key in pageObject.keys():
        ann = pageObject[key]
        for a in ann:
            u = a.getObject()
            if uri in u[ank].keys():
                urlLoc.append((u[ank][uri], u[rect]))

    # print("\t", urlLoc)
    # print("Number of URLs = {}".format(len(urlLoc)))
    ##get text using pdfminer-----------------------------------------------------------------------------------------------------------
    interpreter.process_page(pages_for_pdf_miner[page])
    layout = device.get_result()
    for lobj in layout:
        if isinstance(lobj, LTTextBox):
            x1, y1, x2, y2, text = lobj.bbox[0], lobj.bbox[1], lobj.bbox[2], lobj.bbox[3], lobj.get_text()
            elementLoc.append((lobj.get_text(), lobj.bbox))
            # print(lobj.get_text())
            versions = re.findall(pat, lobj.get_text())
            if (len(versions) > 1):
                final_elements.append(versions[1])
            else:
                final_elements.append(versions)
    # print("\t", elementLoc)
    ##mapping-----------------------------------------------------------------------------------------------------------------------------
    # urlloc = [[url, [x1, y1, x2, y2]]]
    # print("NUMBER OF LINKS IN PAGE: ", len(urlLoc), len(elementLoc))
    for i in urlLoc:
        min_ = 9999
        min_list = []
        for j in range(len(elementLoc)):
            diff_x1 = abs((float(i[1][0])) - (elementLoc[j][1][0]))
            diff_y1 = abs((float(i[1][1])) - (elementLoc[j][1][1]))
            diff_ = diff_x1 + diff_y1
            if(min_ > diff_):
                min_list = []
                min_ = diff_
                min_list.extend([elementLoc[j][0], i[0]])
        final.append(tuple(min_list))


        #     if( ((round(float(i[1][0])) == round(elementLoc[j][1][0]))  and (round(float(i[1][1])) == round(elementLoc[j][1][1]))) or ((round(float(i[1][1])) == round(elementLoc[j][1][1]))  and (round(float(i[1][2])) == round(elementLoc[j][1][2]))) ):
        #         final.append((elementLoc[j][0], i[0]))
        #         found=1
        #         break
        # # if(found==0):
        # #     print("Url not matched: ", i)
    page_contents[page] = final
    # print("NUMBER OF LINKS: ",len(final))
    # print("Page {}:".format(page))
    # for i in page_contents[page]:
    #     print("\t {}".format(i))

    #Grouping------------------------------------------------------------------------------------------------------------------------------
    all_versions = "".join(i[0] for i in final)
    pattern = "[0-9]+\.[0-9]+"
    groups = []
    # print(all_versions)
    T = [t.strip() for t in all_versions.split("\n") if t]

    for i in range(len(T)):
        group(T[i], i)
    
    all_groups[page] = groups





    # for i in groups:
    #     print(i)
    
    # print()



# for i in page_contents:
#     print(i)
#     for j in page_contents[i]:
#         print("\t{} : {}".format(j[0], j[1]))



#RULES--------------------------------------------------------------------------------------------

# define priorities
def pr(word):
    if 'Windows 10' in word:
        return 1
    if '2012' in word:
        return 2
    if '2016' in word:
        return 3
    if '2017' in word:
        return 4
    if '2018' in word:
        return 5
    if '2019' in word:
        return 6
    else:
        return 0

# compare elements in one group (list)
def comp(lst):
    # if any element in the list contains a letter, use the above priorities function
    if any(re.search('[a-zA-Z]', ele) for ele in lst):
        priorities = [[pr(ele),ele] for ele in lst]
        # sort list according to priority
        priorities.sort(reverse=True, key=lambda x: x[0])
        priorities = [i[1] for i in priorities]
        return priorities
    # if elements contain only numbers (version number), sort based on the digits after the last "."
    lst.sort(reverse=True, key=lambda x: x[x.rindex("."):])
    return lst
    


for i in all_groups:
    print('Page',i)
    for j in all_groups[i]:
        if len(j)>1:
            j = comp(j)  #first element in the printed list has the highest priority
        print("\t", j)
    print()