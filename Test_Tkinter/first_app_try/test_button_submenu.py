import tkinter as tk

def show_submenu(event):
    """Display the submenu when hovering over the main button."""
    submenu.place(x=label_button.winfo_x(), y=label_button.winfo_y() + label_button.winfo_height())
    submenu.lift()  # Ensure the submenu is on top
    for sub_button in submenu_buttons:
        sub_button.update_idletasks()  # Ensure the text on buttons is refreshed immediately

def hide_submenu(event):
    """Hide the submenu only if the mouse is outside both the main button and the submenu."""
    widget_under_pointer = root.winfo_containing(event.x_root, event.y_root)
    if widget_under_pointer not in submenu.winfo_children() and widget_under_pointer != submenu and widget_under_pointer != label_button:
        submenu.place_forget()

def on_submenu_button_click(option):
    """Handle clicks on submenu options."""
    print(f"Submenu Option {option} clicked!")

def on_sub_button_hover(event, button, is_entering):
    """Change visuals when hovering over submenu buttons."""
    if is_entering:
        button.config(bg="#FFD700", fg="blue")
    else:
        button.config(bg="#FFDB58", fg="black")

root = tk.Tk()
root.geometry("400x300")

# Main Label Button
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

# Submenu Frame
submenu = tk.Frame(root, bg="#FFD700", relief="raised", borderwidth=2)
submenu.place_forget()  # Initially hidden

# Add labels to the submenu
submenu_buttons = []
for i in range(3):
    sub_button = tk.Label(
        submenu,
        text=f"Option {i+1}",
        font=("Helvetica", 12),
        bg="#FFDB58",
        fg="black",
        padx=10,
        pady=5,
        cursor="hand2",
        relief="flat",  # Flat style for visual consistency
    )
    sub_button.pack(fill="x", padx=5, pady=2)
    sub_button.bind("<Enter>", lambda event, b=sub_button: on_sub_button_hover(event, b, True))
    sub_button.bind("<Leave>", lambda event, b=sub_button: on_sub_button_hover(event, b, False))
    sub_button.bind("<Button-1>", lambda event, option=i+1: on_submenu_button_click(option))
    submenu_buttons.append(sub_button)

# Bind events to the main label button
label_button.bind("<Enter>", show_submenu)
label_button.bind("<Leave>", hide_submenu)

# Bind events to the submenu itself
submenu.bind("<Enter>", lambda event: submenu.lift())
submenu.bind("<Leave>", hide_submenu)

root.mainloop()
