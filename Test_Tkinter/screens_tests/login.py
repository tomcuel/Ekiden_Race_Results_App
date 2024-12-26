import tkinter
from tkinter import messagebox
import openpyxl

def login_form():
    # Function to check login credentials against the Excel file
    def login():
        username_input = username_entry.get()
        password_input = password_entry.get()
        
        # Open the Excel file and get the active sheet
        try:
            workbook = openpyxl.load_workbook('runner_data.xlsx')  # Adjust the path to your actual Excel file
            sheet = workbook.active
            
            # Loop through each row in the sheet (starting from row 2 to skip the header row)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                stored_username, stored_password = row[7], row[8]  
                
                # Check if the input username and password match the stored values
                if username_input == stored_username and password_input == stored_password:
                    messagebox.showinfo(title="Login Success", message="You successfully logged in.")
                    return
            
            # If no match is found, show an error
            messagebox.showerror(title="Error", message="Invalid login.")
        
        except Exception as e:
            messagebox.showerror(title="Error", message=f"An error occurred: {e}")

    # Create main window
    window = tkinter.Tk()
    window.title("Login form")
    window.geometry('340x440')
    window.configure(bg='#333333')

    frame = tkinter.Frame(bg='#333333')

    # Creating widgets
    login_label = tkinter.Label(
        frame, text="Login", bg='#333333', fg="#ffffff", font=("Arial", 30))
    username_label = tkinter.Label(
        frame, text="Username", bg='#333333', fg="#ffffff", font=("Arial", 16))
    username_entry = tkinter.Entry(frame, font=("Arial", 16))
    password_entry = tkinter.Entry(frame, show="*", font=("Arial", 16))
    password_label = tkinter.Label(
        frame, text="Password", bg='#333333', fg="#ffffff", font=("Arial", 16))
    login_button = tkinter.Button(
        frame, text="Login", bg="#FF3399", fg="#000000", font=("Arial", 16), command=login)

    # Placing widgets on the screen
    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)

    frame.pack()

    window.mainloop()

# Call the login form function
login_form()
