import re
import sys
import tkinter as tk
from user import User
from pitch import Pitch
from xg_model import xG_Model
from feature_calculation import Feature_Calculation
from db_setup import get_connection, find_user, add_user, check_email_exist, recent_sims

#Input validation for the login screen and create account screen are defined outside the class because it can be recycled for both pages
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}$")


def email_error(email):
    #checks if the email entered is valid or not
    if len(email) > 254 or '..' in email or not EMAIL_PATTERN.match(email) :
        return 'Please enter a valid email'
    return None


def password_error(password):
    # for creating account, checks whether the password fits the requirements
    missing = []
    if len(password) < 8: missing.append('8+ characters')
    if not any(c.isalpha() for c in password): missing.append('a letter')
    if not any(c.isdigit() for c in password): missing.append('a number')
    if not any(not c.isalnum() and not c.isspace() for c in password): missing.append('a symbol')
    return ('Password needs: ' + ', '.join(missing)) if missing else None


class Application:
    def __init__(self):
        self.__root = None
        self.__container = None
        self.__current_user = None # User attribute
        self.__pitch = Pitch() # Pitch attribute
        self.__simulation = None # Simulation_Input for the play being built
        self.__model = xG_Model('model.pkl') # XGModel, loaded once at startup
        self.__calculator = Feature_Calculation('scaler.pkl') # FeatureCalculation, loaded once at startup
        self.__renderer = None # DefenderRender, built once self.pitch exists
        self.__manager = None # ManageSimulation
        self.__display = None # ResultsDisplay, built per results screen
        self.__db_connection = None

        # main colours and design of the application
        self.__colour1 = '#F9F9F9'
        self.__colour2 = '#129439'
        self.__colour2_dark = '#0C6E2A'
        self.__text = '#14201A'
        self.__muted = '#66756B'
        self.__border = '#DDE3DF'
        self.__error = '#C62828'
        self.__font = 'Helvetica Neue' if sys.platform == 'darwin' else 'Helvetica'
        self.__hand = 'pointinghand' if sys.platform == 'darwin' else 'hand2'

    def start(self):
        # Loads model and scaler, initialises the tkinter root window and navigates to the login screen
        self.__root = tk.Tk()
        self.__root.title('xG Calculator')
        self.__root.geometry('420x520')
        self.__root.minsize(360, 460)
        self.__root.resizable(True, True)
        self.__root.configure(bg=self.__colour1)
        self.__db_connection = get_connection()
        self.__container = tk.Frame(self.__root, bg=self.__colour1)
        self.__container.pack(fill='both', expand=True)
        self.login_screen()
        self.__root.mainloop()

    def clear_container(self):
        # Destroys every widget currently in self.container
        # Called at the top of every screen method
        for widget in self.__container.winfo_children():
            widget.destroy()

    # reusable widgets to the style of the application
    def __entry(self, parent, show=None):
        return tk.Entry(parent, show=show or '', font=(self.__font, 14), bg='white', fg=self.__text,
                        relief='flat', bd=0, highlightthickness=1, highlightbackground=self.__border,
                        highlightcolor=self.__colour2, insertbackground=self.__text)

    def __button(self, parent, text, command):
        btn = tk.Label(parent, text=text, font=(self.__font, 14, 'bold'), bg=self.__colour2,
                       fg='white', pady=10, cursor=self.__hand)
        btn.bind('<Button-1>', lambda event: command())
        btn.bind('<Enter>', lambda event: btn.configure(bg=self.__colour2_dark))
        btn.bind('<Leave>', lambda event: btn.configure(bg=self.__colour2))
        return btn

    def __dropdown(self, parent, options, default=None, command=None):
        placeholder = 'Select option'
        var = tk.StringVar(value=placeholder)

        box = tk.Frame(parent, bg='white', highlightthickness=1, highlightbackground=self.__border,
                       cursor=self.__hand)
        value = tk.Label(box, textvariable=var, font=(self.__font, 14), bg='white',
                         fg=self.__border, anchor='w', padx=8, pady=4)
        arrow = tk.Label(box, text='▾', font=(self.__font, 14), bg='white',
                         fg=self.__colour2, padx=8)
        value.pack(side='left', fill='x', expand=True)
        arrow.pack(side='right')

        menu = tk.Menu(box, tearoff=0, font=(self.__font, 14))

        def select(option):
            var.set(option)
            if command:
                command(option)

        for option in options:
            menu.add_command(label=option, command=lambda o=option: select(o))

        def open_menu(event):
            menu.tk_popup(box.winfo_rootx(), box.winfo_rooty() + box.winfo_height())

        for widget in (box, value, arrow):
            widget.bind('<Button-1>', open_menu)
            widget.bind('<Enter>', lambda event: box.configure(highlightbackground=self.__colour2))
            widget.bind('<Leave>', lambda event: box.configure(highlightbackground=self.__border))

        box.get = lambda: '' if var.get()==placeholder else var.get()
        return box

    def __set_window_size(self, width, height):
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        # never makes the window bigger than the screen (leaves room for the menu bar and dock)
        width = min(width, screen_width)
        height = min(height, screen_height - 80)
        # works out the position that puts the window in the middle of the screen
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.__root.geometry(f'{width}x{height}+{x}+{y}')


    # ---------- screens ----------
    def login_screen(self):
        self.clear_container()
        card = tk.Frame(self.__container, bg=self.__colour1)
        card.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8)

        #adds heading and title text
        tk.Label(card, text='xG Calculator', font=(self.__font, 24, 'bold'),
                 bg=self.__colour1, fg=self.__colour2).pack(pady=(0, 4))
        tk.Label(card, text='Log in to continue', font=(self.__font, 12),
                 bg=self.__colour1, fg=self.__muted).pack(pady=(0, 20))

        #entry boxes
        tk.Label(card, text='Email', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        email_entry = self.__entry(card)
        email_entry.pack(fill='x', ipady=6, pady=(2, 12))

        tk.Label(card, text='Password', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        password_entry = self.__entry(card, show='•')
        password_entry.pack(fill='x', ipady=6, pady=(2, 8))

        #label for when verification error comes up, above the login button
        error_label = tk.Label(card, text='', font=(self.__font, 11), bg=self.__colour1,
                               fg=self.__error, wraplength=300, justify='left', anchor='w')
        error_label.pack(fill='x', pady=(0, 8))

        #This function is run when login button is pressed, to validate what the user enters
        def attempt_login():
            email = email_entry.get().strip()
            password = password_entry.get()
            #if a field is empty an error message is returned
            if not email or not password:
                error_label.config(text='Fields cannot be empty')
                return
            #checks for email errors, if there is an error, message is displayed accordingly
            problem = email_error(email)
            if problem:
                error_label.config(text=problem)
                return
            #if passed the two tests before, then tries to locate the User from the Users table in the database
            try:
                found = find_user(self.__db_connection, email, password)
            #if there is a connection problem with the database, will display error message
            except Exception as error:
                print('LOGIN ERROR:', repr(error))
                error_label.config(text='Could not reach the database, please try again')
                return
            #if User with matching email and password not found, will display error message
            if not found:
                error_label.config(text='Invalid email or password')
                return
            user = User(*found)          # User(userID, name, email) - matches user entry
            self.__current_user = user
            if self.__manager is not None:
                self.__manager.current_user = user
            self.general_loading_screen('Login successful, loading home page', self.home_screen) #displays successful message and switches screen

        #login button
        login_button = self.__button(card, 'Log in', attempt_login)
        login_button.pack(fill='x', pady=(0, 14))
        #label for create account screen, users who do not have an account clicks this which links to the create account page
        create_account_button = tk.Label(card, text="Don't have an account? Create one",
                                         font=(self.__font, 11, 'underline'), bg=self.__colour1,
                                         fg=self.__colour2, cursor=self.__hand)
        create_account_button.pack()
        create_account_button.bind('<Button-1>', lambda event: self.create_account_screen())

        #allows user to log in by pressing the enter button on the keyboard as well as pressing the 'log in' button
        for entry in (email_entry, password_entry):
            entry.bind('<Return>', lambda event: attempt_login())

        #Automatically places the blinking text cursor in the email input box as soon as it loads
        #Allows the user to type immediately without clicking first
        email_entry.focus_set()

    def create_account_screen(self):
        #Sets frame for screen and clears all widgets from the screen
        self.clear_container()
        card = tk.Frame(self.__container, bg=self.__colour1)
        card.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8)

        # adds heading and title text
        tk.Label(card, text='xG Calculator', font=(self.__font, 24, 'bold'),
                 bg=self.__colour1, fg=self.__colour2).pack(pady=(0, 4))
        tk.Label(card, text='Create account to continue', font=(self.__font, 12),
                 bg=self.__colour1, fg=self.__muted).pack(pady=(0, 12))

        # first name and last name side by side
        name_row = tk.Frame(card, bg=self.__colour1)
        name_row.pack(fill='x')
        name_row.columnconfigure((0, 1), weight=1, uniform='name')

        fname_frame = tk.Frame(name_row, bg=self.__colour1)
        fname_frame.grid(row=0, column=0, sticky='ew', padx=(0, 6))
        tk.Label(fname_frame, text='First Name', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        fname_entry = self.__entry(fname_frame)
        fname_entry.pack(fill='x', ipady=6, pady=(2, 12))

        lname_frame = tk.Frame(name_row, bg=self.__colour1)
        lname_frame.grid(row=0, column=1, sticky='ew', padx=(6, 0))
        tk.Label(lname_frame, text='Last Name', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        lname_entry = self.__entry(lname_frame)
        lname_entry.pack(fill='x', ipady=6, pady=(2, 12))

        # organisation
        tk.Label(card, text='Organisation (optional)', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        organisation_entry = self.__entry(card)
        organisation_entry.pack(fill='x', ipady=6, pady=(2, 12))

        # email
        tk.Label(card, text='Email', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        email_entry = self.__entry(card)
        email_entry.pack(fill='x', ipady=6, pady=(2, 12))

        # password and re-enter password side by side
        password_row = tk.Frame(card, bg=self.__colour1)
        password_row.pack(fill='x')
        password_row.columnconfigure((0, 1), weight=1, uniform='password')

        password_frame = tk.Frame(password_row, bg=self.__colour1)
        password_frame.grid(row=0, column=0, sticky='ew', padx=(0, 6))
        tk.Label(password_frame, text='Password', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        password_entry = self.__entry(password_frame, show='•')
        password_entry.pack(fill='x', ipady=6, pady=(2, 12))

        repassword_frame = tk.Frame(password_row, bg=self.__colour1)
        repassword_frame.grid(row=0, column=1, sticky='ew', padx=(6, 0))
        tk.Label(repassword_frame, text='Re-enter Password', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        repassword_entry = self.__entry(repassword_frame, show='•')
        repassword_entry.pack(fill='x', ipady=6, pady=(2, 12))

        # label for when verification error comes up, above the button
        error_label = tk.Label(card, text='', font=(self.__font, 11), bg=self.__colour1,
                               fg=self.__error, wraplength=300, justify='left', anchor='w')
        error_label.pack(fill='x', pady=(0, 8))

        #validation function for account creation screen
        def attempt_create_account():
            email = email_entry.get().strip()
            password = password_entry.get()
            repassword = repassword_entry.get()
            fname = fname_entry.get()
            lname = lname_entry.get()
            organisation = organisation_entry.get()

            #check empty fields
            if not email or not password or not repassword or not fname or not lname:
                error_label.config(text='Mandatory fields cannot be empty')
                return

            # checks for email errors, if there is an error, message is displayed accordingly
            email_problem = email_error(email)
            if email_problem:
                error_label.config(text=email_problem)
                return

            # checks for password errors, if there is an error, message is displayed accordingly
            password_problem = password_error(password)
            if password_problem:
                error_label.config(text=password_problem)
                return

            # checks if passwords match, if they do not match, message is displayed accordingly
            if password!=repassword:
                error_label.config(text='Passwords not matching')
                return

            # checks for email clashes in the Users table in the database
            try:
                found = check_email_exist(self.__db_connection, email)
            # if there is a connection problem with the database, will display error message
            except Exception as error:
                print('LOGIN ERROR:', repr(error))
                error_label.config(text='Could not reach the database, please try again')
                return
            #if User matching email is found, display error message as one email address can only have one account
            if found:
                error_label.config(text='This email already has an account')
                return

            #adds new user to the database
            add_user(self.__db_connection, fname, lname, organisation, email, password)
            refind = find_user(self.__db_connection, email, password)

            #in case error occurs during adding user
            if refind is None:
                error_label.config(text='Account could not be created, please try again')
                return
            user = User(*refind)  # User(userID, name, email) - matches user entry
            #logs in with the new account automatically
            self.__current_user = user
            if self.__manager is not None:
                self.__manager.current_user = user
            self.general_loading_screen('Account creation successful, loading home page', self.home_screen)

        # login button
        create_account_button = self.__button(card, 'Create Account', attempt_create_account)
        create_account_button.pack(fill='x', pady=(0, 14))

        # allows user to log in by pressing the enter button on the keyboard as well as pressing the 'log in' button
        for entry in (email_entry, password_entry, repassword_entry, fname_entry, lname_entry, organisation_entry):
            entry.bind('<Return>', lambda event: attempt_create_account())
        fname_entry.focus_set()


    def home_screen(self):
        self.clear_container()
        self.__set_window_size(1280, 800)
        expanded_width = 200
        collapsed_width = 56

        sidebar = tk.Frame(self.__container, bg=self.__colour1, width=expanded_width,
                           highlightthickness=1, highlightbackground=self.__border)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)  # stops the sidebar shrinking to fit its contents, so the width set above is kept

        main_content = tk.Frame(self.__container, bg=self.__colour1)
        main_content.pack(side='right', fill='both', expand=True)

        # sidebar state
        is_expanded = True
        nav_text_labels = []  # text next to each icon, hidden when the sidebar is collapsed

        def toggle_sidebar(event=None):
            nonlocal is_expanded
            if is_expanded:
                sidebar.configure(width=collapsed_width)
                for label in nav_text_labels:
                    label.pack_forget()
            else:
                sidebar.configure(width=expanded_width)
                for label in nav_text_labels:
                    label.pack(side='left', fill='x')
            is_expanded = not is_expanded

        # toggle button
        toggle_button = tk.Label(sidebar, text='☰', font=(self.__font, 22, 'bold'), bg=self.__colour1,
                                 fg=self.__colour2, cursor=self.__hand, width=2)
        toggle_button.pack(anchor='w', padx=8, pady=(10, 16))
        toggle_button.bind('<Button-1>', toggle_sidebar)
        toggle_button.bind('<Enter>', lambda event: toggle_button.configure(fg=self.__colour2_dark))
        toggle_button.bind('<Leave>', lambda event: toggle_button.configure(fg=self.__colour2))

        # creates one sidebar button made of an icon and its text
        def nav_item(icon, text, command):
            item = tk.Frame(sidebar, bg=self.__colour1, cursor=self.__hand)
            item.pack(fill='x', pady=2)
            icon_label = tk.Label(item, text=icon, font=(self.__font, 18), bg=self.__colour1,
                                  fg=self.__colour2, width=2)
            icon_label.pack(side='left', padx=(8, 10), pady=8)
            text_label = tk.Label(item, text=text, font=(self.__font, 13, 'bold'), bg=self.__colour1,
                                  fg=self.__text, anchor='w')
            text_label.pack(side='left', fill='x')
            nav_text_labels.append(text_label)

            parts = (item, icon_label, text_label)

            def set_background(colour):
                for part in parts:
                    part.configure(bg=colour)

            # binds every part so clicking or hovering anywhere on the button works
            for part in parts:
                part.bind('<Button-1>', lambda event: command())
                part.bind('<Enter>', lambda event: set_background(self.__border))
                part.bind('<Leave>', lambda event: set_background(self.__colour1))

        nav_item('⌂', 'Home', self.home_screen)
        nav_item('+', 'New Simulation', self.new_simulation_screen)
        nav_item('⇄', 'Compare', self.comparison_screen)
        nav_item('⚙', 'Settings', self.settings_screen)

        recents = recent_sims(self.__db_connection, self.__current_user.get_userID())
        tk.Label(self.__container, text=' ', font=(self.__font, 5, 'bold'),
                 bg=self.__colour1, fg=self.__colour2, anchor='w').pack(fill='x', padx=20)
        tk.Label(self.__container, text='Home page', font=(self.__font, 24, 'bold'),
                 bg=self.__colour1, fg=self.__colour2, anchor='w').pack(fill='x', padx=20, pady=(0, 4))
        tk.Label(self.__container, text='Recently saved', font=(self.__font, 20),
                 bg=self.__colour1, fg=self.__muted, anchor='w').pack(fill='x', padx=20, pady=(0, 12))
        if len(recents) == 0:
            tk.Label(self.__container, text='No recently saved simulations', font=(self.__font, 15),
                     bg=self.__colour1, fg=self.__muted, anchor='w').pack(fill='x', padx=20, pady=(0, 12))
        else:
            recents_row = tk.Frame(main_content, bg=self.__colour1)
            recents_row.pack(fill='x', padx=30)
            recents_row.columnconfigure((0,1,2), weight=1, uniform='recent')

            for column, (simulation_id, name, saved_date, best_xg, file_path) in enumerate(recents):
                sim_box = tk.Frame(recents_row, bg='white', highlightthickness=1,
                                   highlightbackground=self.__border, cursor=self.__hand)
                sim_box.grid(row=0, column=column, fill='x', padx=30, pady=(0, 10))
                name_label = tk.Label(sim_box, text=name, font=(self.__font, 15, 'bold'), bg='white',
                                      fg=self.__text, anchor='w')
                name_label.pack(fill='x', padx=16, pady=(12, 2))
                info_label = tk.Label(sim_box, text=f'Saved {saved_date}   ·   Best xG: {best_xg:.2f}',
                                      font=(self.__font, 12), bg='white', fg=self.__muted, anchor='w')
                info_label.pack(fill='x', padx=16, pady=(0, 12))
                # binds every part of the box so clicking anywhere opens that simulation
                for part in (sim_box, name_label, info_label):
                    part.bind('<Button-1>', lambda event, path=file_path: self.results_screen(path))
                    part.bind('<Enter>', lambda event, box=sim_box: box.configure(highlightbackground=self.__colour2))
                    part.bind('<Leave>', lambda event, box=sim_box: box.configure(highlightbackground=self.__border))






    def new_simulation_screen(self):
        pass

    def results_screen(self):
        pass

    def comparison_screen(self):
        pass

    def split_results_screen(self):
        pass

    def general_loading_screen(self, message, next_screen):
        #clears screen so new widgets can be placed
        self.clear_container()

        #Canvas widget used to draw the spinner
        wheel = tk.Canvas(self.__container, width=50, height=50, bg=self.__colour1, highlightthickness=0)
        wheel.pack(expand=True)

        #Draws a 270 degree arc inside the canvas to create the loading wheel graphic
        arc = wheel.create_arc(5, 5, 45, 45, start=0, extent=270, style='arc', outline=self.__colour2, width=5)

        # label to display text to user, message varies as transitions from page to page varies
        message_label = tk.Label(self.__container, text=message, font=(self.__font, 16),
                                 bg=self.__colour1, fg=self.__text, justify='center')
        message_label.pack(expand=True, fill='x', padx=20)

        # wraps the text to the label's current width, so it still fits when the window is resized
        message_label.bind('<Configure>', lambda event: message_label.configure(wraplength=event.width))

        #calls to do the spinning wheel animation
        def spin(angle=0):
            #Checks if the wheel canvas exists before updating to prevent transition errors
            if wheel.winfo_exists():
                #rotates the arc by incrementing starting angle
                wheel.itemconfigure(arc, start=angle)
                #recalls 20 ms later, shifting the angle by 12 degrees counter-clockwise
                self.__root.after(20, spin, angle - 12)

        #calls spin() function
        spin()
        self.__root.after(600, next_screen)

    def special_loading_screen(self):
        pass

    def settings_screen(self):
        pass


app = Application()
app.start()