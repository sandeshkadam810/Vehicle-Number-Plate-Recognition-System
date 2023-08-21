import cv2

import imutils

import numpy as np

import pytesseract

import serial

import mysql.connector


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Establish serial connection
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with the correct port name
def move_servo(angle):
    command = str(angle) + '\n'  # Convert angle to string and add newline character
    ser.write(command.encode()) 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1587394w",
  database="mydatabase"
)

mycursor = mydb.cursor(buffered=True)

# Define a function to check if a number is present in the database
def number_exists(number):
    sql = "SELECT * FROM vehicles WHERE number = %s"
    valchar = (number,)
    mycursor.execute(sql, valchar)
    result = mycursor.fetchone()
    if result:
        return True
    else:
        return False


def recognize_number_plate(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(image, image, mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

        text = pytesseract.image_to_string(cropped, config='--psm 11')
        print("Detected Number is:", text)

        if number_exists(text):
         print("Detected number is Present in the database")

         # Move the servo to 90 degrees
         move_servo(90)

        else:
            print("Number not Present in database")

        

    return image

# Initialize the video capture object
cap = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Failed to capture frame")
        break

    # Recognize number plates in the frame
    result_frame = recognize_number_plate(frame)


    # Display the resulting frame
    cv2.imshow("Number Plate Recognition", result_frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()