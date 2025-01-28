Overview
FaceTrack is a real-time attendance management system using facial recognition. It simplifies the attendance process by leveraging computer vision and machine learning technologies. This project automates attendance marking, minimizes human errors, and provides a user-friendly interface for educators.

Features:
-Real-Time Facial Recognition: Uses OpenCV and machine learning models for efficient and accurate detection.
 Automated Attendance Logging: Stores attendance records securely with timestamps.
-User-Friendly Interface: Built with Streamlit for seamless interaction.
-Scalable Solution: Suitable for various classroom sizes and adaptable to educational institutions and corporate training 
 programs.
-Reports and Analytics: Generates detailed attendance reports in CSV/PDF formats.

Technologies Used:
-Programming Language: Python 3.8+
-Libraries: OpenCV, Scikit-learn, Streamlit, Pandas, NumPy
-Database: SQLite
-Models and Algorithms: K-Nearest Neighbors (KNN) and Haar Cascades
-Frontend: Streamlit

System Requirements:
-Software Requirements
   -Python 3.8+
   -Required Python Libraries: Install using pip install -r requirements.txt
-Hardware Requirements
   -Standard Webcam (720p or 1080p)
   -Computer with Intel i3 or higher and 4GB+ RAM
   
Installation:
1.Clone the repository:
git clone https://github.com/PrashanthVurugonda/Face_recognition_attendance.git cd Face_recognition_attendance

2.Install the required dependencies:
pip install -r requirements.txt

3.Run the application:
streamlit run app.py

Usage:
1.Admin: Register users (students/teachers) and capture face data.
2.Teachers: Monitor live attendance and generate reports.
3.Students: View attendance status and submit appeals for corrections.

Modules:
1.Face Registration: Collects and stores facial data of students.
2.Real-Time Detection: Identifies faces from live webcam feed.
3.Attendance Management: Logs attendance automatically in a secure database.
4.Reports: Provides attendance summaries and analytics.

Testing:
-Unit testing for individual modules (face detection, database logging, etc.).
-Integration testing to ensure seamless interaction between components.
-User Acceptance Testing (UAT) for usability validation.

Future Enhancements:
-Improve accuracy in low-light conditions.
-Integrate voice recognition for added security.
-Enable remote monitoring for teachers via cloud-based databases.

Authors:
1.Kamuni Amulya Sri. 
2.Vurugonda Prashanth.

License:
This project is licensed under the MIT License - see the LICENSE file for details.
