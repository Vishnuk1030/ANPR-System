import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import pytesseract
import re
import mysql.connector

mydb = mysql.connector.connect(
     host="localhost",
     user="root",
    passwd="",
     database="test"
 )
import os
for i in os.listdir("Dataset"):
    for images in os.listdir(r"D:\project\collegeproject-main\collegeproject-main\camera\Datasett"):
        print(images)
    img = cv2.imread("Dataset/"+i)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))



    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]



    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break



    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)



    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    text = pytesseract.image_to_string(cropped_image, lang='eng')
    text = str(text.upper().replace(" ", ""))
    text = re.sub("[^A-Z0-9]+", "", text)
    print(text)
     mycursor = mydb.cursor()
     if text != "None":
         mycursor.execute("update findV set Latitude = '9.854980',Longitude = '78.500504' where Vehno = %s", (text))
         mycursor.execute("insert into findBlock(Vehno,Location,latitude,longitude) values(%s,'Bangalore','9.854980','78.500504');",(text,))
     else:
         print("No number plate detected")
