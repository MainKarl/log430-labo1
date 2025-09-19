# Rapport 

## Question 1

**Quelles commandes avez-vous utilisées pour effectuer les opérations UPDATE et DELETE dans MySQL ? Avez-vous uniquement utilisé Python ou également du SQL ? Veuillez inclure le code pour illustrer votre réponse.**

La librairie mysql.connector de python permet d'avoir un curseur qui peut exécuter des commandes SQL en texte (string). C'est ce que j'ai utilisé pour le update ainsi que le delete. La commande pour le update est la suivante: `UPDATE users SET name = new_user_name, email = new_user_email WHERE id = user_id` et la commande pour le delete est la suivante: `DELETE FROM users WHERE id = user_id`. Dans le DAO, l'utilisation de ces fonctions est comme suit:

```python
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
```

La commande SQL pour supprimer tous les éléments d'une table est la suivante: `DELETE FROM users` et peut être retrouvé dans cet méthode:

```python
def delete_all(self): #optional
    """ Empty users table in MySQL """
    self.cursor.execute("DELETE FROM users")
    self.conn.commit()
```

## Question 2

**Quelles commandes avez-vous utilisées pour effectuer les opérations dans MongoDB ? Avez-vous uniquement utilisé Python ou également du SQL ? Veuillez inclure le code pour illustrer votre réponse.**

J'ai utilisé les méthodes de base de pymongo qui sont fournis pour chaque table d'une base de données.

## Question 3

**Comment avez-vous implémenté votre product_view.py ? Est-ce qu’il importe directement la ProductDAO ? Veuillez inclure le code pour illustrer votre réponse.**

...

## Question 4

**Si nous devions créer une application permettant d’associer des achats d'articles aux utilisateurs (Users → Products), comment structurerions-nous les données dans MySQL par rapport à MongoDB ?**

...
