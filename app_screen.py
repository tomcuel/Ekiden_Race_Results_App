# import the necessary libraries
import tkinter as tk

# import the class created in other files
from utility import Utility
from Data import Data_For_App


# Screen 3: class to show the main app screen where the results are displayed
class App_Screen(tk.Frame):

    # Initialize the App Screen
    def __init__(self, master, navigate_callback, window_width, data : Data_For_App):
        super().__init__(master, bg="#282c34", highlightthickness=0, borderwidth=0, border=0)
        self.navigate_callback = navigate_callback
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.datas = data
        self.window_width = window_width

# Header Section
        header_frame = tk.Frame(self, bg="#FFDB58", height=100, width = self.window_width)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

    # Home Icon Button

        self.logo = Utility.load_resized_image("Data/Pictures/App_Icon.png", 75, 75)
        logo_button = tk.Button(
            header_frame, image= self.logo, compound="left", border=0, highlightthickness=0
        )
        logo_button.place(x=100, y=header_frame.winfo_reqheight() // 2, anchor="center")  
        logo_button.bind("<Button-1>", self.reset_screen)

    # Home Label/Button
        home_button = tk.Label(
            header_frame, text="Home", font=("Helvetica", 40), bg="#FFDB58", border=0, highlightthickness=0
        )
        home_button.place(x=300, y=header_frame.winfo_reqheight() // 2, anchor="center") 
        home_button.bind("<Enter>", lambda event: home_button.config(font=("Helvetica", 50, "bold"), fg="#000000", bg="#FFDB58"))
        home_button.bind("<Leave>", lambda event: home_button.config(font=("Helvetica", 40), fg="#000000", bg="#FFDB58"))
        home_button.bind("<Button-1>", self.reset_screen)
        
    # Results Label/Button
        results_button = tk.Label(
            header_frame, text="Results", font=("Helvetica", 40), bg="#FFDB58", border=0, highlightthickness=0
        )
        results_button.place(x=600, y=header_frame.winfo_reqheight() // 2, anchor="center")
        results_button.bind("<Button-1>", self.show_results_menu)

    # Result Sub-Menu Buttons
        # utility functions
        def show_submenu(event=None):
            # Display the submenu when hovering over the results button.
            submenu.place(x=results_button.winfo_x(), y=results_button.winfo_y() + results_button.winfo_height())
            submenu.lift()
            for sub_button in submenu_buttons:
                sub_button.update_idletasks() # Ensure the text on buttons is refreshed immediately
            results_button.config(font=("Helvetica", 50, "bold")) # Result button bigger when submenu is showing
        def hide_submenu(event=None):
            # Hide the submenu if the mouse is not over the submenu or results button.
            widget_under_pointer = master.winfo_containing(event.x_root, event.y_root)
            if widget_under_pointer not in submenu.winfo_children() and widget_under_pointer != submenu and widget_under_pointer != results_button:
                submenu.place_forget()
            results_button.config(font=("Helvetica", 40)) # Result button smaller when submenu isn't showing

        # Submenu Frame with fixed size
        submenu = tk.Frame(master, bg="#FFDB58", relief="raised", border=0, highlightthickness=0, width=300, height=100)
        submenu.place_forget()

        # Add submenu buttons with place
        team_result_sub_button = tk.Label(
                submenu, text="Team Results",  font=("Helvetica", 30),  bg="#FFDB58", fg="#000000", padx=10, pady=5, anchor="center"
        )
        team_result_sub_button.place(x=0, y=0, relwidth=1, height=50)
        team_result_sub_button.bind("<Enter>", lambda event, b=team_result_sub_button: self.on_submenu_button_hover(event, b, True))
        team_result_sub_button.bind("<Leave>", lambda event, b=team_result_sub_button: self.on_submenu_button_hover(event, b, False))
        team_result_sub_button.bind("<Button-1>", self.show_team_results_sub_menu)
        indiv_result_sub_button = tk.Label(
                submenu, text="Individual Results", font=("Helvetica", 30), bg="#FFDB58", fg="#000000", padx=10, pady=5, anchor="center"
        )
        indiv_result_sub_button.place(x=0, y=50, relwidth=1, height=50)
        indiv_result_sub_button.bind("<Enter>", lambda event, b=indiv_result_sub_button: self.on_submenu_button_hover(event, b, True))
        indiv_result_sub_button.bind("<Leave>", lambda event, b=indiv_result_sub_button: self.on_submenu_button_hover(event, b, False))
        indiv_result_sub_button.bind("<Button-1>", self.show_individual_results_sub_menu)
        submenu_buttons = [team_result_sub_button, indiv_result_sub_button]

    # Bind events to the results and submenu buttons
        results_button.bind("<Enter>", show_submenu)
        results_button.bind("<Leave>", hide_submenu)
        submenu.bind("<Enter>", show_submenu)
        submenu.bind("<Leave>", hide_submenu)

    # Deconnexion Button
        # function to use the dismissable messagebox to ask the user if he really wants to deconnect
        def deconnexion(event=None):
            Utility.show_dismissable_messagebox(master, "Deconnexion", "Are you sure you want to deconnect?", lambda: self.navigate_callback(1), duration=4000, is_deconnexion_avorted=True)
        self.logout_image = Utility.load_resized_image("Data/Pictures/Log_Out.png", 40, 40)
        logout_button = tk.Button(
            header_frame, image=self.logout_image, border=0, highlightthickness=0, compound="center"
        )
        logout_button.place(x=self.window_width - 100, y=header_frame.winfo_reqheight() // 2, anchor="center")
        logout_button.bind("<Button-1>", deconnexion)

    # Search Bar
        self.search_var = tk.StringVar()
        search_bar = tk.Entry(
            header_frame, textvariable=self.search_var, font=("Helvetica", 20), background="#f7f7f7", highlightbackground="#282c34"
        )
        search_bar.place(x=self.window_width // 2 + 275, y=header_frame.winfo_reqheight() // 2, anchor="center")
        search_bar.bind("<Return>", self.perform_search)

    # Create the Scrollable Frame for Results
        self.scroll_canvas = tk.Canvas(self, bg="#282c34", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.scroll_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.config(yscrollcommand=scrollbar.set)
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    # Frame for fixed header content (hidden initially)
        self.results_header_frame = tk.Frame(self.scroll_canvas, bg="#282c34", height=40)
        self.results_header_window = self.scroll_canvas.create_window(
            (0, 0), window=self.results_header_frame, anchor="nw", width=self.scroll_canvas.winfo_width()
        )
        self.results_header_frame.pack_forget()
        header_labels = ["Rank", "Name", "Category", "Time", "Speed"]
        for index, header_text in enumerate(header_labels):
            tk.Label(
                self.results_header_frame, text=header_text, font=("Helvetica", 20), fg="#ffffff", bg="#282c34", anchor="w", padx=5
            ).grid(row=0, column=index, sticky="nsew")
        for col in range(len(header_labels)):
            self.results_header_frame.grid_columnconfigure(col, weight=1)

    # Frame for scrollable results
        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#282c34")
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
        )
        self.scroll_canvas.create_window((0, 40), window=self.scrollable_frame, anchor="nw")

    # Home page content
    # Title Text
        description_title_text = (
            "Welcome to the Ekiden App!"
        )
        self.description_title_label = tk.Label(
            self.scrollable_frame, text=description_title_text, font=("Helvetica", 30), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_title_label.pack(padx=(50,50), pady=(0,20))
        # Description Text
        description_ekiden_text = (
            "An Ekiden is a team relay race where runners work together to complete a marathon distance. \n"
            "Each runner takes a leg of a distance among 5km, 7.2km, or 10km for this one, handing off the team race number to the next teammate.\n\n"
            "This app helps you navigate through the results both for the tems and the individuals, explore the tools available to discover the different distance map, visualize data by clicking on one of the results buttons or search for a specific runner or team in the search bar."
        )
        self.description_ekiden_label = tk.Label(
            self.scrollable_frame, text=description_ekiden_text,font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_ekiden_label.pack(padx=(50,50), pady=(10,10))
        # two buttons to redirect to the team and individual results
    # Frame for result link Buttons
        self.button_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.button_frame.pack(pady=(10, 20),)
        # Buttons for Team Results in the Home Page
        home_page_team_results_button = tk.Label(
            self.button_frame, text="View Team Results", font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center", width = 20, height= 2
        )
        home_page_team_results_button.pack(padx=(50, 50), pady=(10, 10), side = "left")
        home_page_team_results_button.bind("<Enter>", lambda event, b=home_page_team_results_button: self.on_submenu_button_hover(event, b, True))
        home_page_team_results_button.bind("<Leave>", lambda event, b=home_page_team_results_button: self.on_submenu_button_hover(event, b, False))
        home_page_team_results_button.bind("<Button-1>", self.show_team_results_sub_menu)
        # Buttons for Individual Results in the Home Page
        home_page_individual_results_button = tk.Label(
            self.button_frame, text="View Individual Results", font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center", width = 20, height= 2
        )
        home_page_individual_results_button.pack(padx=(50, 50), pady=(10, 10), side = "right") 
        home_page_individual_results_button.bind("<Enter>", lambda event, b=home_page_individual_results_button: self.on_submenu_button_hover(event, b, True))
        home_page_individual_results_button.bind("<Leave>", lambda event, b=home_page_individual_results_button: self.on_submenu_button_hover(event, b, False))
        home_page_individual_results_button.bind("<Button-1>", self.show_individual_results_sub_menu)
    # Race map fo each distance
        # Load the images with the specified dimensions
        map_width, map_height = 425, 250
        self.short = Utility.load_resized_image("Data/Pictures/5k.png", map_width, map_height)
        self.medium = Utility.load_resized_image("Data/Pictures/7_2k.png", map_width, map_height)
        self.long = Utility.load_resized_image("Data/Pictures/10k.png", map_width, map_height)
        # Frame for Race Maps
        self.race_map_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.race_map_frame.pack(pady=(20, 20), fill="x", side="bottom", anchor="s")
        race_map_title = tk.Label(
            self.race_map_frame, text="Here are the different running courses:", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center"
        )
        race_map_title.pack(pady=(0, 10))
        # Sub-frame for map titles and images
        map_content_frame = tk.Frame(self.race_map_frame, bg="#282c34")
        map_content_frame.pack()
        # Short Map Group
        short_map_group = tk.Frame(map_content_frame, bg="#282c34")
        short_map_group.pack(side="left", padx=20)
        short_title = tk.Label(
            short_map_group, text="5 km", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF"
        )
        short_title.pack()
        short_map_label = tk.Label(short_map_group, image=self.short, bg="#282c34")
        short_map_label.pack()
        # Medium Map Group
        medium_map_group = tk.Frame(map_content_frame, bg="#282c34")
        medium_map_group.pack(side="left", padx=20)
        medium_title = tk.Label(
            medium_map_group, text="7.2 km", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF"
        )
        medium_title.pack()
        medium_map_label = tk.Label(medium_map_group, image=self.medium, bg="#282c34")
        medium_map_label.pack()
        # Long Map Group
        long_map_group = tk.Frame(map_content_frame, bg="#282c34")
        long_map_group.pack(side="left", padx=20)
        long_title = tk.Label(
            long_map_group, text="10 km", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF"
        )
        long_title.pack()
        long_map_label = tk.Label(long_map_group, image=self.long, bg="#282c34")
        long_map_label.pack()

    # function to show the results menu in the scrollable frame
    def show_results_menu(self, event=None):   
                # Clear previous results or placeholder text
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # Hide the results header
        self.results_header_frame.pack_forget()

        # Create a frame for organizing the buttons in a grid
        button_grid_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        button_grid_frame.pack(pady=(10, 20), padx=(225, 225), fill="x", anchor="center")
        # Add grid column configurations to ensure buttons are centered
        button_grid_frame.grid_columnconfigure(0, weight=1)
        button_grid_frame.grid_columnconfigure(1, weight=1)
        button_grid_frame.grid_columnconfigure(2, weight=1)
        # creating the 4 buttons for the team results
        team_results_label = tk.Label(
            button_grid_frame, text="Team Results", font=("Helvetica", 30, "bold"), bg="#FFDB58", fg="#000000", anchor="center"
        )
        team_results_label.grid(row=0, column=0, columnspan=3, padx=(50, 50), pady=(20, 10), sticky="nsew")
        # overall scratch 
        overall_team_results_button = tk.Button(
            button_grid_frame, text="Overall", font=("Helvetica", 20), fg="#000000", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda s=self.datas.team_type.UNKOWN: self.show_team_results(s, False, "")
        )
        overall_team_results_button.grid(row=1, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        # men
        men_team_results_button = tk.Button(
            button_grid_frame, text="Men", font=("Helvetica", 20), fg="#000000", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda s=self.datas.team_type.MEN: self.show_team_results(s, False, "")
        )
        men_team_results_button.grid(row=2, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")
        # mixed
        mixed_team_results_button = tk.Button(
            button_grid_frame, text="Mixed", font=("Helvetica", 20), fg="#000000", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda s=self.datas.team_type.MIXED: self.show_team_results(s, False, "")
        )
        mixed_team_results_button.grid(row=2, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        # women
        women_team_results_button = tk.Button(
            button_grid_frame, text="Women", font=("Helvetica", 20), fg="#000000", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda s=self.datas.team_type.WOMEN: self.show_team_results(s, False, "")
        )
        women_team_results_button.grid(row=2, column=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
        # creating the 3 buttons for the individuals results
        team_results_label = tk.Label(
            button_grid_frame, text="Individuals Results", font=("Helvetica", 30, "bold"), bg="#FFDB58", fg="#000000", anchor="center"
        )
        team_results_label.grid(row=3, column=0, columnspan=3, padx=(50, 50), pady=(70, 10), sticky="nsew")
        # making an array of the buttons infos and labels
        button_and_label_names = [["5km", "Men", "Scratch","Women"], 
                                  ["7.2km", "Men", "Scratch","Women"],
                                  ["10km", "Men", "Scratch","Women"]]
        button_and_sex_infos = [[5, self.datas.team_type.MEN, self.datas.team_type.MIXED, self.datas.team_type.WOMEN],
                                [7.2, self.datas.team_type.MEN, self.datas.team_type.MIXED, self.datas.team_type.WOMEN],
                                [10, self.datas.team_type.MEN, self.datas.team_type.MIXED, self.datas.team_type.WOMEN]]
        # Iterate through the button_and_label_names and button_and_sex_infos
        for row_index, (texts, infos) in enumerate(zip(button_and_label_names, button_and_sex_infos)):
            # Create a label for the distance
            distance_label = tk.Label(
                button_grid_frame,text=texts[0], font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center"
            )
            distance_label.grid(row=3+2*row_index+1, column=0, columnspan=3, padx=(50, 50), pady=(10, 10), sticky="nsew")
            # Create buttons for Men, Mixed, and Women
            for col_index, (button_name, sex_info) in enumerate(zip(texts[1:], infos[1:])):
                button = tk.Button(
                    button_grid_frame, text=button_name, font=("Helvetica", 20), fg="#000000", bg="#FFDB58", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
                    command=lambda d=infos[0], s=sex_info: self.show_individual_results(d, s, False, "")
                )
                button.grid(row=3+2*row_index+2, column=col_index, padx=(20, 20), pady=(10, 10), sticky="nsew")

    # function to show the team results submenu in the scrollable frame
    def show_team_results_sub_menu(self, event=None):
                # Clear previous results or placeholder text
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # Hide the results header
        self.results_header_frame.pack_forget()

        # Create a frame for organizing the buttons in a grid
        button_grid_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        button_grid_frame.pack(pady=(10, 20), padx=(225, 225), fill="x", anchor="center")
        # Add grid column configurations to ensure buttons are centered
        button_grid_frame.grid_columnconfigure(0, weight=1)
        button_grid_frame.grid_columnconfigure(1, weight=1)
        button_grid_frame.grid_columnconfigure(2, weight=1)
        # creating the 4 buttons for the team results
        team_results_label = tk.Label(
            button_grid_frame, text="Team Results", font=("Helvetica", 30, "bold"), bg="#FFDB58", fg="#000000", anchor="center"
        )
        team_results_label.grid(row=0, column=0, columnspan=3, padx=(50, 50), pady=(20, 10), sticky="nsew")
        # overall scratch 
        overall_team_results_button = tk.Button(
            button_grid_frame, text="Overall", font=("Helvetica", 20), fg="#000000", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda s=self.datas.team_type.UNKOWN: self.show_team_results(s, True, "")
        )
        overall_team_results_button.grid(row=1, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        # men
        men_team_results_button = tk.Button(
            button_grid_frame, text="Men", font=("Helvetica", 20), fg="#000000", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5, 
            command=lambda s=self.datas.team_type.MEN: self.show_team_results(s, False, "")
        )
        men_team_results_button.grid(row=2, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")
        # mixed
        mixed_team_results_button = tk.Button(
            button_grid_frame, text="Mixed", font=("Helvetica", 20), fg="#000000", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda s=self.datas.team_type.MIXED: self.show_team_results(s, False, "")
        )
        mixed_team_results_button.grid(row=2, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        # women
        women_team_results_button = tk.Button(
            button_grid_frame, text="Women", font=("Helvetica", 20), fg="#000000", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
            command=lambda s=self.datas.team_type.WOMEN: self.show_team_results(s, False, "")
        )
        women_team_results_button.grid(row=2, column=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
    
    # function to show the individual results submenu in the scrollable frame
    def show_individual_results_sub_menu(self, event=None):
                # Clear previous results or placeholder text
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # Hide the results header
        self.results_header_frame.pack_forget()

        # Create a frame for organizing the buttons in a grid
        button_grid_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        button_grid_frame.pack(pady=(10, 20), padx=(225, 225), fill="x", anchor="center")
        # Add grid column configurations to ensure buttons are centered
        button_grid_frame.grid_columnconfigure(0, weight=1)
        button_grid_frame.grid_columnconfigure(1, weight=1)
        button_grid_frame.grid_columnconfigure(2, weight=1)
        # creating the 3 buttons for the individuals results
        team_results_label = tk.Label(
            button_grid_frame, text="Individuals Results", font=("Helvetica", 30, "bold"), bg="#FFDB58", fg="#000000", anchor="center"
        )
        team_results_label.grid(row=2, column=0, columnspan=3, padx=(50, 50), pady=(70, 10), sticky="nsew")
        # making an array of the buttons infos and labels
        button_and_label_names = [["5km", "Men", "Scratch","Women"], 
                                  ["7.2km", "Men", "Scratch","Women"],
                                  ["10km", "Men", "Scratch","Women"]]
        button_and_sex_infos = [[5, self.datas.team_type.MEN, self.datas.team_type.MIXED, self.datas.team_type.WOMEN],
                                [7.2, self.datas.team_type.MEN, self.datas.team_type.MIXED, self.datas.team_type.WOMEN],
                                [10, self.datas.team_type.MEN, self.datas.team_type.MIXED, self.datas.team_type.WOMEN]]
        # Iterate through the button_and_label_names and button_and_sex_infos
        for row_index, (texts, infos) in enumerate(zip(button_and_label_names, button_and_sex_infos)):
            # Create a label for the distance
            distance_label = tk.Label(
                button_grid_frame,text=texts[0], font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center"
            )
            distance_label.grid(row=3+2*row_index, column=0, columnspan=3, padx=(50, 50), pady=(10, 10), sticky="nsew")
            # Create buttons for Men, Mixed, and Women
            for col_index, (button_name, sex_info) in enumerate(zip(texts[1:], infos[1:])):
                button = tk.Button(
                    button_grid_frame, text=button_name, font=("Helvetica", 20), fg="#000000", bg="#FFDB58", anchor="center", width=20, height=2, relief="flat", activeforeground="#ff0000", border=0, highlightthickness=2.5,
                    command=lambda d=infos[0], s=sex_info: self.show_individual_results(d, s, False, "")
                )
                button.grid(row=3+2*row_index+1, column=col_index, padx=(20, 20), pady=(10, 10), sticky="nsew")

    # Function to format time in hh:mm format
    def format_time(self, value):
        hours = int(value // 3600)
        minutes = int((value % 3600) // 60)
        return f"{hours:02d}h{minutes:02d}"

    # function to show the team results in the scrollable frame with the associated graphics (use in the submenu button or the perfom search results)
    def show_team_results(self, sex, is_by_name : bool, name : str):
        # Clear previous results or placeholder text
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.results_header_frame.pack(fill="x", side="top")

        # getting the pictures and the teams
        picture_width, picture_height = 400, 300
        teams = None
        # Search by category
        if not is_by_name: 
            # getting the graph of the category
            self.team_graph = Utility.load_resized_image("Data/Precomputed_graphs/men_team_result.png", picture_width, picture_height)
            if sex == self.datas.team_type.MIXED: 
                self.team_graph = Utility.load_resized_image("Data/Precomputed_graphs/mixed_team_result.png", picture_width, picture_height)
            elif sex == self.datas.team_type.WOMEN: 
                self.team_graph = Utility.load_resized_image("Data/Precomputed_graphs/women_team_result.png", picture_width, picture_height)
            elif sex == self.datas.team_type.UNKOWN:
                self.team_graph = Utility.load_resized_image("Data/Precomputed_graphs/overall_team_result.png", picture_width, picture_height)
            team_graph_label = tk.Label(self.scrollable_frame, image=self.team_graph, bg="#282c34")
            team_graph_label.grid(row=0, column=0, columnspan=5, pady=(20, 10), sticky="nsew")
            # getting the teams of the category
            teams = self.datas.get_teams_by_category(sex)
        # Search by name
        else : 
            # getting the graph of the category
            fig_1, fig_2 = self.datas.create_data_graphs(name, 0, sex, True)
            self.team_graph_1 = Utility.load_resized_image(fig_1, picture_width, picture_height)
            self.team_graph_2 = Utility.load_resized_image(fig_2, picture_width, picture_height)
            # Create two labels for the graphs, placed side by side
            team_graph_label_1 = tk.Label(self.scrollable_frame, image=self.team_graph_1, bg="#282c34")
            team_graph_label_1.grid(row=0, column=0, pady=(20, 10), sticky="nsew", columnspan=2)
            blanc_label = tk.Label(self.scrollable_frame, text="", bg="#282c34")
            blanc_label.grid(row=0, column=2, pady=(20, 10), sticky="nsew")
            team_graph_label_2 = tk.Label(self.scrollable_frame, image=self.team_graph_2, bg="#282c34")
            team_graph_label_2.grid(row=0, column=3, pady=(20, 10), sticky="nsew", columnspan=2)
            # getting the teams of the category
            teams = self.datas.get_teams_by_category_by_name(name)
            
        # sorting the teams by time
        teams.sort(key=lambda team: team.data[self.datas.field.TEAM_TIME])
        
        # searching the team to apply a yellow background on its index
        if is_by_name : 
            team_searched = self.datas.get_team(name)
            team_searched_index = teams.index(team_searched)

        # Fixed cell dimensions
        cell_width = [200, 500, 100, 300, 300]  # Fixed cell width
        cell_height = 40  # Fixed cell height
        # Display results in a tabular format
        for idx, team in enumerate(teams, start=1):
            formatted_time = self.format_time(team.data[self.datas.field.TEAM_TIME])
            team_info = [
                idx, 
                team.data[self.datas.field.TEAM_NAME],
                team.data[self.datas.field.TEAM_CATEGORY].name,
                formatted_time,
                (1000 * 3600 * 42.195 // team.data[self.datas.field.TEAM_TIME]) / 1000 if team.data[self.datas.field.TEAM_TIME] != 0 else 0
            ]

            for col, text in enumerate(team_info): # Create a fixed-size frame for each cell
                cell_frame = tk.Frame(
                    self.scrollable_frame, width=cell_width[col], height=cell_height, bg="#f7f7f7" if idx % 2 == 0 else "#ffffff"
                )
                if is_by_name and idx == team_searched_index + 1: # Apply a yellow background to the searched team
                    cell_frame.configure(bg="#FFDB58")
                cell_frame.grid(row=idx + 1, column=col, sticky="nsew")
                cell_frame.grid_propagate(False)
                cell_label = tk.Label(
                    cell_frame, text=text, font=("Helvetica", 12), bg="#f7f7f7" if idx % 2 == 0 else "#ffffff", anchor="center"
                )
                if is_by_name and idx == team_searched_index + 1: # Apply a yellow background to the searched team
                    cell_label.configure(bg="#FFDB58")
                cell_label.pack(fill="both", expand=True)

            # Configure columns and rows to ensure fixed layout
            for col in range(len(team_info)):
                self.scrollable_frame.grid_columnconfigure(col, minsize= cell_width[col])
        for row in range(1, len(teams) + 2):  # Include the header
            self.scrollable_frame.grid_rowconfigure(row, minsize=cell_height)
          
    # function to show the individual results in the scrollable frame with the associated graphics (use in the submenu button or the perfom search results)
    def show_individual_results(self, distance, sex, is_by_name, name):
        # Clear previous results or placeholder text
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.results_header_frame.pack(fill="x", side="top")

        # getting the pictures and the teams
        picture_width, picture_height = 400, 300
        distance_runners = None
        # Search by category
        if not is_by_name: 
            # getting the graph of the category
            # for a 5km distance
            self.individual_graph = Utility.load_resized_image("Data/Precomputed_graphs/men_5km_result.png", picture_width, picture_height)
            if sex == self.datas.team_type.MIXED: 
                self.team_graph = Utility.load_resized_image("Data/Precomputed_graphs/overall_5km_result.png", picture_width, picture_height)
            elif sex == self.datas.team_type.WOMEN: 
                self.team_graph = Utility.load_resized_image("Data/Precomputed_graphs/women_5km_result.png", picture_width, picture_height)
            # for a 7.2km distance
            if distance == 7.2:
                if sex == self.datas.team_type.MEN:
                    self.individual_graph = Utility.load_resized_image("Data/Precomputed_graphs/men_7_2km_result.png", picture_width, picture_height)
                if sex == self.datas.team_type.MIXED:
                    self.individual_graph = Utility.load_resized_image("Data/Precomputed_graphs/overall_7_2km_result.png", picture_width, picture_height)
                elif sex == self.datas.team_type.WOMEN: 
                    self.individual_graph = Utility.load_resized_image("Data/Precomputed_graphs/women_7_2km_result.png", picture_width, picture_height)
            # for a 10km distance
            if distance == 10:
                if sex == self.datas.team_type.MEN:
                    self.individual_graph = Utility.load_resized_image("Data/Precomputed_graphs/men_10km_result.png", picture_width, picture_height)
                if sex == self.datas.team_type.MIXED:
                    self.individual_graph = Utility.load_resized_image("Data/Precomputed_graphs/overall_10km_result.png", picture_width, picture_height)
                elif sex == self.datas.team_type.WOMEN: 
                    self.individual_graph = Utility.load_resized_image("Data/Precomputed_graphs/women_10km_result.png", picture_width, picture_height)
            individual_graph_label = tk.Label(self.scrollable_frame, image=self.individual_graph, bg="#282c34")
            individual_graph_label.grid(row=0, column=0, columnspan=5, pady=(20, 10), sticky="nsew")
            # getting the runners of the distance
            distance_runners = self.datas.Distance_Relay.get_distance_relay(self.datas, "", distance, sex)
        # Search by name
        else : 
            # getting the graph of the category
            fig_1, fig_2 = self.datas.create_data_graphs(name, distance, sex, False)
            self.team_graph_1 = Utility.load_resized_image(fig_1, picture_width, picture_height)
            self.team_graph_2 = Utility.load_resized_image(fig_2, picture_width, picture_height)
            # Create two labels for the graphs, placed side by side
            individual_graph_label_1 = tk.Label(self.scrollable_frame, image=self.team_graph_1, bg="#282c34")
            individual_graph_label_1.grid(row=0, column=0, pady=(20, 10), sticky="nsew", columnspan=2)
            blanc_label = tk.Label(self.scrollable_frame, text="", bg="#282c34")
            blanc_label.grid(row=0, column=2, pady=(20, 10), sticky="nsew")
            individual_graph_label_2 = tk.Label(self.scrollable_frame, image=self.team_graph_2, bg="#282c34")
            individual_graph_label_2.grid(row=0, column=3, pady=(20, 10), sticky="nsew", columnspan=2)
            # getting the runners of the distance
            distance_runners = self.datas.Distance_Relay.get_distance_relay(self.datas, name, distance, sex)

        # sorting the teams by time
        distance_runners.sort(key=lambda runner: runner.speed, reverse=True)
        
        # searching the team to apply a yellow background on its index
        if is_by_name : 
            runner_searched = self.datas.Distance_Relay.get_runner_by_name(self.datas, name)
            runner_searched_index = distance_runners.index(runner_searched)
        
        # Fixed cell dimensions
        cell_width = [200, 500, 100, 300, 300]  # Fixed cell width
        cell_height = 40  # Fixed cell height
        # Display results in a tabular format
        for idx, runner in enumerate(distance_runners, start=1):
            formatted_time = self.format_time(distance / runner.speed * 3600 if runner.speed != 0 else 0)
            runner_info = [
                idx, 
                runner.name,
                runner.sex.name,
                formatted_time,
                runner.speed
            ]

            for col, text in enumerate(runner_info): # Create a fixed-size frame for each cell
                cell_frame = tk.Frame(
                    self.scrollable_frame, width=cell_width[col], height=cell_height, bg="#f7f7f7" if idx % 2 == 0 else "#ffffff"
                )
                if is_by_name and idx == runner_searched_index + 1: # Apply a yellow background to the searched runner
                    cell_frame.configure(bg="#FFDB58")
                cell_frame.grid(row=idx + 1, column=col, sticky="nsew")
                cell_frame.grid_propagate(False)
                cell_label = tk.Label(
                    cell_frame, text=text, font=("Helvetica", 12), bg="#f7f7f7" if idx % 2 == 0 else "#ffffff", anchor="center"
                )
                if is_by_name and idx == runner_searched_index + 1: # Apply a yellow background to the searched runner
                    cell_label.configure(bg="#FFDB58")
                cell_label.pack(fill="both", expand=True)

            # Configure columns and rows to ensure fixed layout
            for col in range(len(runner_info)):
                self.scrollable_frame.grid_columnconfigure(col, minsize= cell_width[col])
        for row in range(1, len(distance_runners) + 2):  # Include the header
            self.scrollable_frame.grid_rowconfigure(row, minsize=cell_height)
        
    # function to make the search and display the results in the scrollable frame
    def perform_search(self, event=None):
        # Clear previous results or placeholder text
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.results_header_frame.pack(fill="x", side="top")

        # getting the name of a team or a runner given in the search bar
        search_query = self.search_var.get().strip()
        if search_query != "":
            # first looking if the search query is a team name
            is_team_name = False
            is_runner_name = False
            team_searched = self.datas.get_team(search_query)
            if team_searched is not None:
                is_team_name = True
            # then if it's not a team name, we look if it's a runner name
            runner_searched = self.datas.Distance_Relay.get_runner_by_name(self.datas, search_query)
            if not is_team_name and runner_searched is not None:
                is_runner_name = True
            
            # if the search query is a team name, then we show the team results according to the category of the team
            if is_team_name :
                self.show_team_results(team_searched.data[self.datas.field.TEAM_CATEGORY], True, search_query)
            # if the search query is a runner name, then we show the individual results according to the category of the runner
            elif is_runner_name :
                self.show_individual_results(runner_searched.distance, runner_searched.sex, True, search_query)
        
    # reset the scollable frame to its initial state (the text and gpx preview)
    def reset_screen(self, event=None):
        # Clear the search bar
        self.search_var.set("")

        # Clear previous results or placeholder text
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # Hide the results header
        self.results_header_frame.pack_forget()

        # Main text, shown at the start --> recreate here 
        # Title Text
        description_title_text = (
            "Welcome to the Ekiden App!"
        )
        self.description_title_label = tk.Label(
            self.scrollable_frame, text=description_title_text, font=("Helvetica", 30), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_title_label.pack(padx=(50,50), pady=(0,20))
        # Description Text
        description_ekiden_text = (
            "An Ekiden is a team relay race where runners work together to complete a marathon distance. \n"
            "Each runner takes a leg of a distance among 5km, 7.2km, or 10km for this one, handing off the team race number to the next teammate.\n\n"
            "This app helps you navigate through the results both for the tems and the individuals, explore the tools available to discover the different distance map, visualize data by clicking on one of the results buttons or search for a specific runner or team in the search bar."
        )
        self.description_ekiden_label = tk.Label(
            self.scrollable_frame, text=description_ekiden_text,font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center", wraplength=self.window_width-100
        )
        self.description_ekiden_label.pack(padx=(50,50), pady=(10,10))
        # two buttons to redirect to the team and individual results
    # Frame for result link Buttons
        self.button_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.button_frame.pack(pady=(10, 20),)
        # Buttons for Team Results in the Home Page
        home_page_team_results_button = tk.Label(
            self.button_frame, text="View Team Results", font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center", width = 20, height= 2
        )
        home_page_team_results_button.pack(padx=(50, 50), pady=(10, 10), side = "left")
        home_page_team_results_button.bind("<Enter>", lambda event, b=home_page_team_results_button: self.on_submenu_button_hover(event, b, True))
        home_page_team_results_button.bind("<Leave>", lambda event, b=home_page_team_results_button: self.on_submenu_button_hover(event, b, False))
        home_page_team_results_button.bind("<Button-1>", self.show_team_results_sub_menu)
        # Buttons for Individual Results in the Home Page
        home_page_individual_results_button = tk.Label(
            self.button_frame, text="View Individual Results", font=("Helvetica", 20), bg="#FFDB58", fg="#000000", anchor="center", width = 20, height= 2
        )
        home_page_individual_results_button.pack(padx=(50, 50), pady=(10, 10), side = "right") 
        home_page_individual_results_button.bind("<Enter>", lambda event, b=home_page_individual_results_button: self.on_submenu_button_hover(event, b, True))
        home_page_individual_results_button.bind("<Leave>", lambda event, b=home_page_individual_results_button: self.on_submenu_button_hover(event, b, False))
        home_page_individual_results_button.bind("<Button-1>", self.show_individual_results_sub_menu)
    # Race map fo each distance
        # Load the images with the specified dimensions
        map_width, map_height = 425, 250
        self.short = Utility.load_resized_image("Data/Pictures/5k.png", map_width, map_height)
        self.medium = Utility.load_resized_image("Data/Pictures/7_2k.png", map_width, map_height)
        self.long = Utility.load_resized_image("Data/Pictures/10k.png", map_width, map_height)
        # Frame for Race Maps
        self.race_map_frame = tk.Frame(self.scrollable_frame, bg="#282c34")
        self.race_map_frame.pack(pady=(20, 20), fill="x", side="bottom", anchor="s")
        race_map_title = tk.Label(
            self.race_map_frame, text="Here are the different running courses:", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF", anchor="center"
        )
        race_map_title.pack(pady=(0, 10))
        # Sub-frame for map titles and images
        map_content_frame = tk.Frame(self.race_map_frame, bg="#282c34")
        map_content_frame.pack()
        # Short Map Group
        short_map_group = tk.Frame(map_content_frame, bg="#282c34")
        short_map_group.pack(side="left", padx=20)
        short_title = tk.Label(
            short_map_group, text="5 km", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF"
        )
        short_title.pack()
        short_map_label = tk.Label(short_map_group, image=self.short, bg="#282c34")
        short_map_label.pack()
        # Medium Map Group
        medium_map_group = tk.Frame(map_content_frame, bg="#282c34")
        medium_map_group.pack(side="left", padx=20)
        medium_title = tk.Label(
            medium_map_group, text="7.2 km", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF"
        )
        medium_title.pack()
        medium_map_label = tk.Label(medium_map_group, image=self.medium, bg="#282c34")
        medium_map_label.pack()
        # Long Map Group
        long_map_group = tk.Frame(map_content_frame, bg="#282c34")
        long_map_group.pack(side="left", padx=20)
        long_title = tk.Label(
            long_map_group, text="10 km", font=("Helvetica", 20), bg="#282c34", fg="#FFFFFF"
        )
        long_title.pack()
        long_map_label = tk.Label(long_map_group, image=self.long, bg="#282c34")
        long_map_label.pack()
      
        # Scroll back to the top of the canvas (not needed here, but still useful to do in case)
        self.scroll_canvas.yview_moveto(0)
       
    # handle mouse wheel scrolling
    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    # handle making a button bigger when hovering with the mouse over it
    def on_submenu_button_hover(self, event, button, is_entering):
        # Change visuals when hovering over submenu buttons.
        if is_entering:
            button.config(font=("Helvetica", 30, "bold"))
        else:
            button.config(font=("Helvetica", 20))
    