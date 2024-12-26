# import the necessary libraries
import tkinter as tk
from tkinter import PhotoImage
import os

# import the class created in other files
from login_screen import LoginScreen
from signup_screen import SignupScreen
from app_screen import App_Screen
from Data import Data_For_App


# Classe to manage the multi-screen app
class Main_App:

    # Initialize the app
    def __init__(self, window):

        # getting all the ekiden datas
        data = Data_For_App("Data/Ekiden_resultats.txt")
        # precompute the datas for the general grpahics that do not depend on the user's input
        fig = "Data/Precomputed_graphs/overall_team_result.png"
        if not os.path.exists(fig):
            # for the team results
            fig1, fig2 = data.create_data_graphs("", 0, data.team_type.MEN, True, fig_1="Data/Precomputed_graphs/overall_team_result.png", fig_2="Data/Precomputed_graphs/men_team_result.png")
            fig1, fig2 = data.create_data_graphs("", 0, data.team_type.WOMEN, True, fig_1="Data/Precomputed_graphs/overall_team_result.png", fig_2="Data/Precomputed_graphs/women_team_result.png")
            fig1, fig2 = data.create_data_graphs("", 0, data.team_type.MIXED, True, fig_1="Data/Precomputed_graphs/overall_team_result.png", fig_2="Data/Precomputed_graphs/mixed_team_result.png")
            # for each distance
            # 10km
            fig1, fig2 = data.create_data_graphs("", 10, data.team_type.MEN, False, fig_1="Data/Precomputed_graphs/overall_10km_result.png", fig_2="Data/Precomputed_graphs/men_10km_result.png")
            fig1, fig2 = data.create_data_graphs("", 10, data.team_type.WOMEN, False, fig_1="Data/Precomputed_graphs/overall_10km_result.png", fig_2="Data/Precomputed_graphs/women_10km_result.png")
            # 7.2km
            fig1, fig2 = data.create_data_graphs("", 7.2, data.team_type.MEN, False, fig_1="Data/Precomputed_graphs/overall_7_2km_result.png", fig_2="Data/Precomputed_graphs/men_7_2km_result.png")
            fig1, fig2 = data.create_data_graphs("", 7.2, data.team_type.WOMEN, False, fig_1="Data/Precomputed_graphs/overall_7_2km_result.png", fig_2="Data/Precomputed_graphs/women_7_2km_result.png")
            # 5km
            fig1, fig2 = data.create_data_graphs("", 5, data.team_type.MEN, False, fig_1="Data/Precomputed_graphs/overall_5km_result.png", fig_2="Data/Precomputed_graphs/men_5km_result.png")
            fig1, fig2 = data.create_data_graphs("", 5, data.team_type.WOMEN, False, fig_1="Data/Precomputed_graphs/overall_5km_result.png", fig_2="Data/Precomputed_graphs/women_5km_result.png")

        self.window = window
        self.window.title("Multi-Screen Scrollable App")
        self.window.attributes("-fullscreen", True)
        window.configure(height=window.winfo_height(), width=window.winfo_width())
        Icone_app = PhotoImage(file="Data/Pictures/App_Icon.png")
        self.window.iconphoto(True, Icone_app)

        # Create a container frame to hold all screens
        self.container = tk.Frame(window)
        self.container.pack(fill="both", expand=True)

        # Create and store screens in the container
        self.screens = {
            1: LoginScreen(self.container, self.show_screen),
            2: SignupScreen(self.container, self.show_screen),
            3: App_Screen(self.container, self.show_screen, window.winfo_width(), data)
        }

        # Place all screens in the same location within the container
        for screen in self.screens.values():
            screen.grid(row=0, column=0, sticky="nsew")

        # Start with the first screen
        self.current_screen = 1
        self.show_screen(self.current_screen)

        # Bind keyboard inputs
        self.window.bind("<Escape>", self.quit_game)

    # Function to show the selected screen
    def show_screen(self, screen_number):
        # Raise the selected screen to the front and update the current screen tracker
        self.screens[screen_number].tkraise()
        self.current_screen = screen_number
        # direct focus to the first field for the login and sign up screens
        if self.current_screen == 1:
            self.screens[screen_number].after(500, lambda: self.screens[screen_number].username_entry.focus())
        elif self.current_screen == 2:
            self.screens[screen_number].after(500, lambda: self.screens[screen_number].first_name_entry.focus())

    # Function to navigate to the next screen
    def next_screen(self, event=None):
        if self.current_screen < len(self.screens):
            self.show_screen(self.current_screen + 1)

    # Function to navigate to the previous screen
    def previous_screen(self, event=None):
        if self.current_screen > 1:
            self.show_screen(self.current_screen - 1)

    # Function to quit the app
    def quit_game(self, event=None):
        # Quit the app
        self.window.quit()
