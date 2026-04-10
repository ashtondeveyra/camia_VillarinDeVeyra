import tkinter as tk
from tkinter import messagebox, ttk
import qrcode
import json
import os
from PIL import Image
import cv2
from datetime import datetime
import csv
import time
import re

# ---------------- SETTINGS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = "my_secret_key_123"
SCAN_DELAY = 2  # seconds

PASSWORD_FILE = os.path.join(BASE_DIR, "admin_password.txt")

# ✅ NEW: Folders for organization
IMAGE_BASE_DIR = os.path.join(BASE_DIR, "attendance_images")
REPORTS_DIR = os.path.join(BASE_DIR, "attendance_reports")

# Load password from file
def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            return f.read().strip()
    else:
        with open(PASSWORD_FILE, "w") as f:
            f.write("admin123")
        return "admin123"

# Save password to file
def save_password(password):
    with open(PASSWORD_FILE, "w") as f:
        f.write(password)

ADMIN_PASSWORD = load_password()
is_admin = False

# Global Variables:
last_scan_time = 0
scan_count = 0
scanned_students = set()
attendance_records = []
start_time = datetime.now()

# Target attendance time
TARGET_HOUR = 7
TARGET_MINUTE = 30

# Snapshot Function
def save_snapshot(frame, name):
    today = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(IMAGE_BASE_DIR, today)

    os.makedirs(folder_path, exist_ok=True)

    safe_name = name.replace(" ", "_")
    filename = f"{safe_name}.jpg"
    filepath = os.path.join(folder_path, filename)

    cv2.imwrite(filepath, frame)

# ---------------- FUNCTIONS ----------------
def get_time_status_and_time():
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")

    current_minutes = now.hour * 60 + now.minute
    target_minutes = TARGET_HOUR * 60 + TARGET_MINUTE
    diff = current_minutes - target_minutes

    if diff < 0:
        status = "Early"
    elif diff == 0:
        status = "On time"
    else:
        if diff < 10:
            status = "Late (No Admission Slip required)"
        else:
            status = "Late (Admission Slip required)"

    return time_str, status

def filter_table(*args):
    query = search_var.get().lower()

    for item in attendance_table.get_children():
        attendance_table.delete(item)

    for i, record in enumerate(attendance_records, start=1):
        if query in record["name"].lower():
            attendance_table.insert(
                "",
                "end",
                values=(i, record["name"], record["time"], record["status"]),
                tags=(record["status"],)
            )

def register_student(name, frame):
    global scan_count

    if datetime.now() < start_time:
        messagebox.showwarning(
            "System Time Changed",
            "System time appears to have been modified.\n\nAttendance may not be accurate."
        )

    if name in scanned_students:
        messagebox.showwarning("Already Scanned", f"Attendance already recorded for {name}.")
        return

    scanned_students.add(name)
    scan_count += 1

    # SAVE SNAPSHOT
    save_snapshot(frame, name)

    time_str, status = get_time_status_and_time()

    attendance_records.append({
        "name": name,
        "time": time_str,
        "status": status
    })

    attendance_table.insert(
        "",
        "end",
        values=(scan_count, name, time_str, status),
        tags=(status,)
    )

    if status == "Early":
        attendance_table.tag_configure("Early", foreground="blue")
    elif status == "On time":
        attendance_table.tag_configure("On time", foreground="green")
    elif "No Admission Slip required" in status:
        attendance_table.tag_configure("Late (No Admission Slip required)", foreground="orange")
    elif "Admission Slip required" in status:
        attendance_table.tag_configure("Late (Admission Slip required)", foreground="red")

# ---------------- PROMPT ----------------
def simple_prompt(prompt_text):
    top = tk.Toplevel(root)
    top.title(prompt_text)

    tk.Label(top, text=prompt_text).pack(padx=10, pady=5)
    entry = tk.Entry(top, width=40, show="*" if "Password" in prompt_text else "")
    entry.pack(padx=10, pady=5)

    result = {"value": None}

    def submit():
        result["value"] = entry.get().strip()
        top.destroy()

    tk.Button(top, text="Submit", command=submit).pack(pady=5)
    root.wait_window(top)
    return result["value"]

