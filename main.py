import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# DataBase
myDB = sqlite3.connect("file.db")
cursorDB = myDB.cursor()
dbQuery = """
CREATE TABLE IF NOT EXISTS personal_data (
    pid INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    age INTEGER,
    employment TEXT,
    salary REAL,
    tax REAL,
    insurance REAL,
    net_salary REAL
)
"""
cursorDB.execute(dbQuery)
myDB.commit()


# Functions
def validateNum(number):
    if number == "" or number.isdigit():
        return True
    else:
        return False


def validateName(name):
    if len(name) <= 25:
        name = name.strip()
        for char in name:
            if not (char.isalpha() or char.isspace()):
                return False
        return True
    return False


def validateFloat(number):
    if number == "" or (number.replace('.', '', 1).isdigit() and number.count('.') <= 1):
        return True
    else:
        return False


def authentication():
    pid = input_1.get()
    first_name = input_2.get()
    last_name = input_3.get()
    gender = myGender.get()
    age = input_5.get()
    employment = input_6.get()
    salary = input_7.get()
    tax = input_8.get()
    insurance = input_9.get()

    if len(pid) < 3:
        messagebox.showwarning("ID Length",
                               "ID Length must be 3 characters.")
        return

    if len(first_name) < 3 or len(last_name) < 3:
        messagebox.showwarning("Name Length",
                               "First Name and Last Name must be between 3 and 25 characters.")
        return
    if "  " in first_name or "  " in last_name:
        messagebox.showwarning("Invalid Input",
                               "Dont use two spaces in a fild.")
        return

    if gender not in ("Male", "Female"):
        messagebox.showwarning("Invalid Gender",
                               "Please select a valid gender (Male or Female).")
        return

    if not age:
        messagebox.showwarning("Invalid Input",
                               "Please enter Age.")
        return

    if len(age) > 3:
        messagebox.showwarning("Invalid Input",
                               "Age must be less than 3 digits.")
        return

    if not employment:
        messagebox.showwarning("Invalid Input",
                               "Please enter Employment.")
        return

    if not (salary and tax and insurance):
        messagebox.showwarning("Invalid Input",
                               "Please enter Salary, Tax, insurance.")
        return

    if not (pid and first_name and last_name and gender and age and employment and salary and tax and insurance):
        messagebox.showwarning("Incomplete Information",
                               "Please fill in all fields.")
        return
    try:
        salary = float(input_7.get())
        tax = float(input_8.get())
        insurance = float(input_9.get())
        total_tax = (salary * tax) / 100
        total_insurance = (salary * insurance) / 100
        total = tax + insurance
        total_min = total_tax + total_insurance

        if total > 100:
            messagebox.showwarning("Warning",
                                   "The total of Tax and Insurance is over 100.")
        else:
            net_salary = salary - total_min

            input_10.config(state='normal')
            input_10.delete(0, tkinter.END)
            input_10.insert(0, str(net_salary))
            input_10.config(state='disabled')

            age = int(age)
            if age > 100:
                messagebox.showinfo("Congratulations",
                                    "Congratulations for being over 100 years old,\n all your entries are valid!")
            else:
                messagebox.showinfo("Valid Entries",
                                    "All your entries are valid.")

    except ValueError:
        messagebox.showerror("Invalid Input",
                             "Please enter Number values for Age, Salary, Tax, and Insurance.")


