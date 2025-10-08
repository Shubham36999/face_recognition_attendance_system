# 📸 Face Recognition Attendance System

An intelligent Python-based system that automates attendance marking using **real-time face recognition**. This project captures and recognizes human faces through a webcam, compares them with stored images, and logs attendance automatically into a CSV file with timestamp and status.

---

##  Developers

| Name                 | Role                             |
| -------------------- | -------------------------------- |
| **Shubham Kulkarni** | Lead Developer                   |
| **Aditya Likhitkar** | AI/ML & Face Recognition         |
| **Gaurav Kosare**    | Data Handling & Attendance Logic |
| **Laxmikant Bhoskar** | GUI & Capture Module             |
| **Mayank Kene**      | System Integration & Testing     |

**Branch:** IIoT – 5th Semester

---

##  Project Overview

This project demonstrates how **AI-powered computer vision** can automate attendance management in real-world environments like classrooms or offices. The system detects and recognizes faces using OpenCV and DeepFace, maintaining a structured attendance record (`attendance.csv`) without manual intervention.

---

##  Key Features

 **Automatic Attendance Logging:** Marks attendance instantly upon recognition
 **Real-Time Face Detection:** Uses live webcam feed with OpenCV
 **Database of Known Faces:** Each user’s images stored separately under `known_faces/`
 **Threading Support:** Prevents GUI freezing during capture or recognition
n**Statistical Overview:** Displays total records, today’s attendance count, and last update
 **Manual Image Upload:** Add new face images directly via file upload
 **Safe Error Handling:** Handles camera, file, and data errors gracefully

---

##  System Requirements

| Requirement   | Description              |
| ------------- | ------------------------ |
| **Python**    | Version 3.8 or higher    |
| **OS**        | Windows, Linux, or macOS |
| **Camera**    | Built-in or USB webcam   |
| **RAM**       | Minimum 4GB recommended  |
| **Libraries** | See `requirements.txt`   |

---

##  Required Libraries

Your `requirements.txt` file should contain:

```
opencv-python
pandas
numpy
deepface
pillow
tk
```

To install all dependencies:

```bash
pip install -r requirements.txt
```

---

##  Folder Structure

```
face-recognition-attendance/
│
├── main.py                 # Main console menu and core logic
├── capture.py              # Face capture GUI (Tkinter + OpenCV)
├── recognize.py            # Recognition logic (DeepFace/OpenCV)
├── known_faces/            # Folder containing images per person
│   └── <Name>/             # Example: known_faces/Shubham/
│       ├── img1.jpg
│       └── img2.jpg
├── attendance.csv          # Auto-generated attendance log
├── requirements.txt        # Dependencies
├── LICENSE                 # MIT License
├── README.md               # Documentation
└── .gitignore              # Ignored files (venv, pycache, etc.)
```

---

##  Working Mechanism

### Step 1: **Face Capture**

* Run `main.py`
* Choose **Option 1: Capture New Person**
* A camera window opens to capture images for that person
* Captured images are saved in `known_faces/<name>/`

### Step 2: **Recognition & Attendance**

* Choose **Option 2: Recognize Person**
* The system loads all known faces
* When a face is detected and matched, it logs:

  * `Name`
  * `Date`
  * `Time`
  * `Status = Present`

### Step 3: **Data Storage**

* Each recognition session appends new entries to `attendance.csv`
* The file is readable in Excel or any CSV viewer

### Step 4: **Statistics & Management**

* **Option 4:** Displays total attendance records and today’s summary
* **Option 5:** Clears current day’s attendance data
* **Option 3:** Allows adding a photo manually for a person without capturing via webcam

---

##  How to Run

1. **Clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/face-recognition-attendance.git
   cd face-recognition-attendance
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application:**

   ```bash
   python main.py
   ```

4. **Use the console menu:**

| Option | Description                   |
| ------ | ----------------------------- |
| 1      | Capture new face images       |
| 2      | Recognize and mark attendance |
| 3      | Upload external image         |
| 4      | Show attendance statistics    |
| 5      | Clear today’s attendance      |
| 0      | Exit                          |

---

##  Example Attendance Output

| Name    | Date       | Time     | Status  |
| ------- | ---------- | -------- | ------- |
| Shubham | 2025-10-08 | 09:15:33 | Present |
| Aditya  | 2025-10-08 | 09:17:02 | Present |
| Gaurav  | 2025-10-08 | 09:18:49 | Present |

---

##  Attendance Statistics

When you choose **Option 4**, the console prints:

```
----- Attendance Stats -----
Total Records  : 35
Unique People  : 5
Today's Count  : 4
Latest Date    : 2025-10-08
----------------------------
```

---

##  Code Explanation (Simplified)

### `main.py`

Handles:

* Menu navigation
* Attendance file management
* Launching capture & recognition threads

### `capture.py`

* Captures multiple face images per person
* Stores under `known_faces/<name>`

### `recognize.py`

* Loads all known embeddings
* Uses DeepFace to compare faces
* Updates `attendance.csv` if a match is found

---

##  Troubleshooting Guide

| Issue                           | Cause                      | Solution                                      |
| ------------------------------- | -------------------------- | --------------------------------------------- |
| **Camera not accessible**       | Used by another app        | Close other camera apps, retry                |
| **No module named cv2**         | OpenCV not installed       | `pip install opencv-python`                   |
| **Empty attendance file**       | No recognized faces yet    | Ensure good lighting and correct angles       |
| **Unknown face not recognized** | Insufficient training data | Capture at least 5–10 clear images per person |

---

##  Security Tips

* Store `attendance.csv` in a secure directory if used in organizations.
* Avoid sharing `known_faces/` folder publicly.
* Regularly backup attendance logs.

---

##  Acknowledgments

Special thanks to:

* **OpenCV Community** – for providing efficient image processing libraries
* **DeepFace Framework** – for simplifying face recognition models
* **Pandas Team** – for enabling seamless data analysis
* **IIoT Department** – for project guidance and evaluation

---

##  Future Improvements

* Add a graphical dashboard for attendance visualization
* Enable cloud sync (Firebase or MongoDB)
* Integrate email/SMS notification for absentees
* Add mobile app for student/employee check-in

---

**Made with  by Team IIoT — Shubham, Aditya, Gaurav, Laxmikant & Mayank**