# ---------------- ADMIN FUNCTIONS ----------------
def show_admin_buttons():
    login_btn.pack_forget()
    change_pass_btn.pack_forget()
    update_btn.pack(pady=2)
    delete_btn.pack(pady=2)
    logout_btn.pack(pady=2)

def hide_admin_buttons():
    update_btn.pack_forget()
    delete_btn.pack_forget()
    logout_btn.pack_forget()
    login_btn.pack(pady=2)
    change_pass_btn.pack(pady=2)

def admin_login():
    global is_admin
    password = simple_prompt("Enter Admin Password:")

    if password is None:
        return

    if password == ADMIN_PASSWORD:
        is_admin = True
        messagebox.showinfo("Access Granted", "Admin mode enabled.")
        show_admin_buttons()
    else:
        messagebox.showerror("Access Denied", "Incorrect password.")

def admin_logout():
    global is_admin

    if not is_admin:
        messagebox.showinfo("Admin Mode", "You are not in admin mode.")
        return

    is_admin = False
    hide_admin_buttons()
    messagebox.showinfo("Logged Out", "Admin mode disabled.")

def change_password():
    global ADMIN_PASSWORD

    current = simple_prompt("Enter Current Password:")
    if current is None:
        return

    if current != ADMIN_PASSWORD:
        messagebox.showerror("Error", "Incorrect current password.")
        return

    new_pass = simple_prompt("Enter New Password:")
    if new_pass is None or new_pass.strip() == "":
        messagebox.showwarning("Invalid Input", "Password cannot be empty.")
        return

    confirm_pass = simple_prompt("Confirm New Password:")
    if confirm_pass != new_pass:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    ADMIN_PASSWORD = new_pass
    save_password(new_pass)
    messagebox.showinfo("Success", "Password changed successfully.")

def get_selected_index():
    selected = attendance_table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a record first.")
        return None

    item = attendance_table.item(selected[0])
    index = int(item["values"][0]) - 1
    return index

def refresh_table():
    for item in attendance_table.get_children():
        attendance_table.delete(item)

    for i, record in enumerate(attendance_records, start=1):
        attendance_table.insert(
            "",
            "end",
            values=(i, record["name"], record["time"], record["status"]),
            tags=(record["status"],)
        )

def delete_record():
    global scan_count

    index = get_selected_index()
    if index is None:
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if not confirm:
        return

    name = attendance_records[index]["name"]
    if name in scanned_students:
        scanned_students.remove(name)

    del attendance_records[index]
    scan_count = len(attendance_records)
    refresh_table()

