"""
Product DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from models.product import Product

class ProductDAO:
    def __init__(self):
        try:
            env_path = os.path.join(Path(__file__).parent.parent.parent, '.env')
            load_dotenv(dotenv_path=env_path)
            db_host = os.getenv("MYSQL_HOST")
            db_name = os.getenv("MYSQL_DB_NAME")
            db_user = os.getenv("MYSQL_USER")
            db_pass = os.getenv("MYSQL_PASSWORD")
            self.conn = mysql.connector.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_pass, 
                port=3307
            )
            self.cursor = self.conn.cursor()
        except FileNotFoundError as e:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all products from MySQL """
        self.cursor.execute("SELECT id, name, brand, price FROM products")
        rows = self.cursor.fetchall()
        return [Product(*row) for row in rows]

    def insert(self, product):
        """ Insert given product into MySQL """
        self.cursor.execute(
            "INSERT INTO products (name, brand, price) VALUES (%s, %s, %s)",
            (product.name, product.brand, product.price)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, product):
        """ Update given product in MySQL """
        self.cursor.execute(
            "UPDATE products SET name = %s, brand = %s, price = %s WHERE id = %s",
            (product.name, product.brand, product.price, product.id)
        )

    def delete(self, product_id):
        """ Delete product from MySQL with given product ID """
        query = "DELETE FROM products WHERE id = %s"
        params = (product_id,)
        self.cursor.execute(query, params)
        self.conn.commit()

    def delete_all(self): #optional
        """ Empty products table in MySQL """
        self.cursor.execute("DELETE FROM products")
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
