# from pdf2image import convert_from_path
 
 
# # Store Pdf with convert_from_path function
# images = convert_from_path('file3.pdf')
 
# for i in range(len(images)):
   
#       # Save pages as images in the pdf
#     images[i].save('page'+ str(i) +'.jpg', 'JPEG')

import cv2

image = cv2.imread('page15.jpg')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,1))
detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    cv2.drawContours(image, [c], -1, (36,255,12), 3)

cv2.imshow('thresh', thresh)
cv2.imshow('detected_lines', detected_lines)
cv2.imshow('image', image)
cv2.waitKey()