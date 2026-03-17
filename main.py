from tkinter import ttk, messagebox
import tkinter as tk
from databaseMod import databaseClass


db = databaseClass("employeeData.db")

root = tk.Tk()
root.title("CENTURY FACILITY SERVICES - EMPLOYEE DATA")
root.config(bg="#B0C4DE")
root.state("zoomed")

 
idVar = tk.StringVar()
nameVar = tk.StringVar() 
emailVar = tk.StringVar()
phoneVar = tk.StringVar()
salaryVar = tk.StringVar()
attendanceVar = tk.StringVar()
searchVar = tk.StringVar()
searchFieldVar = tk.StringVar()  


# mainFrame covers entire window 

mainFrame = tk.Frame(root, bg = "#B0C4DE")
mainFrame.pack(expand="True", fill="both")

mainFrame.rowconfigure(0, weight=1)
mainFrame.rowconfigure(1, weight=1)
mainFrame.rowconfigure(2, weight=1)
mainFrame.rowconfigure(3, weight=1)
mainFrame.rowconfigure(4, weight=1)

mainFrame.columnconfigure(0, weight=1)

heading = tk.Label(mainFrame, text = "CENTURY FACILITY SERVICES - EMPLOYEE DATA", font=("Times New Roman", 20, "bold","underline"), bg = "#B0C4DE")
heading.grid(row=0)


# data entry frame

entryFrame = tk.Frame(mainFrame, bg = "#B0C4DE")
entryFrame.grid(row=1)

id = tk.Label(entryFrame, text = "ID : ", font=("Calibri", 16, "bold"), bg = "#B0C4DE")
id.grid(row=0, column=0, sticky="e")

txtid = tk.Entry(entryFrame, textvariable=idVar, font=("Calibri", 16), width=25)
txtid.grid(row=0, column=1, padx=10, pady=10, sticky="w")

name = tk.Label(entryFrame, text = "Name : ", font=("Calibri", 16, "bold"), bg = "#B0C4DE")
name.grid(row=0, column=2, sticky="e")

txtname = tk.Entry(entryFrame, textvariable=nameVar, font=("Calibri", 16), width=25)
txtname.grid(row=0, column=3, padx=10, pady=10, sticky="w")

email = tk.Label(entryFrame, text = "Email : ", font=("Calibri", 16, "bold"), bg = "#B0C4DE")
email.grid(row=1, column=0, sticky="e")

txtemail = tk.Entry(entryFrame, textvariable=emailVar, font=("Calibri", 16), width=25)
txtemail.grid(row=1, column=1, padx=10, pady=10, sticky="w")

phone = tk.Label(entryFrame, text = "Phone number : ", font=("Calibri", 16, "bold"), bg = "#B0C4DE")
phone.grid(row=1, column=2, sticky="e")

txtphone = tk.Entry(entryFrame, textvariable=phoneVar, font=("Calibri", 16), width=25)
txtphone.grid(row=1, column=3, padx=10, pady=10, sticky="w")

salary = tk.Label(entryFrame, text = "Salary : ", font=("Calibri", 16, "bold"), bg = "#B0C4DE")
salary.grid(row=2, column=0, sticky="e")

txtsalary = tk.Entry(entryFrame, textvariable=salaryVar, font=("Calibri", 16), width=25)
txtsalary.grid(row=2, column=1, padx=10, pady=10, sticky="w")

attendance = tk.Label(entryFrame, text = "Attendance (Days) : ", font=("Calibri", 16, "bold"), bg = "#B0C4DE")
attendance.grid(row=2, column=2, sticky="e")

txtattendance = tk.Entry(entryFrame, textvariable=attendanceVar, font=("Calibri", 16), width=25)
txtattendance.grid(row=2, column=3, padx=10, pady=10, sticky="w")


# Functions 

def clear_tv_table():
    """Clear all the data that was previously present in the data display table (treeview widget)"""
    for item in table.get_children():
      table.delete(item) 

def clear_entries():
    """Clears all the entered data"""
    idVar.set("")
    nameVar.set("") 
    emailVar.set("")
    phoneVar.set("")
    salaryVar.set("")
    attendanceVar.set("")

def get_record(event):
    """Gets the data from the particular row selected in table"""
    selected_row = table.focus()
    global rowData
    rowData = table.item(selected_row, "values")
    if rowData:  # Check if rowData is not empty
        global id1 
        id1 = int(rowData[0])
        idVar.set(rowData[0])
        nameVar.set(rowData[1]) 
        emailVar.set(rowData[2])
        phoneVar.set(rowData[3])
        salaryVar.set(rowData[4])
        attendanceVar.set(rowData[5])

def get_data():
    """Gets all the data from the database and adds it to the data display table"""
    for row in db.fetch():
        table.insert(parent="", index="end", value=row)

def validate_input():
    """Validate user input and return error message if any"""
    if (idVar.get() == "" or nameVar.get() == "" or emailVar.get() == "" or 
        phoneVar.get() == "" or salaryVar.get() == "" or attendanceVar.get() == ""):
        return "Enter complete details"
    
    # Check if ID is numeric
    try:
        int(idVar.get())
    except ValueError:
        return "ID must be a number"
    
    # Check if phone number is numeric
    try:
        int(phoneVar.get())
    except ValueError:
        return "Phone number must be numeric"
    
    # Check if salary is numeric
    try:
        float(salaryVar.get())
    except ValueError:
        return "Salary must be a number"
    
    # Check if attendance is numeric
    try:
        int(attendanceVar.get())
    except ValueError:
        return "Attendance must be a number"
    
    return None

