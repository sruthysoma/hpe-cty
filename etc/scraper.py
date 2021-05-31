import pdfplumber
#from docx2pdf import convert

#convert("to_convert.docx", "converted.pdf")
pdf=pdfplumber.open(r"file.pdf")
# print(type(pdf.pages[0]))

# links=[]

page=pdf.pages[0]
print(page.hyperlinks[0])
print(page.hyperlinks[1])
print(page.hyperlinks)

# for i in range(len(pdf.pages)):
#     linkObjects=pdf.pages[i].hyperlinks
    
    # for j in linkObjects:
    #     if not j["uri"].startswith("mailto:"):
    #         links.append(j["uri"])
        

# #print(links)
# print('\nNumber of links found: ',len(links))

#print(links.index("https://downloadcenter.intel.com/download/29227/Chipset-INF-Utility"))

#OTHER LIBRARIES
#pypdf2 - did not detect all URLs
#pdfminer - needs some jdk functionality to run (JDK)

#SHORTCOMINGS
#Works only for machine generated links - explicitly link text to a URL
#Does not recognize text from a scanned PDF 


subheaders = []
inDrivers=False
for i in range(len(pdf.pages)):
    p = pdf.pages[i]
    val = ''
    for word in p.extract_words(x_tolerance=3, y_tolerance=10, extra_attrs=['size']):
        if word['size']==18:
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
                   #print(i)
            val = ''

print("'Drivers' subheading found on page: ",start_idx)
print("Drivers section ends at page: ", end_idx)
print()


# # print(subheaders)

# for i in range(start_idx, end_idx+1):
#     p = pdf.pages[i]
#     table = p.extract_table(table_settings={"vertical_strategy": "text", 
#                                          "horizontal_strategy": "lines", 
#                                          "snap_tolerance": 4,})
#     print(table)

# print(tables)
#NEXT STEP
#extract links using plumber - from drivers subheading, until we find text whose fontsize is greater than or equal to that of drivers

#If hardcoded fontsize is not reliable, we can find the largest "drivers", and use its fontsize