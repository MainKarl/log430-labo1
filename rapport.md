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

J'ai utilisé les méthodes de base de pymongo qui sont fournis pour chaque table d'une base de données. En utilisant la collection users de la base de données mongodb, j'ai accès au méthode find (utilisé pour la récupération de la liste d'utilisateur), insert_one (utilisé pour l'insertion), update_one (utilisé pour la mise à jours des données), delete_one (utilisé pour la suppression d'un utilisateur) et delete_many (utilisé pour la suppression de tous les utilisateurs). SQL n'a pas été utilisé, car MongoDB est une base de données NoSQL.

```python
def select_all(self):
    return [User(str(row["_id"]), row["name"], row["email"]) for row in self.users.find()]

def insert(self, user):
    insert_operation = { "name": user.name, "email": user.email }
    result = self.users.insert_one(insert_operation)
    return result.inserted_id

def update(self, user):
    query_filter = { "_id": user.id }
    update_operation = { "$set" : {"name" : user.name, "email" : user.email }}
    self.users.update_one(query_filter, update_operation)

def delete(self, user_id):
    query_filter = { "_id": user_id }
    self.users.delete_one(query_filter)

def delete_all(self):
    self.users.delete_many()
```

## Question 3

**Comment avez-vous implémenté votre product_view.py ? Est-ce qu’il importe directement la ProductDAO ? Veuillez inclure le code pour illustrer votre réponse.**

La vue pour le produit à été implémenté d'une manière très similaire à la vue pour les utilisateurs. Premièrement, il est demandée des options à l'utilisateur de montrer la liste de produit, en ajouter ou quitter l'application. Tant l'affichage de la liste des produits que l'ajout d'un produit va appelé le contrôleur de produit pour récupérer la liste ou effectuer l'action demandée. Le ProductDAO n'est pas directement utilisé par la vue, mais plutôt par le contrôleur qui fait le lien entre la vue et le DAO/modèle.

```python
class ProductView:
    @staticmethod
    def show_options():
        controller = ProductController()
        while True:
            print("\n1. Montrer la liste des produits\n2. Ajouter un produit\n3. Supprimer un produit\n4. Quitter l'appli")
            choice = input("Choississez une option")

            if choice == "1":
                products = controller.list_products()
                ProductView.show_products(products)
            elif choice == "2":
                name, brand, price = ProductView.get_inputs()
                product = Product(name, brand, price)
                controller.create_product(product)
            elif choice == "3":
                id = input("L'id du produit: ").strip()
                controller.delete_product(product)
            elif choice == "4":
                controller.shutdown()
                break
            else:
                print("Cette option n'existe pas!")
    
    @staticmethod
    def show_products(products):
        print("\n".join(f"{product.id} : {product.name}, {product.brand} ({product.price})" for product in products))

    @staticmethod
    def get_inputs():
        name = input("Nom du produit: ").strip()
        brand = input("Marque du produit: ").strip()
        price = input("Prix du produit: ").strip()
        return name, brand, price
```

## Question 4

**Si nous devions créer une application permettant d’associer des achats d'articles aux utilisateurs (Users → Products), comment structurerions-nous les données dans MySQL par rapport à MongoDB ?**

Dans MySQL, nous utiliserions une table associative qui fait le lien entre la table Users et Products grâce à leur id respectif. Cette table contiendrait ainsi un id à part entière, l'id de l'utilisateur concerné (qui sert de clé étrangère avec la table Users) et l'id du produit concerné (qui sert de clé étrangère avec la table Products). 

```sql
CREATE TABLE IF NOT EXISTS User_Products (
    id int primary key auto_increment,
    user_id int foreign key (id) references Users(id),
    product_id int foreign key (id) references Products(id)
);
```

Étant donné que MongoDB est un NoSQL, alors la structure varie. La collection users va contenir une variable qui contient une liste de référence des id de products que l'utilisateur a acheté (un "embed" pourrait aussi être utilisé plutôt qu'une référence).

```python
class User:
    def __init__(self, user_id, name, email, product_ids):
        self.id = user_id
        self.name = name
        self.email = email
        self.product_ids = product_ids # Représente la liste de références des ids des produits achetés par l'utilisateur.
```

## CI/CD

Le CI/CD va tout d'abord vérifier que le dépôt est valide. Quand cela est terminé, il va installer python ainsi que ces dépendances et construire le docker sur la machine virtuelle (tant l'application que les bases de données). Finalement, les tests python sont exécutés sur la machine virtuelle pour vérifier que tous fonctionnent correctement.

Étant donné que le CI c'est fait sur la machine de déploiement, alors le CD est effectué en même temps que le CI!
