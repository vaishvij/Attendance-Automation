import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import os
import shutil

# Initialize Firebase
cred = credentials.Certificate("Enter path of your private key here")
firebase_admin.initialize_app(cred,{"databaseURL":"Enter path of your realtime Database here","storageBucket":"Enter path of your storage bucket here"})
ref = db.reference("Students")

class StudentDatabaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Portal")

        self.student_id_label = ttk.Label(root, text="Student ID:")
        self.student_id_entry = ttk.Entry(root)

        self.name_label = ttk.Label(root, text="Name:")
        self.name_entry = ttk.Entry(root)

        self.course_label = ttk.Label(root, text="Course:")
        self.course_entry = ttk.Entry(root)

        self.start_year_label = ttk.Label(root, text="Start Year:")
        self.start_year_entry = ttk.Entry(root)

        self.total_attendance_label = ttk.Label(root, text="Total Attendance:")
        self.total_attendance_entry = ttk.Entry(root)

        self.grade_label = ttk.Label(root, text="Grade:")
        self.grade_entry = ttk.Entry(root)

        self.year_label = ttk.Label(root, text="Year:")
        self.year_entry = ttk.Entry(root)

        self.upload_button = ttk.Button(root, text="Upload Image", command=self.upload_image)

        self.add_button = ttk.Button(root, text="Add Student", command=self.add_student)

        self.student_id_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.course_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.course_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.start_year_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.start_year_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        self.total_attendance_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.total_attendance_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        self.grade_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        self.grade_entry.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

        self.year_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        self.year_entry.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)

        self.upload_button.grid(row=7, column=0, columnspan=2, pady=10)
        self.add_button.grid(row=8, column=0, columnspan=2, pady=10)

    def add_student(self):
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        course = self.course_entry.get()
        start_year = int(self.start_year_entry.get())
        total_attendance = int(self.total_attendance_entry.get())
        grade = self.grade_entry.get()
        year = int(self.year_entry.get())

        student_data = {
            "name": name,
            "course": course,
            "start_year": start_year,
            "total_attendance": total_attendance,
            "grade": grade,
            "year": year,
            # Assuming you want to set a default timestamp for last_attendance_time
            "last_attendance_time": "2024-01-10 00:54:34"
        }

        # Add the student data to the Firebase database with the specified student ID
        ref.child(student_id).set(student_data)

        messagebox.showinfo("Success", "Student added successfully!")

    def upload_image(self):
        student_id = self.student_id_entry.get()
        if not student_id:
            messagebox.showerror("Error", "Please enter the Student ID first.")
            return

        file_path = filedialog.askopenfilename(initialdir="Images", title="Select Image",filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            _,file_extension=os.path.splitext(file_path)
            file_name = f"{student_id}{file_extension}"
            local_image_path=os.path.join("Images",file_name)
            shutil.copyfile(file_path,local_image_path)
            blob = storage.bucket().blob(f"Images/{file_name}")
            blob.upload_from_filename(file_path)
            messagebox.showinfo("Success", f"Image {file_name} uploaded successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDatabaseGUI(root)
    root.mainloop()