def add_employee():
    # Validate input
    error_msg = validate_input()
    if error_msg:
        messagebox.showerror(title="Error", message=error_msg)
        return
    
    # Try to insert employee
    success, msg = db.insert(int(idVar.get()), nameVar.get(), emailVar.get(), 
                            int(phoneVar.get()), float(salaryVar.get()), int(attendanceVar.get()))
    
    if success:
        clear_entries()
        clear_tv_table()
        get_data()
        messagebox.showinfo(title="Success", message=msg)
    else:
        messagebox.showerror(title="Error", message=msg)
    
def del_employee():
    if 'rowData' not in globals() or not rowData:
        messagebox.showerror(title="Error", message="Select a record to delete first")
        return
        
    db.delete(int(rowData[0]))
    clear_entries()
    clear_tv_table()
    get_data()
    messagebox.showinfo(title="Success", message="Employee deleted successfully")

def update():
    if not table.focus():
        messagebox.showerror(title="Error", message="Select record to update first")
        return
    
    # Validate input
    error_msg = validate_input()
    if error_msg:
        messagebox.showerror(title="Error", message=error_msg)
        return
    
    # Try to update employee
    success, msg = db.update(int(idVar.get()), nameVar.get(), emailVar.get(), 
                            int(phoneVar.get()), float(salaryVar.get()), int(attendanceVar.get()), id1)
    
    if success:
        clear_entries()
        clear_tv_table()
        get_data()
        messagebox.showinfo(title="Success", message=msg)
    else:
        messagebox.showerror(title="Error", message=msg)


def search_employee():
    """Search for employees based on search criteria"""
    search_term = searchVar.get().strip()
    search_field = searchFieldVar.get()
    
    clear_tv_table()
    
    if search_term == "":
        # If search is empty, show all records
        get_data()
    else:
        # Perform search
        results = db.search(search_term, search_field)
        for row in results:
            table.insert(parent="", index="end", value=row)

def clear_search():
    """Clear search and show all records"""
    searchVar.set("")
    clear_tv_table()
    get_data()


#search frame
searchFrame = tk.Frame(mainFrame, bg = "#B0C4DE")
searchFrame.grid(row=2)

searchFrame.columnconfigure(0, weight=1)
searchFrame.columnconfigure(1, weight=1)
searchFrame.columnconfigure(2, weight=1)
searchFrame.columnconfigure(3, weight=1)
searchFrame.columnconfigure(4, weight=1)

searchLabel = tk.Label(searchFrame, text="Search:", font=("Calibri", 14, "bold"), bg="#B0C4DE")
searchLabel.grid(row=0, column=0, padx=5, pady=10, sticky="e")

searchEntry = tk.Entry(searchFrame, textvariable=searchVar, font=("Calibri", 14), width=20)
searchEntry.grid(row=0, column=1, padx=5, pady=10)

searchFieldVar.set("all")
searchFieldCombo = ttk.Combobox(searchFrame, textvariable=searchFieldVar, 
                               values=["all", "ID", "Name", "Email", "Phone", "Salary", "Attendance"], 
                               state="readonly", font=("Calibri", 12), width=12)
searchFieldCombo.grid(row=0, column=2, padx=5, pady=10)

searchButton = tk.Button(searchFrame, text="Search", font=("Calibri", 12, "bold"), bg="darkgreen", fg="white", 
                        command=search_employee, width=10)
searchButton.grid(row=0, column=3, padx=5, pady=10)

clearSearchButton = tk.Button(searchFrame, text="Clear", font=("Calibri", 12, "bold"), bg="darkred", fg="white", 
                             command=clear_search, width=10)
clearSearchButton.grid(row=0, column=4, padx=5, pady=10)

# Bind Enter key to search
searchEntry.bind('<Return>', lambda event: search_employee())


#buttons frame

buttonFrame = tk.Frame(mainFrame, bg = "#B0C4DE")
buttonFrame.grid(row=3)

buttonFrame.columnconfigure(0, weight=1)
buttonFrame.columnconfigure(1, weight=1)
buttonFrame.columnconfigure(2, weight=1)

addButton = tk.Button(buttonFrame, text="Add new employee", font=("Calibri", 16,"bold"), width=20, bg="black", fg="white", command=add_employee)
addButton.grid(row=0, column=0, padx=10, pady=10)

delButton = tk.Button(buttonFrame, text="Delete employee", font=("Calibri", 16,"bold"), width=20, bg="black", fg="white", command=del_employee)
delButton.grid(row=0, column=1, padx=10, pady=10)

updateButton = tk.Button(buttonFrame, text="Update details", font=("Calibri", 16, "bold"), width=20, bg="black", fg="white", command=update)
updateButton.grid(row=0, column=2, padx=10, pady=10)


# data display table

tableFrame = tk.Frame(mainFrame)
tableFrame.grid(row=4)

# making a scrollbar

tableScrollbar = tk.Scrollbar(tableFrame)
tableScrollbar.pack(side="right", fill="y")

table = ttk.Treeview(tableFrame, columns=(1,2,3,4,5,6), show="headings", yscrollcommand=tableScrollbar.set) 

tableScrollbar.configure(command=table.yview)

table.heading(1, text = "ID")
table.heading(2, text = "Name")
table.heading(3, text = "Email")
table.heading(4, text = "Phone no.")
table.heading(5, text = "Salary")
table.heading(6, text = "Attendance")

table.column(1, width ="50", anchor="center")
table.column(2, width ="110", anchor="w")
table.column(3, width ="180", anchor="w")
table.column(4, width ="130", anchor="w")
table.column(5, width ="100", anchor="e")
table.column(6, width ="100", anchor="center")

tableStyle = ttk.Style(table)
tableStyle.theme_use('clam')
tableStyle.configure("Treeview", rowheight = 40, font=14)

table.bind("<ButtonRelease-1>", get_record)
table.pack()

clear_tv_table()
get_data()


root.mainloop()