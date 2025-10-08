import os
import shutil
import threading
from datetime import date
import pandas as pd
from capture import capture_for_label
from recognize import FaceRecognizer  # must be implemented separately
import cv2

UPLOAD_FOLDER = 'known_faces'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ATTENDANCE_FILE = "attendance.csv"


# ---------------- UTILITY FUNCTIONS -----------------
def get_attendance_data():
    """Load or initialize attendance CSV"""
    if not os.path.exists(ATTENDANCE_FILE):
        return pd.DataFrame(columns=['Name', 'Date', 'Time', 'Status'])
    try:
        df = pd.read_csv(ATTENDANCE_FILE)
        if {'Date', 'Time'}.issubset(df.columns):
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
            df = df.sort_values('DateTime', ascending=False)
            df = df.drop(columns=['DateTime'], errors='ignore')
        return df
    except Exception as e:
        print(f"[ERROR] Loading attendance data: {e}")
        return pd.DataFrame(columns=['Name', 'Date', 'Time', 'Status'])


def run_thread(func):
    """Run a function in a background thread without blocking UI"""
    thread = threading.Thread(target=func, daemon=True)
    thread.start()
    # Do NOT join here – allows non-blocking operation


# ---------------- CAMERA FUNCTIONS -----------------
def check_camera():
    """Check if camera can be accessed"""
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print("[ERROR] Cannot access camera!")
            return False
        cap.release()
        return True
    except Exception as e:
        print(f"[ERROR] Camera initialization failed: {e}")
        return False


# ---------------- MAIN OPERATIONS -----------------
def capture_person():
    """Capture face images for new or existing person"""
    if not check_camera():
        print("[ERROR] Camera not accessible. Please check your device.")
        return
    try:
        print("Starting image capture GUI...")
        run_thread(capture_for_label)
    except Exception as e:
        print(f"[ERROR] Capture failed: {e}")


def recognize_person():
    """Run live face recognition (non-GUI)"""
    if not check_camera():
        print("[ERROR] Camera not accessible. Please check your device.")
        return
    try:
        print("Starting recognition session...")
        recognizer = FaceRecognizer()
        recognizer.recognize_live_gui()
        print("Recognition session ended.")
    except Exception as e:
        print(f"[ERROR] Recognition failed: {e}")


def upload_image():
    """Upload external image into known_faces"""
    try:
        name = input("Enter person's name: ").strip()
        if not name:
            print("[ERROR] Name cannot be empty.")
            return

        file_path = input("Enter full image path: ").strip()
        if not os.path.isfile(file_path):
            print("[ERROR] File not found.")
            return

        ext = file_path.rsplit('.', 1)[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            print(f"[ERROR] Invalid file type. Allowed: {ALLOWED_EXTENSIONS}")
            return

        person_dir = os.path.join(UPLOAD_FOLDER, name)
        os.makedirs(person_dir, exist_ok=True)
        dest_path = os.path.join(person_dir, os.path.basename(file_path))
        shutil.copy(file_path, dest_path)
        print(f"[INFO] Image uploaded successfully for {name}")
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")


def show_stats():
    """Show attendance statistics summary"""
    df = get_attendance_data()
    today = date.today().strftime("%Y-%m-%d")

    total_records = len(df)
    unique_people = df['Name'].nunique() if not df.empty else 0
    today_records = len(df[df['Date'] == today]) if not df.empty else 0
    latest_date = df['Date'].max() if not df.empty else 'N/A'

    print("\n----- Attendance Stats -----")
    print(f"Total Records  : {total_records}")
    print(f"Unique People  : {unique_people}")
    print(f"Today's Count  : {today_records}")
    print(f"Latest Date    : {latest_date}")
    print("----------------------------\n")


def clear_today_attendance():
    """Clear today's attendance records"""
    try:
        df = get_attendance_data()
        today = date.today().strftime("%Y-%m-%d")
        if df.empty:
            print("[INFO] No attendance data to clear.")
            return
        df = df[df['Date'] != today]
        df.to_csv(ATTENDANCE_FILE, index=False)
        print("[INFO] Today's attendance cleared successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to clear today's data: {e}")


# ---------------- MAIN MENU -----------------
def main_menu():
    """Console-based main menu"""
    while True:
        print("\n=== Face Recognition Attendance System ===")
        print("1. Capture New Person")
        print("2. Recognize Person")
        print("3. Upload Image")
        print("4. Show Attendance Stats")
        print("5. Clear Today's Attendance")
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == '1':
            capture_person()
        elif choice == '2':
            recognize_person()
        elif choice == '3':
            upload_image()
        elif choice == '4':
            show_stats()
        elif choice == '5':
            clear_today_attendance()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("[ERROR] Invalid choice, please try again.")


if __name__ == '__main__':
    main_menu()
