import re
import sys
import tkinter as tk
from user import User
from pitch import Pitch
from xg_model import xG_Model
from feature_calculation import Feature_Calculation
from db_setup import get_connection

# ---------- small validation helpers (no tkinter in them) ----------
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}$")


def email_error(email):
    if len(email) > 254 or '..' in email or not EMAIL_PATTERN.match(email):
        return 'Please enter a valid email'
    return None


def password_error(password):
    """Only used on Create Account (login must not reveal the rules)."""
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
        self.__current_user = None
        self.__pitch = Pitch()
        self.__simulation = None
        self.__model = xG_Model('model.pkl')
        self.__calculator = Feature_Calculation('scaler.pkl')
        self.__renderer = None
        self.__manager = None
        self.__display = None
        self.__db_connection = None
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
        for widget in self.__container.winfo_children():
            widget.destroy()

    # ---------- reusable styled widgets (Mac-safe) ----------
    def __entry(self, parent, show=None):
        # highlight* draws the border; tk.Entry honours it on macOS
        return tk.Entry(parent, show=show or '', font=(self.__font, 14), bg='white', fg=self.__text,
                        relief='flat', bd=0, highlightthickness=1, highlightbackground=self.__border,
                        highlightcolor=self.__colour2, insertbackground=self.__text)

    def __button(self, parent, text, command):
        # tk.Button ignores bg/fg on macOS, so use a Label that behaves like a button
        btn = tk.Label(parent, text=text, font=(self.__font, 14, 'bold'), bg=self.__colour2,
                       fg='white', pady=10, cursor=self.__hand)
        btn.bind('<Button-1>', lambda e: command())
        btn.bind('<Enter>', lambda e: btn.configure(bg=self.__colour2_dark))
        btn.bind('<Leave>', lambda e: btn.configure(bg=self.__colour2))
        return btn

    # ---------- screens ----------
    def login_screen(self):
        self.clear_container()
        card = tk.Frame(self.__container, bg=self.__colour1)
        card.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8)

        tk.Label(card, text='xG Calculator', font=(self.__font, 24, 'bold'),
                 bg=self.__colour1, fg=self.__colour2).pack(pady=(0, 4))
        tk.Label(card, text='Log in to continue', font=(self.__font, 12),
                 bg=self.__colour1, fg=self.__muted).pack(pady=(0, 20))

        tk.Label(card, text='Email', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        email_entry = self.__entry(card)
        email_entry.pack(fill='x', ipady=6, pady=(2, 12))

        tk.Label(card, text='Password', font=(self.__font, 11, 'bold'), bg=self.__colour1,
                 fg=self.__text, anchor='w').pack(fill='x')
        password_entry = self.__entry(card, show='•')
        password_entry.pack(fill='x', ipady=6, pady=(2, 8))

        error_label = tk.Label(card, text='', font=(self.__font, 11), bg=self.__colour1,
                               fg=self.__error, wraplength=300, justify='left', anchor='w')
        error_label.pack(fill='x', pady=(0, 8))

        def attempt_login():
            email = email_entry.get().strip()
            password = password_entry.get()
            if not email or not password:
                error_label.config(text='Fields cannot be empty')
                return
            problem = email_error(email)
            if problem:
                error_label.config(text=problem)
                return
            try:
                user = User(self.__db_connection).login(email, password)
            except Exception as error:
                print('LOGIN ERROR:', repr(error))
                error_label.config(text='Could not reach the database, please try again')
                return
            if not user:
                error_label.config(text='Invalid email or password')
                return
            self.__current_user = user
            if self.__manager is not None:
                self.__manager.current_user = user
            # pass the function itself (no brackets) so it runs AFTER the loading screen
            self.general_loading_screen('Login successful, loading home page', self.home_screen)

        login_button = self.__button(card, 'Log in', attempt_login)
        login_button.pack(fill='x', pady=(0, 14))

        create_account_button = tk.Label(card, text="Don't have an account? Create one",
                                         font=(self.__font, 11, 'underline'), bg=self.__colour1,
                                         fg=self.__colour2, cursor=self.__hand)
        create_account_button.pack()
        create_account_button.bind('<Button-1>', lambda e: self.create_account_screen())

        for entry in (email_entry, password_entry):
            entry.bind('<Return>', lambda e: attempt_login())
        email_entry.focus_set()

    def create_account_screen(self):
        pass

    def home_screen(self):
        # placeholder so the loading screen has somewhere to go - replace later
        self.clear_container()
        tk.Label(self.__container, text='Home page', font=(self.__font, 20, 'bold'),
                 bg=self.__colour1, fg=self.__text).pack(expand=True)

    def new_simulation_screen(self):
        pass

    def results_screen(self):
        pass

    def comparison_screen(self):
        pass

    def split_results_screen(self):
        pass

    def general_loading_screen(self, message, next_screen):
        self.clear_container()
        tk.Label(self.__container, text=message, font=(self.__font, 16),
                 bg=self.__colour1, fg=self.__text).pack(expand=True)
        self.__root.after(900, next_screen)

    def special_loading_screen(self):
        pass

    def settings_screen(self):
        pass


app = Application()
app.start()