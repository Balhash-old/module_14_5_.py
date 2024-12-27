import sqlite3


def initiate_db():
    connection = sqlite3.connect('products.dp')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price TEXT NOT NULL
    )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL)  
             ''')

    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    check_user = cursor.execute("SELECT * FROM Users WHERE username=?", (username,))

    if check_user.fetchone() is None:
        cursor.execute(
            "INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
            (username, email, age, 1000)
        )

    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    check_user = cursor.execute("SELECT * FROM Users WHERE username=?", (username,))

    exists = True

    if check_user.fetchone() is None:
        exists = False

    connection.commit()
    connection.close()
    return exists


def add_product(prod_id, title, description, price):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    check_product = cursor.execute("SELECT * FROM Products WHERE id=?", (prod_id,))

    if check_product.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Products VALUES('{prod_id}', '{title}', '{description}', '{price}')
''')

    connection.commit()
    connection.close()




def check_and_populate_products():
    connection = sqlite3.connect('products.dp')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM Products')
    count = cursor.fetchone()[0]

    if count == 0:
        for i in range(1, 5):
            cursor.execute(
                'INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                (f'Продукт {i}', f'Описание {i}', f'{i * 100}')
            )
    else:
        pass

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('products.dp')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products