def save():
    try:
        pid = input_1.get()
        first_name = input_2.get()
        last_name = input_3.get()
        gender = myGender.get()
        age = input_5.get()
        employment = input_6.get()
        salary = input_7.get()
        tax = input_8.get()
        insurance = input_9.get()
        net_salary = input_10.get()

        if not (pid and first_name and last_name and gender and age and employment and salary and tax and insurance):
            messagebox.showwarning("Incomplete Information",
                                   "Please fill in all fields.")
            return

        mySaveDB = sqlite3.connect("file.db")
        cursorSaveDB = mySaveDB.cursor()

        cursorSaveDB.execute("SELECT pid FROM personal_data WHERE pid=?", (pid,))
        existing_id = cursorSaveDB.fetchone()
        if existing_id:
            messagebox.showwarning("Duplicate ID",
                                   "This ID exists in the database.")
            return
        confirmation = messagebox.askyesno("Confirm Data",
                                           "Are you sure you want to save this data?")
        if confirmation:
            cursorSaveDB.execute(
                "INSERT INTO personal_data (pid, first_name, last_name, gender, age, employment, salary, tax, insurance, net_salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (pid, first_name, last_name, gender, age, employment, salary, tax, insurance, net_salary))

            mySaveDB.commit()

            messagebox.showinfo("Data Saved",
                                "Your data has been saved successfully.")

    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred: {e}")


def clearForm():
    input_1.delete(0, tkinter.END)
    input_2.delete(0, tkinter.END)
    input_3.delete(0, tkinter.END)
    myGender.set(" ")
    input_5.delete(0, tkinter.END)
    input_6.set(" ")
    input_7.delete(0, tkinter.END)
    input_8.delete(0, tkinter.END)
    input_9.delete(0, tkinter.END)
    input_10.config(state='normal')
    input_10.delete(0, tkinter.END)
    input_10.insert(0, " ")
    input_10.config(state='disabled')
    messagebox.showinfo("Form Cleared",
                        "Your form has been cleared.")


def authentication_shortcut(event):
    _ = event
    authentication()


def save_shortcut(event):
    _ = event
    save()


def clear_shortcut(event):
    _ = event
    clearForm()


def mainMenu():
    menu_bar = tkinter.Menu(myform)

    file_menu = tkinter.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Authentication", command=authentication, accelerator="Ctrl+X")
    file_menu.add_command(label="Save", command=save, accelerator="Ctrl+s")
    file_menu.add_command(label="Clear Form", command=clearForm, accelerator="Ctrl+c")

    menu_bar.add_cascade(label="File", menu=file_menu)
    myform.config(menu=menu_bar)

    myform.bind("<Control-x>", authentication_shortcut)
    myform.bind("<Control-s>", save_shortcut)
    myform.bind("<Control-c>", clear_shortcut)


# Tkinter
myform = tkinter.Tk()
myform.title("Information Form")
myform.resizable(False, False)
myform.configure(padx=10, pady=20)
myform.iconbitmap('icon.ico')

validatorNum = myform.register(validateNum)
validatorName = myform.register(validateName)
validateFloat = myform.register(validateFloat)

# ID
label_1 = tkinter.Label(myform, text="ID", width=12, font=("Calibri", 15), anchor="w", justify="left")
input_1 = tkinter.Entry(myform, validate="key", validatecommand=(validatorNum, "%P"), width=15, font=("Calibri", 15))
label_1.grid(row=0, column=0)
input_1.grid(row=0, column=1, columnspan=2)

# First Name
label_2 = tkinter.Label(myform, text="First Name", width=12, font=("Calibri", 15), anchor="w", justify="left")
input_2 = tkinter.Entry(myform, width=15, validate="key", validatecommand=(validatorName, "%P"), font=("Calibri", 15))
label_2.grid(row=1, column=0)
input_2.grid(row=1, column=1, columnspan=2)

# Last Name
label_3 = tkinter.Label(myform, text="Last Name", width=12, font=("Calibri", 15), anchor="w", justify="left")
input_3 = tkinter.Entry(myform, width=15, validate="key", validatecommand=(validatorName, "%P"), font=("Calibri", 15))
label_3.grid(row=2, column=0)
input_3.grid(row=2, column=1, columnspan=2)

# Gender
selectedGender = tkinter.Label(myform, text="Gender", font=("Calibri", 15), anchor="w", justify="left")
selectedGender.grid(row=3, column=0, sticky="w")

myGender = tkinter.StringVar()
myGender.set(" ")

maleRadio = tkinter.Radiobutton(myform, text="Male", font=("Calibri", 15), value="Male", variable=myGender)
maleRadio.grid(row=3, column=1)

femaleRadio = tkinter.Radiobutton(myform, text="Female", font=("Calibri", 15), value="Female", variable=myGender)
femaleRadio.grid(row=3, column=2)

# Age
label_5 = tkinter.Label(myform, text="Age", width=12, font=("Calibri", 15), anchor="w", justify="left")
input_5 = tkinter.Entry(myform, width=15, validate="key", validatecommand=(validatorNum, "%P"), font=("Calibri", 15))
label_5.grid(row=4, column=0)
input_5.grid(row=4, column=1, columnspan=2)

# Employment
label_6 = tkinter.Label(myform, text="Employment", width=12, font=("Calibri", 15), anchor="w", justify="left")
input_6 = ttk.Combobox(myform, values=["Student", "Employed", "Unemployed", "Retired"], width=13, font=("Calibri", 15),
                       state="readonly")
label_6.grid(row=5, column=0)
input_6.grid(row=5, column=1, columnspan=2)

# Salary
label_7 = tkinter.Label(myform, text="Salary", width=12, font=("Calibri", 15), anchor="w", justify="left")
input_7 = tkinter.Entry(myform, width=15, validate="key", validatecommand=(validateFloat, "%P"), font=("Calibri", 15))
label_7.grid(row=6, column=0)
input_7.grid(row=6, column=1, columnspan=2)

# Tax
label_8 = tkinter.Label(myform, text="Tax", width=12, font=("Calibri", 15), anchor="w", justify="left")
input_8 = tkinter.Entry(myform, width=15, validate="key", validatecommand=(validateFloat, "%P"), font=("Calibri", 15))
label_8.grid(row=7, column=0)
input_8.grid(row=7, column=1, columnspan=2)

# Insurance
label_9 = tkinter.Label(myform, text="Insurance", width=12, font=("Calibri", 15), anchor="w", justify="left")
input_9 = tkinter.Entry(myform, width=15, validate="key", validatecommand=(validateFloat, "%P"), font=("Calibri", 15))
label_9.grid(row=8, column=0)
input_9.grid(row=8, column=1, columnspan=2)

# Net Salary
label_10 = tkinter.Label(myform, text="Net Salary", width=12, font=("Calibri", 15), anchor="w", justify="left")
input_10 = tkinter.Entry(myform, width=15, font=("Calibri", 15), highlightthickness=2,
                         highlightbackground="green")
input_10.config(state='disabled')
label_10.grid(row=9, column=0)
input_10.grid(row=9, column=1, columnspan=2)

# Buttons
btn_1 = tkinter.Button(myform, text="Authentication", width=14, font=("Calibri", 15), bg="skyblue", fg="black",
                       activebackground="white", activeforeground="black")
btn_1.config(command=authentication)
btn_1.grid(row=10, column=0, columnspan=3)

btn_2 = tkinter.Button(myform, text="Save", width=14, font=("Calibri", 15), bg="green", fg="white",
                       activebackground="white", activeforeground="green")
btn_2.config(command=save)
btn_2.grid(row=11, column=0, columnspan=3)

btn_3 = tkinter.Button(myform, text="Clear Form", width=14, font=("Calibri", 15), bg="gray", fg="white",
                       activebackground="white", activeforeground="gray")
btn_3.config(command=clearForm)
btn_3.grid(row=12, column=0, columnspan=3)

mainMenu()
myform.mainloop()
