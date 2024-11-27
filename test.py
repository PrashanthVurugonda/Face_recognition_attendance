from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# Initialize video capture and face detector
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load labels and faces
with open('data/names.pkl', 'rb') as w:
    names, roll_numbers, dept_names = pickle.load(w)  # Unpack names, roll numbers, and department names
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

# Train KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, names)  # Train with face data and corresponding names

# Load background image
imgBackground = cv2.imread("background.png")

# Define column names for CSV
COL_NAMES = ['NAME', 'ROLL_NO', 'DEPT_NAME', 'TIME']

# Ensure Attendance folder exists
if not os.path.exists("Attendance"):
    os.makedirs("Attendance")

# Set countdown duration
countdown_duration = 10
countdown_time = countdown_duration
countdown_started = False  # Start countdown only when a face is detected
detected_name = None  # Variable to hold the detected name

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Capture and process each detected face
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)

        # Get the current timestamp for attendance
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        file_path = f"Attendance/Attendance_{date}.csv"
        file_exists = os.path.isfile(file_path)

        # Find index of detected name to retrieve roll number and department
        detected_name = output[0]
        name_index = names.index(detected_name)
        roll_no = roll_numbers[name_index]
        dept_name = dept_names[name_index]

        # Prepare the attendance entry
        attendance = [detected_name, roll_no, dept_name, timestamp]

        # Draw rectangle and display name on frame for each face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, detected_name, (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        # Insert the detected face into the background image
        imgBackground[162:162 + 480, 55:55 + 640] = frame

        # Start countdown when a face is detected
        countdown_started = True

    # Countdown logic
    if countdown_started:
        countdown_time -= 1 / 30  # Assuming ~30 FPS
        if countdown_time <= 0 and detected_name is not None:
            speak(f"Attendance taken for {detected_name}")
            with open(file_path, mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(COL_NAMES)  # Write header if file is new
                writer.writerow(attendance)   # Write the attendance data
            time.sleep(3)  # Wait for 3 seconds before continuing
            countdown_time = countdown_duration  # Reset countdown time for next attendance
            countdown_started = False  # Reset countdown flag

    # Display the frame with the detected faces and background
    cv2.imshow("Frame", imgBackground)

    # Check for key presses
    key = cv2.waitKey(1)

    if key == ord('o') and detected_name is not None:
        # Take attendance when 'o' is pressed
        speak(f"Attendance taken for {detected_name}")

        with open(file_path, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(COL_NAMES)  # Write header if file is new
            writer.writerow(attendance)   # Write the attendance data
        time.sleep(3)  # Wait for 3 seconds before continuing

    elif key == ord('q'):
        # Exit the system when 'q' is pressed
        break

# Release video capture and close all windows
video.release()
cv2.destroyAllWindows()
