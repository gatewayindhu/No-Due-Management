import sqlite3

class Database:
    def __init__(self, db_name="no_due_system.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS dues (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            due_amount REAL DEFAULT 0
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_student(self, student_id, name, department, due_amount=0):
        query = "INSERT INTO dues (student_id, name, department, due_amount) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (student_id, name, department, due_amount))
        self.conn.commit()

    def update_due(self, student_id, due_amount):
        query = "UPDATE dues SET due_amount = ? WHERE student_id = ?"
        self.cursor.execute(query, (due_amount, student_id))
        self.conn.commit()

    def get_students(self):
        query = "SELECT * FROM dues"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_student(self, student_id):
        query = "DELETE FROM dues WHERE student_id = ?"
        self.cursor.execute(query, (student_id,))
        self.conn.commit()
