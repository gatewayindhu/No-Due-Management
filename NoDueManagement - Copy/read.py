import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from database import Database


class NoDueManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("No Due Management System")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")
        
        self.db = Database()

        
        self.header_frame = tk.Frame(root, bg="#4CAF50", pady=10)
        self.header_frame.pack(fill="x")
        self.header_label = tk.Label(self.header_frame, text="No Due Management System", font=("Helvetica", 24), fg="white", bg="#4CAF50")
        self.header_label.pack()

        
        self.form_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
        self.form_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.student_id_label = tk.Label(self.form_frame, text="Student ID", font=("Helvetica", 12))
        self.student_id_label.grid(row=0, column=0, padx=10, pady=10)
        self.student_id_entry = tk.Entry(self.form_frame, font=("Helvetica", 12), width=20)
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=10)

        self.name_label = tk.Label(self.form_frame, text="Name", font=("Helvetica", 12))
        self.name_label.grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.form_frame, font=("Helvetica", 12), width=20)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        self.department_label = tk.Label(self.form_frame, text="Department", font=("Helvetica", 12))
        self.department_label.grid(row=2, column=0, padx=10, pady=10)
        self.department_entry = tk.Entry(self.form_frame, font=("Helvetica", 12), width=20)
        self.department_entry.grid(row=2, column=1, padx=10, pady=10)

        self.due_amount_label = tk.Label(self.form_frame, text="Due Amount", font=("Helvetica", 12))
        self.due_amount_label.grid(row=3, column=0, padx=10, pady=10)
        self.due_amount_entry = tk.Entry(self.form_frame, font=("Helvetica", 12), width=20)
        self.due_amount_entry.grid(row=3, column=1, padx=10, pady=10)

        button_style = {"font": ("Helvetica", 12), "width": 15, "bg": "#4CAF50", "fg": "white", "activebackground": "#45a049"}
        
        self.add_button = tk.Button(self.form_frame, text="Add Student", command=self.add_student, **button_style)
        self.add_button.grid(row=4, column=0, padx=10, pady=10)

        self.update_button = tk.Button(self.form_frame, text="Update Due", command=self.update_due, **button_style)
        self.update_button.grid(row=4, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self.form_frame, text="Delete Student", command=self.delete_student, **button_style)
        self.delete_button.grid(row=4, column=2, padx=10, pady=10)

        self.pay_button = tk.Button(self.form_frame, text="Pay Due", command=self.pay_due, **button_style)
        self.pay_button.grid(row=4, column=3, padx=10, pady=10)

      
        self.search_label = tk.Label(self.form_frame, text="Search", font=("Helvetica", 12))
        self.search_label.grid(row=5, column=0, padx=10, pady=10)
        self.search_entry = tk.Entry(self.form_frame, font=("Helvetica", 12))
        self.search_entry.grid(row=5, column=1, padx=10, pady=10)
        self.search_button = tk.Button(self.form_frame, text="Search", command=self.search_student, **button_style)
        self.search_button.grid(row=5, column=2, padx=10, pady=10)

        
        self.export_button = tk.Button(self.form_frame, text="Export to Excel", command=self.export_to_excel, **button_style)
        self.export_button.grid(row=6, column=0, columnspan=2, pady=10)

        
        self.analytics_button = tk.Button(self.form_frame, text="Show Analytics", command=self.show_analytics, **button_style)
        self.analytics_button.grid(row=6, column=2, columnspan=2, pady=10)

        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Department", "Due"), show="headings", height=6)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Due", text="Due Amount")
        self.tree.pack(fill="both", padx=20, pady=20)

        self.refresh_data()

    def add_student(self):
        try:
            student_id = int(self.student_id_entry.get())
            name = self.name_entry.get()
            department = self.department_entry.get()
            due_amount = float(self.due_amount_entry.get())

            self.db.add_student(student_id, name, department, due_amount)
            messagebox.showinfo("Success", "Student added successfully!")
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {e}")

    def update_due(self):
        try:
            student_id = int(self.student_id_entry.get())
            due_amount = float(self.due_amount_entry.get())

            self.db.update_due(student_id, due_amount)
            messagebox.showinfo("Success", "Due updated successfully!")
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update due: {e}")

    def delete_student(self):
        try:
            student_id = int(self.student_id_entry.get())
            self.db.delete_student(student_id)
            messagebox.showinfo("Success", "Student deleted successfully!")
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {e}")

    def pay_due(self):
        try:
            student_id = int(self.student_id_entry.get())
            self.db.update_due(student_id, 0)  
            messagebox.showinfo("Success", "Payment successful! Due cleared.")
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear due: {e}")

    def search_student(self):
        query = self.search_entry.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for student in self.db.get_students():
            if query in str(student[0]).lower() or query in student[1].lower() or query in student[2].lower():
                self.tree.insert("", "end", values=student)

    def export_to_excel(self):
        
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        
        if file_path:
            data = self.db.get_students()
            if data:
                df = pd.DataFrame(data, columns=["Student ID", "Name", "Department", "Due Amount"])
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Data exported to '{file_path}'")
            else:
                messagebox.showwarning("Warning", "No data to export!")
        else:
            messagebox.showwarning("Warning", "Save path not selected!")

    def show_analytics(self):
        data = self.db.get_students()
        departments = {}
        dues = []

        for _, _, dept, due in data:
            if dept in departments:
                departments[dept] += due
            else:
                departments[dept] = due
            dues.append(due)

        
        plt.figure(figsize=(10, 5))
        plt.subplot(2, 2, 1)  
        plt.bar(departments.keys(), departments.values(), color="skyblue")
        plt.title("Total Dues by Department")
        plt.xlabel("Department")
        plt.ylabel("Total Dues")

        
        plt.subplot(2, 2, 2) 
        plt.pie(departments.values(), labels=departments.keys(), autopct='%1.1f%%', startangle=140)
        plt.title("Dues Distribution by Department")

        plt.subplot(2, 2, 3)  
        plt.hist(dues, bins=10, color="lightcoral", edgecolor="black")
        plt.title("Histogram of Dues")
        plt.xlabel("Due Amount")
        plt.ylabel("Frequency")

        
        student_ids = [student[0] for student in data]
        plt.subplot(2, 2, 4)  
        plt.scatter(student_ids, dues, color="green")
        plt.title("Student ID vs Due Amount")
        plt.xlabel("Student ID")
        plt.ylabel("Due Amount")

      
        plt.tight_layout()
        plt.show()

    def refresh_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for student in self.db.get_students():
            self.tree.insert("", "end", values=student)


if __name__ == "__main__":
    root = tk.Tk()
    app = NoDueManagementSystem(root)  
    root.mainloop()
