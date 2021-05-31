import pdfplumber
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
import PyPDF2
import re
from collections import defaultdict
from difflib import SequenceMatcher
import requests
import urllib.request as urlreq
import os
import shutil
import download_script


#Compress the downloads folder
def zip_downloads():
    if os.path.exists(os.getcwd() + r"\package.zip"):
        os.remove(os.getcwd() + r"\package.zip")
    shutil.make_archive("package", 'zip', "downloads")

    # if os.path.exists(os.path.join(os.getcwd(), "package.zip")):
    #     os.remove(os.path.join(os.getcwd(), "package.zip"))
    # shutil.make_archive("package", 'zip', "downloads")


# Check if the url contains a downloadable resource
def is_downloadable(url):
    try:
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True
    except:
        print()

# Find the Drivers pages
def slice_pdf(file):
    pdf=pdfplumber.open("uploadedFiles" + r"\{}".format(file))

    links=[]
    for i in range(len(pdf.pages)):
        linkObjects=pdf.pages[i].hyperlinks
        for j in linkObjects:
            links.append(j["uri"])            
    
    print('\nNumber of links found in the PDF: ',len(links))

    sizes = []
    for i in range(len(pdf.pages)):
        p = pdf.pages[i]
        for word in p.extract_words(x_tolerance=3, y_tolerance=10, extra_attrs=['size']):
            if word['text']=='Drivers':
                sizes.append(word['size'])

    max_font = int(max(sizes))

    subheaders = []
    inDrivers = False

    for i in range(len(pdf.pages)):
        p = pdf.pages[i]
        val = ''
        for word in p.extract_words(x_tolerance=3, y_tolerance=10, extra_attrs=['size']):
            if word['size']==max_font:
                val = ' '.join([val, word['text']]).strip()
            else:
                if val != '':
                    subheaders.append(val)
                    if val == 'Drivers':
                        start_idx = i+1
                        inDrivers=True
                    if ((val!="Drivers") and (inDrivers)):
                        end_idx=i+1
                        inDrivers=False
                val = ''
    
    return start_idx-1, end_idx-1



# Group similar links together
def group(string, groups, pattern):
    if len(groups)==0:
      matched=re.search(pattern, string)
      if(bool(matched) == 1):
        groups.append([string.strip()])
        return     
    else:
        matched=re.search(pattern, string)
        if(bool(matched)==0):
            return
        else:
            pat=matched.group(0)
            pat=pat.replace('.', '\.')             
            for i in range(len(groups)):       
                check = re.search( pat, groups[i][0].strip().split("LINK_FOR_VER")[0])
                if ( (bool(check)==1) or (similar(string.strip().split("LINK_FOR_VER")[0], groups[i][0].strip().split("LINK_FOR_VER")[0]) > 0.85) ):
                    if(string.strip().split("LINK_FOR_VER")[0] not in [j.strip().split("LINK_FOR_VER")[0] for j in groups[i]]):   
                        #   [j.split(":")[0] for j in groups[i]]
                        groups[i].append(string.strip())
                        return 
            groups.append([string.strip()])


# String similarity
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Download packages
def download(url,logFile):
    if (url[url.rindex(".")+1:]=="zip" or url[url.rindex(".")+1:]=="exe") and  is_downloadable(url):
        filename = url[url.rindex('/')+1:]
        urlreq.urlretrieve(url, os.getcwd() + r"\downloads" + r"\{}".format(filename))

        logFile.write("\nDownloading "+url)
    else:
        download_script.download_from_url(url,logFile)


# Average of similarities between strings in a list
def get_list_similarity(lst):
    s = []
    for i in range(len(lst)):
        for j in lst[i+1:]:
            s.append(similar(lst[i],j))
    return sum(s)/len(s)

# Set priority
def pr(lst, spec):
    # spec = get_user_spec()
    flag = 0
    
    lst = [[i, i.split('LINK_FOR_VER')[0].strip()] for i in lst]
    for i in lst:
        if '(' in i[1]:
            i.append(i[1][:i[1].index('(')].strip())
            if ')' in i[1]:
                i.append(i[1][i[1].index('(')+1:i[1].index(')')].strip())
            else:
                i.append(i[1][i[1].index('(')+1:].strip())
        else:
            i.append(i[1])
            i.append('Windows 10')

    v_numbers = [i[3] for i in lst]
    sim = get_list_similarity(v_numbers)


    if sim>0.9:
        lst.sort(key=lambda x: x[2], reverse=True)
        #if lst[0][2] != lst[1][2]: #no repeated version numbers (ignoring the text inside braces)
        return [i[0] for i in lst], flag
    
    for i in lst:
        # sims = [similar(i[3].lower(),s.lower()) for s in spec] # METHOD 1
        # i.append(str(max(sims))) # METHOD 1
        if flag == 1:
            break
        if spec in i[3]:
            i.append("1")
            flag = 1

    for i in lst:
        if len(i)==4:
            i.append("0")
    
    # For example:
    # 0 - '2.30 (Microsoft Windows 2016) LINK_FOR_VERhttp://www.mellanox.com/downloads/WinOF/MLNX_WinOF2-2_30_50000_All_x64.exe'
    # 1 - '2.30 (Microsoft Windows 2016)'
    # 2 - '2.30'
    # 3 - 'Microsoft Windows 2016'
    # 4 - '1.0' (similarity or presence)

    lst.sort(key=lambda x: x[4], reverse=True) 
    res = [i[0] for i in lst]
    return res, flag


