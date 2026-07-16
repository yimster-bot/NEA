import sqlite3

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
             FOREIGN KEY (UserID) REFERENCES Users(UserID);   
             ''')

    connection.commit()