def update_record():
    index = get_selected_index()
    if index is None:
        return

    record = attendance_records[index]

    top = tk.Toplevel(root)
    top.title("Update Record")

    tk.Label(top, text="Update Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(top, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    name_entry.insert(0, record["name"])

    tk.Label(top, text="Update Time (HH:MM AM/PM):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    time_entry = tk.Entry(top, width=30, fg="gray")
    time_entry.grid(row=1, column=1, padx=10, pady=5)
    placeholder = "Ex: 07:30 AM"
    time_entry.insert(0, placeholder)

    def on_focus_in(event):
        if time_entry.get() == placeholder:
            time_entry.delete(0, tk.END)
            time_entry.config(fg="black")
    time_entry.bind("<FocusIn>", on_focus_in)

    tk.Label(top, text="Update Status:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    status_var = tk.StringVar(value=record["status"])
    status_options = ["Early", "On time", "Late (No Admission Slip required)", "Late (Admission Slip required)"]
    status_menu = ttk.Combobox(top, textvariable=status_var, values=status_options, state="readonly", width=28)
    status_menu.grid(row=2, column=1, padx=10, pady=5)

    def submit_update():
        new_name = name_entry.get().strip()
        new_time = time_entry.get().strip()
        new_status = status_var.get().strip()

        if not re.fullmatch(r"[A-Za-z.,\s]+", new_name):
            messagebox.showwarning("Invalid Input", "Name must contain letters only.")
            return

        if new_time == "" or new_time == placeholder:
            new_time = record["time"]
        else:
            if not re.fullmatch(r"(0[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)", new_time, re.IGNORECASE):
                messagebox.showwarning("Invalid Input", "Time must be in HH:MM AM/PM format.")
                return

        if new_status not in status_options:
            messagebox.showwarning("Invalid Input", "Please select a valid status.")
            return

        old_name = record["name"]
        if old_name in scanned_students:
            scanned_students.remove(old_name)
        scanned_students.add(new_name)

        record["name"] = new_name
        record["time"] = new_time
        record["status"] = new_status

        selected_item = attendance_table.selection()[0]
        attendance_table.item(selected_item, values=(index + 1, new_name, new_time, new_status))

        if new_status == "Early":
            attendance_table.item(selected_item, tags=("Early",))
            attendance_table.tag_configure("Early", foreground="blue")
        elif new_status == "On time":
            attendance_table.item(selected_item, tags=("On time",))
            attendance_table.tag_configure("On time", foreground="green")
        elif new_status == "Late (No Admission Slip required)":
            attendance_table.item(selected_item, tags=("Late (No Admission Slip required)",))
            attendance_table.tag_configure("Late (No Admission Slip required)", foreground="orange")
        elif new_status == "Late (Admission Slip required)":
            attendance_table.item(selected_item, tags=("Late (Admission Slip required)",))
            attendance_table.tag_configure("Late (Admission Slip required)", foreground="red")

        top.destroy()
        messagebox.showinfo("Updated", "Record updated successfully.")

    tk.Button(top, text="Submit", command=submit_update).grid(row=3, column=0, columnspan=2, pady=10)
    top.grab_set()
    root.wait_window(top)

# ---------------- EXPORT FUNCTIONS ----------------
def export_csv():
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(REPORTS_DIR, exist_ok=True) # Ensure folder exists
    filename = os.path.join(REPORTS_DIR, f"attendance_{today}.csv")

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Student Name", "Time", "Time Status"])
            for record in attendance_records:
                writer.writerow([record["name"], record["time"], record["status"]])
        return filename
    except PermissionError:
        messagebox.showerror(
            "File Error",
            "Unable to save CSV file.\n\nPlease close the file if it is open and try again."
        )
        return None

def export_text_report():
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(REPORTS_DIR, exist_ok=True) # Ensure folder exists
    filename = os.path.join(REPORTS_DIR, f"attendance_report_{today}.txt")

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("Attendance Report\n")
            file.write("=================\n\n")
            for i, record in enumerate(attendance_records, start=1):
                file.write(f"{i}. {record['name']} - {record['time']} - {record['status']}\n")
            file.write(f"\nTotal Attendance: {len(attendance_records)}\n")
        return filename
    except PermissionError:
        messagebox.showerror(
            "File Error",
            "Unable to save text report.\n\nPlease close the file if it is open and try again."
        )
        return None

def on_close():
    if len(attendance_records) == 0:
        messagebox.showwarning("No Data", "At least one person needed to register.")
        return

    csv_file = export_csv()
    txt_file = export_text_report()

    if not csv_file or not txt_file:
        return

    messagebox.showinfo(
        "Attendance Saved",
        f"Attendance exported automatically to 'attendance_reports' folder.\n"
        f"- {os.path.basename(csv_file)}\n"
        f"- {os.path.basename(txt_file)}"
    )

    root.destroy()

# ---------------- QR / SCAN FUNCTIONS ----------------
def generate_qr():
    name = simple_prompt("Enter full name for QR:")

    if name is None:
        return

    if name.strip() == "":
        messagebox.showwarning("Invalid Input", "Name cannot be empty.")
        return

    if not re.fullmatch(r"[A-Za-z.,\s]+", name):
        messagebox.showwarning("Invalid Input", "Name can only contain letters, periods, and commas only.")
        return

    data = {"name": name, "key": SECRET_KEY}
    data_string = json.dumps(data)

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filename = os.path.join(BASE_DIR, f"{name.replace(' ', '_')}_QR.png")
    img.save(filename)

    os.startfile(filename)
    messagebox.showinfo("QR Generated", f"QR code saved as {os.path.basename(filename)}")

def scan_qr():
    global last_scan_time

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Unable to access camera.")
        return

    detector = cv2.QRCodeDetector()
    messagebox.showinfo("Scan QR", "Show QR code and your face beside it. Press 'Q' to cancel.")

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Camera Error", "Failed to read camera.")
            break

        cv2.imshow("QR Scanner", frame)
        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            current_time = time.time()
            if current_time - last_scan_time < SCAN_DELAY:
                continue

            last_scan_time = current_time

            try:
                qr_data = json.loads(data)
                if qr_data.get("key") != SECRET_KEY:
                    messagebox.showerror("Invalid Qr", "Unauthorized QR code.")
                    continue

                register_student(qr_data.get("name", "Unknown"), frame)

            except json.JSONDecodeError:
                messagebox.showerror("Invalid QR", "QR not recognized.")

            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Attendance System")
root.geometry("600x500")

title_label = tk.Label(root, text="Class Monitor Attendance Tracker", font=("Arial", 16, "bold"))
title_label.pack(pady=(10, 0))

instruction_label = tk.Label(
    root,
    text="(Once ensured that everyone has registered, please close this window)",
    font=("Arial", 10),
    fg="gray"
)
instruction_label.pack(pady=(0, 10))

legend_frame = tk.Frame(root)
legend_frame.pack(pady=(0, 5))

tk.Label(legend_frame, text="● Early", fg="blue", font=("Arial", 9)).pack(side="left", padx=5)
tk.Label(legend_frame, text="● On time", fg="green", font=("Arial", 9)).pack(side="left", padx=5)
tk.Label(legend_frame, text="● Late (No Slip)", fg="orange", font=("Arial", 9)).pack(side="left", padx=5)
tk.Label(legend_frame, text="● Late (Slip Required)", fg="red", font=("Arial", 9)).pack(side="left", padx=5)

search_var = tk.StringVar()
search_var.trace("w", filter_table)

search_frame = tk.Frame(root)
search_frame.pack(pady=(0, 5))

tk.Label(search_frame, text="Search Name:").pack(side="left", padx=5)
tk.Entry(search_frame, textvariable=search_var, width=30).pack(side="left")

table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ("No.", "Name", "Time", "Status")
attendance_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

attendance_table.heading("No.", text="No.")
attendance_table.heading("Name", text="Name")
attendance_table.heading("Time", text="Time")
attendance_table.heading("Status", text="Status")

attendance_table.column("No.", width=40, anchor="center")
attendance_table.column("Name", width=180)
attendance_table.column("Time", width=100, anchor="center")
attendance_table.column("Status", width=220)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=attendance_table.yview)
attendance_table.configure(yscrollcommand=scrollbar.set)

attendance_table.pack(side="left")
scrollbar.pack(side="right", fill="y")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

student_frame = tk.LabelFrame(btn_frame, text="Student Buttons", padx=10, pady=10)
student_frame.grid(row=0, column=0, padx=10, pady=5)

tk.Button(student_frame, text="Generate QR", width=15, command=generate_qr).pack(pady=2)
tk.Button(student_frame, text="Scan QR", width=15, command=scan_qr).pack(pady=2)

admin_frame = tk.LabelFrame(btn_frame, text="Admin Buttons", padx=10, pady=10)
admin_frame.grid(row=0, column=1, padx=10, pady=5)

login_btn = tk.Button(admin_frame, text="Log in as Admin", width=20, command=admin_login)
login_btn.pack(pady=2)

change_pass_btn = tk.Button(admin_frame, text="Change Password", width=20, command=change_password)
change_pass_btn.pack(pady=2)

update_btn = tk.Button(admin_frame, text="Update Record", width=20, command=update_record)
delete_btn = tk.Button(admin_frame, text="Delete Record", width=20, command=delete_record)
logout_btn = tk.Button(admin_frame, text="Log out", width=20, command=admin_logout)

hide_admin_buttons()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()