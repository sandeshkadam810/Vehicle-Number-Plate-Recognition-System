import cv2

import imutils

import numpy as np

import pytesseract

from PIL import Image

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1587394w",
  database="mydatabase"
)


mycursor = mydb.cursor(buffered=True)


def store_number(number):
    sql = "INSERT INTO vehicles (number) VALUES (%s)"
    val = (number,)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Number", number, "stored in the database")

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('C:/Users/SANDESH/Documents/psap c/VS Code programs/EDAI2/4.jpeg',cv2.IMREAD_COLOR)


img = cv2.resize(img, (620,480) )



gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.bilateralFilter(gray, 11, 17, 17) 

edged = cv2.Canny(gray, 30, 200) 



cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnts = imutils.grab_contours(cnts)

cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

screenCnt = None



for c in cnts:



 peri = cv2.arcLength(c, True)

 approx = cv2.approxPolyDP(c, 0.018 * peri, True)

 



 if len(approx) == 4:

  screenCnt = approx

  break


 


if screenCnt is None:

 detected = 0

 print ("No contour detected")

else:

 detected = 1


if detected == 1:

 cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)


mask = np.zeros(gray.shape,np.uint8)

new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)

new_image = cv2.bitwise_and(img,img,mask=mask)


(x, y) = np.where(mask == 255)

(topx, topy) = (np.min(x), np.min(y))

(bottomx, bottomy) = (np.max(x), np.max(y))

Cropped = gray[topx:bottomx+1, topy:bottomy+1]



text = pytesseract.image_to_string(Cropped, config='--psm 11')

print("Detected Number is:",text)


def store_number(number):
    sql = "INSERT INTO vehicles (number) VALUES (%s)"
    val = (number,)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Number", number, "stored in the database")

#store_number(text)
cv2.imshow('image',img)

cv2.imshow('Cropped',Cropped)


cv2.waitKey(0)

cv2.destroyAllWindows()