# Compare elements in one group (list)
def comp(lst, lst_spec):
    # If any element in the list contains a letter, use the above priorities function
    if any(re.search('[a-zA-Z]', ele.split("LINK_FOR_VER")[0]) for ele in lst): 
        prioritized, download = pr(lst, lst_spec)
        if not download:
            return prioritized,0
        return prioritized,1

    # If all elements contain only numbers (version number), sort based on the digits after the last "."
    lst.sort(reverse=True, key=lambda x: x[x.rindex("."):])
    return lst,1


def main(pdf_file, lst_spec):
    PDFFile_for_pypdf = open("uploadedFiles" + r"\{}".format(pdf_file),'rb')
    # PDFFile_for_pypdf = open(os.path.join(os.getcwd(), "uploadFiles", pdf_file), "rb")

    PDF_pypdf = PyPDF2.PdfFileReader(PDFFile_for_pypdf)
    key = '/Annots'
    uri = '/URI'
    ank = '/A'
    rect='/Rect'

    fp_for_pdfminer = open("uploadedFiles" + r"\{}".format(pdf_file), 'rb')
    # fp_for_pdfminer = open(os.path.join(os.getcwd(), "uploadFiles", pdf_file), "rb")

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages_for_pdf_miner = list(PDFPage.get_pages(fp_for_pdfminer))

    # start_idx = 18
    # end_idx = 18
    start_idx, end_idx = slice_pdf(pdf_file)

    page_contents = defaultdict(list)
    all_groups = defaultdict(list)

    for page in range(start_idx, end_idx+1):
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

        ##get text using pdfminer-----------------------------------------------------------------------------------------------------------
        interpreter.process_page(pages_for_pdf_miner[page])
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

        ##mapping-----------------------------------------------------------------------------------------------------------------------------
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

        page_contents[page] = final
        
        #Grouping------------------------------------------------------------------------------------------------------------------------------
        all_versions = "NEW_ROW".join(i[0]+"LINK_FOR_VER"+i[1] for i in final)
        pattern = "[0-9]+\.[0-9]+"
        groups = []
        T = [t.strip() for t in all_versions.split("NEW_ROW") if t]

        for i in range(len(T)):
            group(T[i], groups, pattern)
        all_groups[page] = groups




    # if ("downloads" not in os.listdir(os.getcwd())):
    #     os.mkdir(os.getcwd() + r"\downloads") 

    if ("downloads" in os.listdir(os.getcwd())):
        shutil.rmtree(os.getcwd() + r"\downloads", ignore_errors = False)
        # shutil.rmtree(os.join(os.getcwd(), "downloads"), ignore_errors = False)

    os.mkdir(os.getcwd() + r"\downloads") 
    # os.mkdir(os.join(os.getcwd(), "downloads"))

    if os.path.exists(os.getcwd() + r"\downloads" + r"\log.txt"):
        os.remove(os.getcwd() + r"\downloads" + r"\log.txt")
    logFile = open(os.getcwd() + r"\downloads" + r"\log.txt", "a") 

    # if os.path.exists(os.join(os.getcwd(), "downloads", "log.txt")):
    #     os.remove(os.join(os.getcwd(), "downloads", "log.txt"))
    # logFile = open(os.join(os.getcwd(), "downloads", "log.txt"), "a") 


    # download("https://www.mellanox.com/downloads/WinOF/MLNX_VPI_WinOF-5_50_54000_All_win2019_x64.exe", logFile)

    for i in all_groups.keys():
        print('Page',i+1)
        print('Links found:',sum([len(x) for x in all_groups[i]]))

        for j in all_groups[i]:
            j = [k.replace('\n','') for k in j]
            if len(j)>1:
                j,dl = comp(j, lst_spec) #first element has the highest priority
                print("\t", j)
                if dl == 1:
                    print("To download:",j[0].split("LINK_FOR_VER")[1])
                    download(j[0].split("LINK_FOR_VER")[1],logFile)
                else:
                    print("No matching URL for the specified OS :(")
            else:
                print("\t", j)
                print("To download:",j[0].split("LINK_FOR_VER")[1])
                download(j[0].split("LINK_FOR_VER")[1],logFile)
            print()            
        print()

    zip_downloads()

 
if __name__ == '__main__':
    main("file4.pdf")



