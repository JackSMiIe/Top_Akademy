import psycopg2

# Установите соединение с вашей базой данных
conn = psycopg2.connect(
    dbname='vpn_users', 
    user='sasha', 
    password='2007', 
    host='localhost'
)

cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255) NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS brands (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(255) NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS measurements (
    id SERIAL PRIMARY KEY,
    measurement CHAR(2) NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT REFERENCES categories(id),
    brand_id INT REFERENCES brands(id),
    measurement_id INT REFERENCES measurements(id)
);
''')

# Заполнение таблиц данными
categories_data = [
    ('Electronics',),
    ('Clothing',),
    ('Food',)
]

brands_data = [
    ('BrandA',),
    ('BrandB',),
    ('BrandC',)
]

measurements_data = [
    ('kg',),
    ('l',),
    ('pcs',)
]

products_data = [
    ('Product1', 'Description1', 1, 1, 1),
    ('Product2', 'Description2', 2, 2, 2),
    ('Product3', 'Description3', 3, 3, 3),
]

# Вставка данных в таблицы
cursor.executemany('INSERT INTO categories (category) VALUES (%s)', categories_data)
cursor.executemany('INSERT INTO brands (brand) VALUES (%s)', brands_data)
cursor.executemany('INSERT INTO measurements (measurement) VALUES (%s)', measurements_data)
cursor.executemany('INSERT INTO products (product, description, category_id, brand_id, measurement_id) VALUES (%s, %s, %s, %s, %s)', products_data)

conn.commit()

# Закрытие соединения
cursor.close()
conn.close()
