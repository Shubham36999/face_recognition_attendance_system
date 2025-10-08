"""
Face Recognition Attendance System - Image Capture Module with GUI
Captures labeled face images for training the recognition system
"""

import cv2
import os
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

def capture_for_label():
    """
    Capture face images with user-provided label
    Saves multiple images under known_faces/<label>/
    """
    root = tk.Tk()
    root.withdraw()  # hide the root window

    # Get user input for name label
    name = simpledialog.askstring("Input", "Enter the name for this person:")
    if not name or not name.strip():
        messagebox.showerror("Error", "Name cannot be empty!")
        return
    name = name.strip()

    # Create directory for this person
    person_dir = os.path.join("known_faces", name)
    os.makedirs(person_dir, exist_ok=True)

    # Initialize camera
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot access camera!")
            return
    except Exception as e:
        messagebox.showerror("Error", f"Camera initialization error: {e}")
        return

    print(f"📷 Capturing images for: {name}")
    print("Press SPACE to capture image, ESC to exit")

    image_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        # Overlay instructions
        cv2.putText(frame, f"Capturing for: {name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Images captured: {image_count}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press SPACE to capture, ESC to exit", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Show the frame
        cv2.imshow('Face Capture', frame)
        key = cv2.waitKey(1) & 0xFF

        # Capture image
        if key == ord(' '):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}_{image_count + 1}.jpg"
            filepath = os.path.join(person_dir, filename)
            cv2.imwrite(filepath, frame)
            image_count += 1
            print(f"✅ Captured image {image_count}: {filename}")

        # Exit with ESC
        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Done", f"Capture session completed! Saved {image_count} images for {name}")
    print(f"🎯 Capture session completed! Saved {image_count} images for {name}")


def list_known_faces():
    """List all known faces in the system"""
    known_faces_dir = "known_faces"
    if not os.path.exists(known_faces_dir):
        messagebox.showinfo("Info", "No known faces directory found")
        return

    people = [d for d in os.listdir(known_faces_dir)
              if os.path.isdir(os.path.join(known_faces_dir, d))]

    if not people:
        messagebox.showinfo("Info", "No people registered yet")
        return

    info = "\n".join(
        [f"{i+1}. {person} ({len([f for f in os.listdir(os.path.join(known_faces_dir, person)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])} images)"
         for i, person in enumerate(people)]
    )
    messagebox.showinfo("Known Faces", info)
    print("\n👥 Known people in the system:")
    print(info)


# ----------------- GUI MENU -----------------
def main_menu_gui():
    root = tk.Tk()
    root.withdraw()

    while True:
        choice = simpledialog.askstring("Menu",
            "🎭 Face Recognition Attendance System\n\n"
            "1. Capture new person\n"
            "2. List known faces\n"
            "3. Exit\n\n"
            "Enter choice (1-3):"
        )
        if choice is None:
            break
        choice = choice.strip()
        if choice == "1":
            capture_for_label()
        elif choice == "2":
            list_known_faces()
        elif choice == "3":
            messagebox.showinfo("Exit", "Goodbye!")
            break
        else:
            messagebox.showerror("Error", "Invalid choice. Please try again.")


# ----------------- MAIN -----------------
if __name__ == "__main__":
    main_menu_gui()
