import pyodbc

class UserDatabase:
    def __init__(self, server, database):
        self.server = server
        self.database = database

        
        # Connect to database
        self.cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+";Trusted_Connection=yes;")
        self.cursor = self.cnxn.cursor()
        
        # Create users table if it doesn't exist
        self.cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[users]') AND type in (N'U'))
            CREATE TABLE [dbo].[users](
                [id] [int] IDENTITY(1,1) NOT NULL,
                [username] [nvarchar](50) NOT NULL,
                [email] [nvarchar](50) NOT NULL,
                [password] [nvarchar](50) NOT NULL,
                PRIMARY KEY CLUSTERED ([id] ASC)
            )
        ''')
        self.cnxn.commit()
    
    def create_user(self, username, email, password):
        # Check if username or email is already taken
        print("username, ",username)
        print("username, ",email)
        self.cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = self.cursor.fetchone()
        
        if existing_user:
            # Username or email already taken, raise error
            raise ValueError('Username or email already taken')
        else:
            # Add user to database
            self.cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            self.cnxn.commit()
            
    def read_user(self, email):
        # Get user from database
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = self.cursor.fetchone()
        
        if user:
            # Return user as dictionary
            return {'id': user[0], 'username': user[1], 'email': user[2], 'password': user[3]}
        else:
            # User not found, return None
            return None
    
    def update_user_password(self, username, new_password):
        # Update user's password
        self.cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        self.cnxn.commit()
        
    def delete_user(self, username):
        # Delete user from database
        self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self.cnxn.commit()
