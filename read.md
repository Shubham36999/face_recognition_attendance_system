# Face Recognition Attendance System

**Developer/Author:** Shubham Kulkarni, Aditya Likhitkar, Gaurav Kosare, Laxmikan Bhoskar, Mayank Kene  
**Branch:** IIoT (5th Sem)

---

## Overview
A Python-based console application for real-time face recognition attendance management.  
This system allows you to:
- Capture new persons via camera
- Recognize faces in real-time
- Upload images for known persons
- View attendance statistics
- Clear today's attendance records

---

## Features
- Non-blocking camera operations using threads
- Attendance tracking with CSV storage
- Real-time face recognition GUI (requires `FaceRecognizer` implementation)
- Image upload support (`png`, `jpg`, `jpeg`)

---

## Requirements

Python 3.9+ is recommended. Install dependencies via:

```bash
pip install -r requirements.txt

Structure
face-recognition-attendance/
│
├── capture.py                 # Capturing face images for new persons
├── recognize.py               # Face recognition logic
├── main.py                    # The code you provided (main menu)
├── requirements.txt           # Required Python libraries
├── attendance.csv             # Attendance records (auto-created)
├── known_faces/               # Folder to store captured/ uploaded images
│
└── README.md                  # Project documentation
