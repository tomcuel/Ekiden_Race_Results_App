from tkinter import *
# Create the main window
window = Tk()
window.title("Hello World")
window.geometry("1000x800")
window.config(background="#5cfaff")
# Icone de la fenêtre du programme
Icone_photo = PhotoImage(file="Capture d’écran 2024-11-02 à 18.40.18.png")
window.iconphoto(True, Icone_photo)



# Create a fixed header frame
header_frame = Frame(window, height=400, bg="#FFDB58")
header_frame.pack(side="top", fill="x")
# Add content to the header frame (e.g., labels or buttons)
header_label = Label(header_frame, text="Fixed Header Area", font=("Helvetica", 20), bg="#FFDB58")
header_label.pack(pady=0)
# Prevent the frame from resizing based on its contents
header_frame.pack_propagate(False)



# Ajouter une image
image_path = "Capture d’écran 2024-11-02 à 18.40.18.png"
def load_and_resize_image(image_path, new_width):
    # Load the image
    photo = PhotoImage(file=image_path)
    # Calculate new height to maintain aspect ratio
    new_height = int(photo.height() * (new_width / photo.width()))
    # Resize using the PhotoImage method
    resized_photo = photo.subsample(int(photo.width() / new_width), int(photo.height() / new_height))
    return resized_photo
resized_photo = load_and_resize_image(image_path, 600)
# Add the resized image to the header frame
image = Label(header_frame, image=resized_photo)
header_width = header_frame.winfo_width() * 1000
image_width = resized_photo.width()
image.place(x=(header_width - image_width) // 2, y=50)
# Ajouter un texte avec des effets dessus
label = Label(header_frame, text="Hello", font=('Arial', 40, 'bold'), fg='#00FF00', bg='black', relief=RAISED, bd=10, padx=20, pady=20)
label.place(x=0, y=0)



# Variable to keep track of the label widget
label = None
# Function to show or hide the label
def clicked():
    global label
    if label is None:
        # Create and display the label if it does not exist
        label = Label(header_frame, text="Button was clicked")
        label.config(font=('Arial', 20))
        label.place(x=800, y=200)
    else:
        # Destroy the label and set it to None if it exists
        label.destroy()
        label = None
button = Button(header_frame, text="Click me", command=clicked)
button.config(font=('Ink Free', 50, 'bold'), bg='#ff6200', fg='yellow', activebackground='brown', activeforeground='green')
button.pack()
button.place(x=800, y=0)



# Create a canvas widget for scrolling
# Create a canvas widget for scrolling
canvas = Canvas(window, highlightthickness=0, takefocus=False)  # Prevent canvas from taking focus
scroll_frame = Frame(canvas, bg="#5cfaff", highlightthickness=0, takefocus=False)  # Prevent frame from taking focus
# Configure a vertical scrollbar for the canvas
v_scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=v_scrollbar.set)
# Pack the canvas and scrollbar to fill the window
v_scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
# Create a window in the canvas to add widgets
canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")



# Create an entry widget with focus outline enabled
entry = Entry(scroll_frame, font=("Helvetica", 14), highlightthickness=2, highlightcolor="black")
entry.grid(row=0, column=0, padx=10, pady=10)
# Add submit and delete buttons
def submit():
    username = entry.get()
    print("Username: ", username)
def delete():
    entry.delete(0, END)
submitted = Button(scroll_frame, text="Submit", command=submit, highlightthickness=0)
submitted.grid(row=0, column=1, padx=10, pady=10, sticky="w")
deleted = Button(scroll_frame, text="Delete", command=delete, highlightthickness=0)
deleted.grid(row=0, column=2, padx=10, pady=10, sticky="w")
# Function to deselect entry when clicking outside
def on_click(event):
    if event.widget != entry:
        window.focus()
# Bind the click event to the window
window.bind("<Button-1>", on_click)


# Add buttons to the scrollable frame
for i in range(1, 31):
    button = Button(scroll_frame, text=f"Button {i}", command=lambda i=i: print(f"Button {i} clicked"))
    button.grid(row=i, column=0, padx=10, pady=5)
# Update the canvas scroll region when the frame size changes
scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
# Bind scrolling events for trackpad
def on_mouse_wheel(event):
    if event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")



# Bind the appropriate events for mouse scrolling
canvas.bind_all("<MouseWheel>", on_mouse_wheel)



window.mainloop()