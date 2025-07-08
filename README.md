# Attendance Automation using Face Detection 🤖📸

## Introduction

This project implements an attendance automation system using face detection. The system utilizes computer vision techniques, Firebase Realtime Database, and Firebase Storage to manage student information, attendance records, and images.

## Features

- **Face Detection**: Utilizes the `face_recognition` library to detect faces in the webcam feed. 🧑‍💻
- **Firebase Integration**: Connects to Firebase Realtime Database and Firebase Storage to store student data and images. ☁️
- **Attendance Portal**: Displays an interactive attendance portal with real-time face recognition. 🗂️
- **GUI**: Basic Tkinter-based GUI to enter data into the database. 🖥️
- **Lighting**: Works in low-light conditions. 🌟

## Requirements

Ensure you have the following dependencies installed:

- In Windows machines, download Visual Studio with Development in C++ to successfully install these libraries.
- `firebase-admin==5.0.1`
- `opencv-python==4.5.3`
- `cvzone==1.5.3`
- `face-recognition==1.3.0`
- `numpy==1.21.2`
- `Pillow==8.3.2`

You can install them using:

```bash
pip install -r requirements.txt
```

## Usage
**Firebase Configuration**
1.Add your Firebase service account key (JSON) to the project. 🔑
2.Update the Firebase Realtime Database and Storage URLs in the code. 🌐

**Run Database Maker**
```bash
python databaseMaker.py
```
If you want to initialize the database with the provided data, run the databaseMaker.py file. 📚

**Run Admin Portal**
```bash
python adminPortal.py
```
Use the Admin Portal to add additional student data. Upload student images through the portal. 📷

**Run Encodings Generator**
```bash
python encode.py
```
Generate face encodings based on the uploaded images. 🧩

**Run Main Script**
```bash
python main.py
```
Execute the main script to start the attendance automation system. 🚀

## Acknowledgments
This project utilizes the face_recognition library by Adam Geitgey. Special thanks to the author and contributors for providing an excellent face recognition tool. 

## Contributing
Feel free to contribute to the project by opening issues or submitting pull requests.

## License
This project is licensed under the MIT License. 📜



