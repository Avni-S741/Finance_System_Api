import sqlite3

def make_connection():
    connect_db=sqlite3.connect("expense.db")
    connect_db.row_factory = sqlite3.Row

    return connect_db 

def init_db():
    connect_db=make_connection()
    cursor=connect_db.cursor()

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS expensestore (
    id  TEXT PRIMARY KEY,
    amount REAL NOT NULL CHECK (amount > 0),
    item TEXT NOT NULL,
    paid_on TEXT NOT NULL,
    category TEXT NOT NULL,
    deleted INTEGER NOT NULL DEFAULT  0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    deleted_at TEXT 
    );
    ''')
    connect_db.commit()
    connect_db.close()



