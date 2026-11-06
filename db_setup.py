import sqlite3
import hashlib
from datetime import date

DB_PATH = 'xg_calculator.db'

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    create_tables(connection)
    return connection

def create_tables(connection):
    connection.execute(''' CREATE TABLE IF NOT EXISTS Users  
            (UserID INTEGER PRIMARY KEY AUTOINCREMENT,   
             First_Name TEXT NOT NULL, 
             Last_Name TEXT NOT NULL,
             Organisation TEXT,
             Email TEXT NOT NULL UNIQUE,
             Password TEXT NOT NULL,
             Creation_Date TEXT NOT NULL);   
             ''')

    connection.execute(''' CREATE TABLE IF NOT EXISTS Previous_Simulations  
            (SimulationID INTEGER PRIMARY KEY AUTOINCREMENT,   
             Date TEXT NOT NULL, 
             Best_xG REAL NOT NULL,
             Simulation_Name TEXT NOT NULL,
             File_Path TEXT NOT NULL,
             UserID INTEGER NOT NULL,
             FOREIGN KEY (UserID) REFERENCES Users(UserID));   
             ''')

    connection.commit()


# ---------- passwords: never store the real password, only its hash ----------
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# ---------- the two database actions the login / create account screens need ----------
def add_user(connection, first_name, last_name, organisation, email, password):
    """Returns True if the account was created, False if that email is already registered."""
    try:
        connection.execute(
            'INSERT INTO Users (First_Name, Last_Name, Organisation, Email, Password, Creation_Date) '
            'VALUES (?, ?, ?, ?, ?, ?)',
            (first_name, last_name, organisation, email.lower(), hash_password(password),
             date.today().isoformat()))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def find_user(connection, email, password):
    """Returns (UserID, 'First Last', Email) if the details are right, otherwise None."""
    row = connection.execute(
        'SELECT UserID, First_Name, Last_Name, Email, Password FROM Users WHERE Email = ?',
        (email.lower(),)).fetchone()
    if row and hash_password(password) == row[4]:
        return row[0], row[1] + ' ' + row[2], row[3]
    return None


def check_email_exist(connection, email):
    row = connection.execute(
        'SELECT Email FROM Users WHERE Email = ?', (email.lower(),)).fetchone()
    return row is not None

def delete_user(connection, user_id):
    """Deletes the user and their saved simulations. Returns True if a user was deleted."""
    connection.execute('DELETE FROM Previous_Simulations WHERE UserID = ?', (user_id,))
    cursor = connection.execute('DELETE FROM Users WHERE UserID = ?', (user_id,))
    connection.commit()
    return cursor.rowcount > 0

def recent_sims(connection, user_id):
    """Returns the user's 3 most recent simulations as (SimulationID, Simulation_Name, Date, Best_xG, File_Path)."""
    return connection.execute(
        'SELECT SimulationID, Simulation_Name, Date, Best_xG, File_Path FROM Previous_Simulations '
        'WHERE UserID = ? ORDER BY Date DESC, SimulationID DESC LIMIT 3',
        (user_id,)).fetchall()


connection = get_connection()
query = "INSERT INTO Previous_Simulations (SimulationID, Date, Best_xG, Simulation_Name, File_Path, UserID) VALUES (1, )"
print(connection.execute('SELECT * FROM Users').fetchall())



