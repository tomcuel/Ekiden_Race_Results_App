import tkinter as tk
from tkinter import ttk

class ScrollableApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Scrollable App")
        
        # Create a canvas widget for scrolling
        self.canvas = tk.Canvas(window)
        self.scroll_frame = tk.Frame(self.canvas)
        
        # Configure a vertical scrollbar for the canvas
        self.v_scrollbar = ttk.Scrollbar(window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        
        # Pack the canvas and scrollbar to fill the window
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create a window in the canvas to add widgets
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        
        # Bind scrolling events for trackpad and mouse wheel
        self.canvas.bind_all("<MouseWheel>", self.on_scroll)

        # Create an entry widget directly in the scrollable area
        self.entry = tk.Entry(self.scroll_frame, font=("Helvetica", 14))
        self.entry.grid(row=0, column=0, padx=10, pady=10)
        self.entry.bind("<FocusIn>", self.on_entry_click)
        self.entry_selected = False
        
        # Populate the frame with buttons and content
        for i in range(1, 31):
            button = tk.Button(self.scroll_frame, text=f"Button {i}", command=lambda i=i: self.display_text(f"Button {i} clicked"))
            button.grid(row=i, column=0, padx=10, pady=5)
        
        # Update canvas scroll region when frame changes
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    def display_text(self, text):
        print(text)

    def on_entry_click(self, event):
        if self.entry_selected:
            self.entry_selected = False
            self.window.focus()  # Deselect the entry when clicked again
        else:
            self.entry_selected = True

    def on_scroll(self, event):
        direction = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(direction, "units")

# Create the main window
window = tk.Tk()
window.geometry("800x600")  # Set the desired window size
app = ScrollableApp(window)
window.mainloop()
