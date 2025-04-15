import sqlite3

DB_NAME = "suppliers.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            contact TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS supplies (
            supplier_id INTEGER,
            product_id INTEGER,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            PRIMARY KEY (supplier_id, product_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_supplier():
    name = input("Введіть назву постачальника: ").strip()
    contact = input("Введіть контактні дані: ").strip()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO suppliers (name, contact) VALUES (?, ?)", (name, contact))
        conn.commit()
        print("Постачальника додано.")
    except sqlite3.IntegrityError:
        print("Постачальник з такою назвою вже існує.")
    conn.close()

def add_product():
    name = input("Введіть назву товару: ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name) VALUES (?)", (name,))
        conn.commit()
        print("Товар додано.")
    except sqlite3.IntegrityError:
        print("Такий товар вже існує.")
    conn.close()

def link_supplier_product():
    supplier_name = input("Введіть назву постачальника: ").strip()
    product_name = input("Введіть назву товару: ").strip()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM suppliers WHERE name = ?", (supplier_name,))
    supplier = cursor.fetchone()
    cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
    product = cursor.fetchone()
    
    if supplier and product:
        try:
            cursor.execute("INSERT INTO supplies (supplier_id, product_id) VALUES (?, ?)", (supplier[0], product[0]))
            conn.commit()
            print("Зв’язок додано.")
        except sqlite3.IntegrityError:
            print("Цей постачальник вже постачає цей товар.")
    else:
        print("Постачальника або товар не знайдено.")
    
    conn.close()

def search_suppliers_by_product():
    product_name = input("Введіть назву товару: ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.name, s.contact
        FROM suppliers s
        JOIN supplies sp ON s.id = sp.supplier_id
        JOIN products p ON p.id = sp.product_id
        WHERE p.name = ?
    ''', (product_name,))
    
    results = cursor.fetchall()
    if results:
        print(f"\nПостачальники товару '{product_name}':")
        for name, contact in results:
            print(f"- {name} (контакти: {contact})")
    else:
        print("Немає постачальників для цього товару.")
    
    conn.close()

def search_products_by_supplier():
    supplier_name = input("Введіть назву постачальника: ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.name
        FROM products p
        JOIN supplies sp ON p.id = sp.product_id
        JOIN suppliers s ON s.id = sp.supplier_id
        WHERE s.name = ?
    ''', (supplier_name,))
    
    results = cursor.fetchall()
    if results:
        print(f"\nТовари, які постачає '{supplier_name}':")
        for (name,) in results:
            print(f"- {name}")
    else:
        print("Цей постачальник не постачає жодного товару.")
    
    conn.close()

def main():
    create_db()
    while True:
        print("\nМеню:")
        print("1 — Додати постачальника")
        print("2 — Додати товар")
        print("3 — Зв’язати постачальника з товаром")
        print("4 — Знайти постачальників за товаром")
        print("5 — Знайти товари за постачальником")
        print("0 — Вихід")
        choice = input("Ваш вибір: ").strip()
        if choice == '1':
            add_supplier()
        elif choice == '2':
            add_product()
        elif choice == '3':
            link_supplier_product()
        elif choice == '4':
            search_suppliers_by_product()
        elif choice == '5':
            search_products_by_supplier()
        elif choice == '0':
            print("До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
