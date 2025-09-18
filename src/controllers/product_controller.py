from daos.product_dao import ProductDAO

class ProductController:
    def __init__(self):
        self.dao = ProductDAO()
    
    def list_products(self):
        return self.dao.select_all()
    
    def create_product(self, product):
        self.dao.insert(product)
    
    def shutdown(self):
        self.dao.close()