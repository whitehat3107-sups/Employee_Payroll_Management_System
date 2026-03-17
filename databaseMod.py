import tkinter as tk
import sqlite3 

class databaseClass():
    def __init__(self, dbName):

        self.dbName = dbName

        # Connect to database or create a new one
        self.conn = sqlite3.connect(self.dbName)

        
        # cur is used to execute commands in database
        self.cur = self.conn.cursor()


        # query to create a table named data in the database
        # Here ID has PRIMARY KEY constraint which means it is unique and does not have NULL value
        query = """
        CREATE TABLE IF NOT EXISTS data(
            ID INTEGER PRIMARY KEY,
            Name varchar(100), 
            Email varchar(100),
            Phone INTEGER,
            Salary REAL,
            Attendance INTEGER
        )"""
        self.cur.execute(query)

        # Save the changes to the database
        self.conn.commit()


    def fetch(self):
        selectQuery = "SELECT *,oid from data"
        self.cur.execute(selectQuery)

        # fetchall returns a list of tuples of all the data present in the database
        records = self.cur.fetchall()
        return records

    def check_id_exists(self, id):
        """Check if an ID already exists in the database"""
        checkQuery = "SELECT COUNT(*) FROM data WHERE ID=?"
        self.cur.execute(checkQuery, (id,))
        count = self.cur.fetchone()[0]
        return count > 0

        
    def insert(self, id, name, email, phone, salary, attendance):
        try:
            insertQuery = "INSERT INTO data (ID,Name,Email,Phone,Salary,Attendance) VALUES (?,?,?,?,?,?)"
            self.cur.execute(insertQuery,(id, name, email, phone, salary, attendance))
            self.conn.commit()
            return True, "Employee added successfully"
        except sqlite3.IntegrityError:
            return False, "Employee ID already exists"
        except Exception as e:
            return False, f"Database error: {str(e)}"


    def delete(self, id):
        delQuery = """DELETE FROM data WHERE ID=?"""
        self.cur.execute(delQuery,(id,))
        self.conn.commit()

    def update(self, id, name, email, phone, salary, attendance, id1):
        try:
            updQuery = """
                UPDATE data 
                SET ID=?, Name=?, Email=?, Phone=?, Salary=?, Attendance=? 
                WHERE ID=?
                """
            self.cur.execute(updQuery,(id, name, email, phone, salary, attendance, id1))
            self.conn.commit()
            return True, "Employee updated successfully"
        except sqlite3.IntegrityError:
            return False, "Employee ID already exists"
        except Exception as e:
            return False, f"Database error: {str(e)}"

    def search(self, search_term, search_field="all"):
        """Search for employees based on search term and field"""
        if search_field == "all":
            searchQuery = """
                SELECT *,oid FROM data 
                WHERE CAST(ID AS TEXT) LIKE ? OR 
                      Name LIKE ? OR 
                      Email LIKE ? OR 
                      CAST(Phone AS TEXT) LIKE ? OR
                      CAST(Salary AS TEXT) LIKE ? OR
                      CAST(Attendance AS TEXT) LIKE ?
            """
            search_pattern = f"%{search_term}%"
            self.cur.execute(searchQuery, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
        else:
            if search_field == "ID":
                searchQuery = "SELECT *,oid FROM data WHERE CAST(ID AS TEXT) LIKE ?"
            elif search_field == "Name":
                searchQuery = "SELECT *,oid FROM data WHERE Name LIKE ?"
            elif search_field == "Email":
                searchQuery = "SELECT *,oid FROM data WHERE Email LIKE ?"
            elif search_field == "Phone":
                searchQuery = "SELECT *,oid FROM data WHERE CAST(Phone AS TEXT) LIKE ?"
            elif search_field == "Salary":
                searchQuery = "SELECT *,oid FROM data WHERE CAST(Salary AS TEXT) LIKE ?"
            elif search_field == "Attendance":
                searchQuery = "SELECT *,oid FROM data WHERE CAST(Attendance AS TEXT) LIKE ?"
            
            search_pattern = f"%{search_term}%"
            self.cur.execute(searchQuery, (search_pattern,))
        
        records = self.cur.fetchall()
        return records