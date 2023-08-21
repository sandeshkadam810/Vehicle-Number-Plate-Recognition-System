import cv2

import imutils

import numpy as np

import pytesseract

import mysql.connector

from PIL import Image


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1587394w",
  database="mydatabase"
)

mycursor = mydb.cursor()

# Define a function to check if a number is present in the database
def number_exists(number):
    sql = "SELECT * FROM vehicles WHERE number = %s"
    val = (number,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return True
    else:
        return False
def store_number(number):
    sql = "INSERT INTO vehicles (number) VALUES (%s)"
    val = (number,)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Number", number, "stored in the database")

text='| HR26DK8337'
if number_exists('| HR26DK8337 '):
    print("Detected Number is:", text)
    print("Detected number is Present in the database")
else:
    print("Number not Present in database")