import cv2
import pickle
import numpy as np
import os

# Initialize video capture and face detector
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Create the 'data' directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

def collect_faces(name, roll_no, dept_name):
    faces_data = []
    i = 0
    print(f"Collecting face data for {name}...")

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w, :]
            resized_img = cv2.resize(crop_img, (50, 50))
            if len(faces_data) <= 100 and i % 10 == 0:
                faces_data.append(resized_img)
            i += 1
            cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
        
        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1)
        if k == ord('q') or len(faces_data) == 100:
            break
    
    faces_data = np.asarray(faces_data)
    faces_data = faces_data.reshape(100, -1)
    
    # Save face data and user info (name, roll number, department)
    save_data(name, roll_no, dept_name, faces_data)
    print(f"Face data collection complete for {name}.")
    
    return

def save_data(name, roll_no, dept_name, faces_data):
    # Save names, faces_data, roll numbers, and department names
    if not os.path.exists('data/names.pkl'):
        names = [name] * 100
        roll_numbers = [roll_no] * 100
        dept_names = [dept_name] * 100
        with open('data/names.pkl', 'wb') as f:
            pickle.dump((names, roll_numbers, dept_names), f)
    else:
        with open('data/names.pkl', 'rb') as f:
            names, roll_numbers, dept_names = pickle.load(f)
        names += [name] * 100
        roll_numbers += [roll_no] * 100
        dept_names += [dept_name] * 100
        with open('data/names.pkl', 'wb') as f:
            pickle.dump((names, roll_numbers, dept_names), f)

    if not os.path.exists('data/faces_data.pkl'):
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(faces_data, f)
    else:
        with open('data/faces_data.pkl', 'rb') as f:
            faces = pickle.load(f)
        faces = np.append(faces, faces_data, axis=0)
        with open('data/faces_data.pkl', 'wb') as f:
            pickle.dump(faces, f)

def main():
    while True:
        name = input("Enter Your Name (or type 'exit' to stop): ")
        if name.lower() == 'exit':
            break
        
        roll_no = input("Enter Your Roll Number: ")
        dept_name = input("Enter Your Department Name: ")
        
        # Collect face data for the entered user
        collect_faces(name, roll_no, dept_name)
    
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
