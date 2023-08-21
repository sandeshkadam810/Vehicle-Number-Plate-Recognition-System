import serial
import time

# Establish serial connection
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with the correct port name
# Wait for the connection to be established
time.sleep(2)

# Function to control the servo motor
def move_servo(angle):
    command = str(angle) + '\n'  # Convert angle to string and add newline character
    ser.write(command.encode())  # Send the command to Arduino

# Move the servo to 0 degrees
move_servo(90)
