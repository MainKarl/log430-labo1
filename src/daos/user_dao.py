"""
User DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from models.user import User

class UserDAO:
    def __init__(self):
        try:
            env_path = os.path.join(Path(__file__).parent.parent.parent, '.env')
            print(env_path)
            load_dotenv(dotenv_path=env_path)
            db_host = "mysql" #os.getenv("MYSQL_HOST")
            db_name = "mydb" #os.getenv("MYSQL_DB_NAME")
            db_user = "user" #os.getenv("MYSQL_USER")
            db_pass = "pass" #os.getenv("MYSQL_PASSWORD")
            self.conn = mysql.connector.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_pass, 
                port=3306
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print(f"Attente, la base de données a généré une erreur: ${str(e)}")
        except FileNotFoundError as e:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all users from MySQL """
        self.cursor.execute("SELECT id, name, email FROM users")
        rows = self.cursor.fetchall()
        return [User(*row) for row in rows]

    def insert(self, user):
        """ Insert given user into MySQL """
        self.cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (user.name, user.email)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, user):
        """ Update given user in MySQL """
        self.cursor.execute(
            "UPDATE users SET name = %s, email = %s WHERE id = %s",
            (user.name, user.email, user.id)
        )
        self.conn.commit()

    def delete(self, user_id):
        """ Delete user from MySQL with given user ID """
        query = "DELETE FROM users WHERE id = %s"
        params = (user_id,)
        print("DELETE FROM users WHERE id = "+str(user_id))
        self.cursor.execute(query,params)
        self.conn.commit()

    def delete_all(self): #optional
        """ Empty users table in MySQL """
        self.cursor.execute("DELETE FROM users")
        self.conn.commit()
        
    def close(self):
        self.cursor.close()
        self.conn.close()
