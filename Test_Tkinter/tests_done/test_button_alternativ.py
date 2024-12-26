import tkinter as tk

def on_enter(event):
    label_button.config(font=("Helvetica", 18, "bold"), fg="blue", bg="#FFD700")  # Increase font size and change color

def on_leave(event):
    label_button.config(font=("Helvetica", 14, "bold"), fg="black", bg="#FFDB58")  # Restore original style

def on_click(event):
    print("Label button clicked!")

root = tk.Tk()
root.geometry("400x300")

# Create a label that looks like a button
label_button = tk.Label(
    root,
    text="Click Me",
    font=("Helvetica", 14, "bold"),
    bg="#FFDB58",
    fg="black",
    padx=20,
    pady=10,
    cursor="hand2",  # Hand cursor for interactivity
    relief="raised",
)
label_button.pack(pady=50)

# Bind hover and click events
label_button.bind("<Enter>", on_enter)
label_button.bind("<Leave>", on_leave)
label_button.bind("<Button-1>", on_click)

root.mainloop()

