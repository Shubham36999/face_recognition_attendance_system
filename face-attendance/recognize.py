"""
Face Recognition Attendance System - Recognition Module with Camera GUI
Real-time face recognition and attendance marking
"""

import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime, date
from deepface import DeepFace
import tkinter as tk
from tkinter import messagebox
import pickle
from PIL import Image, ImageTk

# Configuration
TOLERANCE = 0.6  # Similarity threshold
ATTENDANCE_FILE = "attendance.csv"
EMBEDDINGS_FILE = "embeddings.pkl"


class FaceRecognizer:
    def __init__(self):
        self.known_face_embeddings = {}
        self.known_face_names = []
        self.attendance_marked_today = set()
        self.load_attendance_data()
        self.load_known_faces()

    # ----------------- Load Precomputed Embeddings -----------------
    def load_known_faces(self):
        if os.path.exists(EMBEDDINGS_FILE):
            with open(EMBEDDINGS_FILE, "rb") as f:
                self.known_face_embeddings = pickle.load(f)
            self.known_face_names = list(self.known_face_embeddings.keys())
            print(f"✅ Loaded {len(self.known_face_names)} people from precomputed embeddings")
            return True
        else:
            print("⚠️ No precomputed embeddings found. Run precompute_embeddings() first.")
            return False

    def cosine_similarity(self, embedding1, embedding2):
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        if norm1 == 0 or norm2 == 0:
            return 0
        return dot_product / (norm1 * norm2)

    def recognize_face(self, face_image):
        try:
            embedding = DeepFace.represent(face_image, model_name='VGG-Face', enforce_detection=False)
            if not embedding or len(embedding) == 0:
                return None, 0
            face_embedding = embedding[0]["embedding"]

            best_match = None
            highest_similarity = 0

            for name, known_embedding in self.known_face_embeddings.items():
                similarity = self.cosine_similarity(face_embedding, known_embedding)
                if similarity > highest_similarity and similarity > TOLERANCE:
                    highest_similarity = similarity
                    best_match = name

            return best_match, highest_similarity
        except Exception as e:
            print(f"❌ Recognition error: {e}")
            return None, 0

    # ----------------- Attendance Functions -----------------
    def load_attendance_data(self):
        today = date.today().strftime("%Y-%m-%d")
        if os.path.exists(ATTENDANCE_FILE):
            try:
                df = pd.read_csv(ATTENDANCE_FILE)
                today_records = df[df['Date'] == today]
                self.attendance_marked_today = set(today_records['Name'].tolist())
                print(f"📅 Loaded attendance data. {len(self.attendance_marked_today)} people already marked today.")
            except Exception as e:
                print(f"⚠️  Could not load attendance data: {e}")
                self.attendance_marked_today = set()
        else:
            self.attendance_marked_today = set()

    def mark_attendance(self, name):
        if name in self.attendance_marked_today:
            return False
        self.attendance_marked_today.add(name)
        now = datetime.now()
        data = {'Name': name, 'Date': now.strftime("%Y-%m-%d"),
                'Time': now.strftime("%H:%M:%S"), 'Status': 'Present'}
        try:
            if os.path.exists(ATTENDANCE_FILE):
                df = pd.read_csv(ATTENDANCE_FILE)
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            else:
                df = pd.DataFrame([data])
            df.to_csv(ATTENDANCE_FILE, index=False)
            print(f"✅ Attendance marked for {name} at {data['Time']}")
            return True
        except Exception as e:
            print(f"❌ Could not save attendance: {e}")
            return False

    # ----------------- GUI Recognition -----------------
    def recognize_live_gui(self):
        if not self.known_face_names:
            messagebox.showerror("Error", "No known faces loaded! Precompute embeddings first.")
            return

        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot access camera!")
            return

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Tkinter window
        self.root = tk.Tk()
        self.root.title("Face Recognition Attendance System")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        self.info_label = tk.Label(self.root, text=f"Known faces: {len(self.known_face_names)} | Today: {len(self.attendance_marked_today)}", font=("Helvetica", 12))
        self.info_label.pack()

        self.update_frame()
        self.root.mainloop()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.root.after(10, self.update_frame)
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            face_image = rgb_frame[y:y+h, x:x+w]
            name, confidence = self.recognize_face(face_image)
            if name:
                color = (0, 255, 0)
                label = f"{name} ({confidence:.2f})"
                self.mark_attendance(name)
            else:
                color = (0, 0, 255)
                label = "Unknown"
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        self.info_label.config(text=f"Known faces: {len(self.known_face_names)} | Today: {len(self.attendance_marked_today)}")

        # Convert OpenCV image to Tkinter PhotoImage
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

        self.root.after(10, self.update_frame)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()
        messagebox.showinfo("Session Ended", f"Total attendance today: {len(self.attendance_marked_today)}")


# ----------------- MAIN -----------------
if __name__ == "__main__":
    recognizer = FaceRecognizer()
    recognizer.recognize_live_gui()
