import tkinter as tk
from tkinter import ttk

class Screen1(tk.Frame):
    def __init__(self, master, navigate_callback):
        super().__init__(master)
        self.navigate_callback = navigate_callback
        tk.Label(self, text="Screen 1", font=("Helvetica", 24)).pack(pady=20)
        tk.Button(self, text="Go to Screen 2", command=lambda: self.navigate_callback(2)).pack(pady=10)

class Screen2(tk.Frame):
    def __init__(self, master, navigate_callback):
        super().__init__(master)
        self.navigate_callback = navigate_callback
        tk.Label(self, text="Screen 2", font=("Helvetica", 24)).pack(pady=20)
        tk.Button(self, text="Go to Screen 3", command=lambda: self.navigate_callback(3)).pack(pady=10)
        tk.Button(self, text="Back to Screen 1", command=lambda: self.navigate_callback(1)).pack(pady=10)

class Screen3(tk.Frame):
    def __init__(self, master, navigate_callback):
        super().__init__(master)
        self.navigate_callback = navigate_callback
        tk.Label(self, text="Screen 3", font=("Helvetica", 24)).pack(pady=20)
        tk.Button(self, text="Back to Screen 2", command=lambda: self.navigate_callback(2)).pack(pady=10)

class ScrollableApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Multi-Screen Scrollable App")

        # Set the window to full screen
        self.window.attributes("-fullscreen", True)

        # Create a container frame to hold all screens
        self.container = tk.Frame(window)
        self.container.pack(fill="both", expand=True)

        # Create and store screens in the container
        self.screens = {
            1: Screen1(self.container, self.show_screen),
            2: Screen2(self.container, self.show_screen),
            3: Screen3(self.container, self.show_screen)
        }

        # Place all screens in the same location within the container
        for screen in self.screens.values():
            screen.grid(row=0, column=0, sticky="nsew")

        # Start with the first screen
        self.current_screen = 1
        self.show_screen(self.current_screen)

        # Bind keyboard inputs
        self.window.bind("<Escape>", self.quit_game)
        self.window.bind("l", self.next_screen)
        self.window.bind("j", self.previous_screen)

    def show_screen(self, screen_number):
        # Raise the selected screen to the front and update the current screen tracker
        self.screens[screen_number].tkraise()
        self.current_screen = screen_number

    def next_screen(self, event=None):
        if self.current_screen < len(self.screens):
            self.show_screen(self.current_screen + 1)

    def previous_screen(self, event=None):
        if self.current_screen > 1:
            self.show_screen(self.current_screen - 1)

    def quit_game(self, event=None):
        # Quit the game and restore the window to a normal state
        self.window.attributes("-fullscreen", False)
        self.window.quit()

# Create the main window
window = tk.Tk()
app = ScrollableApp(window)
window.mainloop()
