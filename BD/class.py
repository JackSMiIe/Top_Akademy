class ProductManager:
    def __init__(self, dbname, user, password, host='localhost'):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.cursor = self.conn.cursor()

    def fetch_all_products(self):
        self.cursor.execute("SELECT * FROM products;")
        return self.cursor.fetchall()

    def fetch_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
        return self.cursor.fetchone()

    def fetch_products_by_category(self, category_id):
        self.cursor.execute("SELECT * FROM products WHERE category_id = %s;", (category_id,))
        return self.cursor.fetchall()

    def fetch_products_by_brand(self, brand_id):
        self.cursor.execute("SELECT * FROM products WHERE brand_id = %s;", (brand_id,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()


class ProductCRUD:
    def __init__(self, dbname, user, password, host='localhost'):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.cursor = self.conn.cursor()

    def insert_product(self, product, description, category_id, brand_id, measurement_id):
        self.cursor.execute('''
            INSERT INTO products (product, description, category_id, brand_id, measurement_id) 
            VALUES (%s, %s, %s, %s, %s);
        ''', (product, description, category_id, brand_id, measurement_id))
        self.conn.commit()

    def update_product(self, product_id, product, description, category_id, brand_id, measurement_id):
        self.cursor.execute('''
            UPDATE products 
            SET product = %s, description = %s, category_id = %s, brand_id = %s, measurement_id = %s 
            WHERE id = %s;
        ''', (product, description, category_id, brand_id, measurement_id, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id = %s;", (product_id,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


# Пример использования классов
if __name__ == '__main__':
    product_manager = ProductManager('vpn_users', 'sasha', '2007')
    all_products = product_manager.fetch_all_products()
    print("All Products:", all_products)

    product = product_manager.fetch_product_by_id(1)
    print("Product by ID 1:", product)

    products_by_category = product_manager.fetch_products_by_category(1)
    print("Products in Category 1:", products_by_category)

    products_by_brand = product_manager.fetch_products_by_brand(1)
    print("Products by Brand 1:", products_by_brand)

    product_manager.close()

    product_crud = ProductCRUD('vpn_users', 'sasha', '2007')
    product_crud.insert_product('Product4', 'Description4', 1, 1, 1)
    product_crud.update_product(1, 'Updated Product1', 'Updated Description1', 1, 1, 1)
    product_crud.delete_product(2)
    product_crud.close()
