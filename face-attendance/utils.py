
"""
Face Recognition Attendance System - Utility Functions
Additional tools for system management and testing
"""

import os
import pandas as pd
import shutil
from datetime import datetime, date
import cv2

def clear_all_data():
    """Clear all attendance and face data (use with caution)"""
    print("⚠️  WARNING: This will delete ALL attendance and face data!")
    confirm = input("Type 'YES' to confirm: ")

    if confirm != "YES":
        print("❌ Operation cancelled")
        return

    # Remove attendance file
    if os.path.exists("attendance.csv"):
        os.remove("attendance.csv")
        print("✅ Deleted attendance.csv")

    # Remove known_faces directory
    if os.path.exists("known_faces"):
        shutil.rmtree("known_faces")
        print("✅ Deleted known_faces directory")

    print("🗑️  All data cleared successfully!")

def backup_data():
    """Create a backup of all attendance and face data"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"

    os.makedirs(backup_dir, exist_ok=True)

    # Backup attendance file
    if os.path.exists("attendance.csv"):
        shutil.copy2("attendance.csv", os.path.join(backup_dir, "attendance.csv"))
        print(f"✅ Backed up attendance.csv to {backup_dir}")

    # Backup known faces
    if os.path.exists("known_faces"):
        shutil.copytree("known_faces", os.path.join(backup_dir, "known_faces"))
        print(f"✅ Backed up known_faces to {backup_dir}")

    print(f"💾 Backup completed: {backup_dir}")

def generate_report():
    """Generate a detailed attendance report"""
    if not os.path.exists("attendance.csv"):
        print("❌ No attendance data found!")
        return

    df = pd.read_csv("attendance.csv")

    print("\n📊 ATTENDANCE REPORT")
    print("=" * 50)

    # Basic statistics
    total_records = len(df)
    unique_people = df['Name'].nunique()
    date_range = f"{df['Date'].min()} to {df['Date'].max()}"

    print(f"Total Records: {total_records}")
    print(f"Unique People: {unique_people}")
    print(f"Date Range: {date_range}")

    # Today's attendance
    today = date.today().strftime("%Y-%m-%d")
    today_records = df[df['Date'] == today]
    print(f"Today's Attendance: {len(today_records)}")

    # Most frequent attendees
    print("\n🏆 Most Frequent Attendees:")
    frequent = df['Name'].value_counts().head(5)
    for i, (name, count) in enumerate(frequent.items(), 1):
        print(f"{i}. {name}: {count} days")

    # Recent activity
    print("\n🕒 Recent Activity (Last 5 records):")
    recent = df.tail(5)
    for _, record in recent.iterrows():
        print(f"- {record['Name']} on {record['Date']} at {record['Time']}")

def test_camera():
    """Test camera functionality"""
    print("📹 Testing camera...")

    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Cannot access camera!")
            return False

        print("✅ Camera accessible")
        print("Press any key to capture test image, ESC to exit")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to grab frame")
                break

            cv2.putText(frame, "Camera Test - Press any key", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Camera Test', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key != 255:  # Any other key
                cv2.imwrite(f"test_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg", frame)
                print("✅ Test image captured")
                break

        cap.release()
        cv2.destroyAllWindows()
        print("📹 Camera test completed")
        return True

    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

def list_system_info():
    """Display system information and status"""
    print("\n🖥️  SYSTEM INFORMATION")
    print("=" * 50)

    # Check directories
    if os.path.exists("known_faces"):
        people = [d for d in os.listdir("known_faces") 
                  if os.path.isdir(os.path.join("known_faces", d))]
        print(f"Known People: {len(people)}")
        for person in people:
            person_dir = os.path.join("known_faces", person)
            image_count = len([f for f in os.listdir(person_dir) 
                              if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            print(f"  - {person}: {image_count} images")
    else:
        print("Known People: 0 (no directory)")

    # Check attendance file
    if os.path.exists("attendance.csv"):
        df = pd.read_csv("attendance.csv")
        print(f"Attendance Records: {len(df)}")
        print(f"File Size: {os.path.getsize('attendance.csv')} bytes")
    else:
        print("Attendance Records: 0 (no file)")

    # Check dependencies
    try:
        import cv2
        print(f"OpenCV Version: {cv2.__version__}")
    except ImportError:
        print("OpenCV: Not installed")

    try:
        import deepface
        print("DeepFace: Installed")
    except ImportError:
        print("DeepFace: Not installed")

    try:
        import flask
        print(f"Flask Version: {flask.__version__}")
    except ImportError:
        print("Flask: Not installed")

if __name__ == "__main__":
    print("🛠️  Face Recognition Attendance System - Utilities")
    print("=" * 60)

    while True:
        print("\n📋 Available Tools:")
        print("1. System Information")
        print("2. Generate Report") 
        print("3. Test Camera")
        print("4. Backup Data")
        print("5. Clear All Data")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            list_system_info()
        elif choice == "2":
            generate_report()
        elif choice == "3":
            test_camera()
        elif choice == "4":
            backup_data()
        elif choice == "5":
            clear_all_data()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
