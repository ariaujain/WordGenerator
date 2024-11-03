import sqlite3
import os

#Define the database path for consistency
DB_PATH = os.path.abspath('users.db')

def setupDatabase():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (
                                name TEXT NOT NULL,
                                email TEXT NOT NULL UNIQUE)''')
        print("Database setup complete. Table 'users' is ready.")
    except sqlite3.Error as e:
        print(f"Database setup error: {e}")

def addUser(name, email):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            print(f"User '{name}' with email '{email}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: The email '{email}' already exists in the database.")
    except sqlite3.Error as e:
        print(f"Error adding user '{name}': {e}")

def getUsers():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            users = [user[0] for user in conn.execute("SELECT email FROM users")]
        print(f"Retrieved {len(users)} users from the database.")
        return users
    except sqlite3.Error as e:
        print(f"Error retrieving users: {e}")
        return []

if __name__ == "__main__":
    setupDatabase()

    currentUsers = getUsers()
    print("Initial users in the database:", currentUsers)

    #List of default users to add
    defaultUsers = [
        ("Aria", "ariaujain@gmail.com"),
        ("Keira", "keirasschultz@gmail.com"),
        ("Sophia", "806hearty@gmail.com")
    ]

    #Add default users if they are not already in the database
    for name, email in defaultUsers:
        if email not in currentUsers:
            addUser(name, email)
        else:
            print(f"User with email '{email}' already exists. Skipping.")

    #Display all current users for verification
    print("Final list of users in the database:")
    print(getUsers())
