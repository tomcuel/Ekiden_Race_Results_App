# import the necessary libraries
import tkinter as tk
from tkinter import messagebox
import openpyxl

# import the class created in other files
from utility import Utility


# Screen 1: classe to manage the sign up screen
class LoginScreen(tk.Frame):

    # Initialize the Login Screen
    def __init__(self, master, navigate_callback):
        super().__init__(master, bg="#282c34", highlightthickness=0, borderwidth=0, border=0)
        self.navigate_callback = navigate_callback
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header Label
        label = tk.Label(
            self, text="Ekiden Analysis App", font=("Helvetica", 100, "bold"), fg="#ffffff", bg="#282c34"
        )
        label.pack(pady=(90, 50))

        # Username Field
        username_label = tk.Label(
            self, text="Username:", font=("Helvetica", 40), fg="#ffffff", bg="#282c34"
        )
        username_label.pack()
        self.username_entry = tk.Entry(
            self, font=("Helvetica", 20), bg="#f7f7f7"
        )
        self.username_entry.pack(pady=(30, 20))
        self.username_entry.bind("<Return>", Utility.focus_next_widget)

        # Password Field
        password_label = tk.Label(
            self, text="Password:", font=("Helvetica", 40), fg="#ffffff", bg="#282c34"
        )
        password_label.pack()
        self.password_entry = tk.Entry(
            self, show="*", font=("Helvetica", 20), bg="#f7f7f7"
        )
        self.password_entry.pack(pady=(30, 20))
        self.password_entry.bind("<Return>", Utility.focus_next_widget)

        # Login Button 
        self.login_button = tk.Button(
            self, text="Login", font=("Helvetica", 40), fg="#000000", relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, command=self.login,
        )
        self.login_button.pack(pady=(20, 20))
        self.login_button.bind("<Return>", lambda e: self.login_button.invoke())

        # Sign Up Button
        self.signup_button = tk.Button(
            self, text="Sign Up", font=("Helvetica", 40), fg="#000000", relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, command=lambda: [self.navigate_callback(2), self.clear_user_info()] 
        )
        self.signup_button.pack(pady=(20, 20))
        self.signup_button.bind("<Return>", lambda e: self.signup_button.invoke())
        self.signup_button.bind("<Tab>", lambda e: self.refocus_to_username())

    # Function to check if the login credentials are valid (in the Excel file)
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Open the Excel file and get the active sheet
        try:
            workbook = openpyxl.load_workbook('Data/runner_data.xlsx')  # Adjust the path to your actual Excel file
            sheet = workbook.active
            
            # Loop through each row in the sheet (starting from row 2 to skip the header row)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Check if the input username and password match the stored values
                if row[7] == username and row[8] == password:
                    Utility.show_dismissable_messagebox(self, "Success", "Login successful!", lambda: self.navigate_callback(3))
                    self.clear_user_info()
                    return
            # If no match is found, show an error and reset the password fields
            Utility.show_dismissable_messagebox(self, "Error", "Invalid login", lambda: None)
            self.clear_user_info()
        
        except Exception as e:
            messagebox.showerror(title="Error", message=f"An error occurred: {e}")

    # Function to refocus on the username entry field when the Tab key is pressed on the Sign Up button
    def refocus_to_username(self):
        self.username_entry.focus()
        return "break"
    
    # Function to clear both username and password fields from the login screen
    def clear_user_info(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
