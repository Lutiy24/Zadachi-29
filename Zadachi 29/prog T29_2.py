import sqlite3

DB_NAME = "systems.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS systems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            address TEXT,
            login TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_system():
    name = input("Введіть назву системи: ").strip()
    address = input("Введіть адресу (URL) системи (можна залишити порожнім): ").strip()
    login = input("Введіть логін: ").strip()
    password = input("Введіть пароль: ").strip()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO systems (name, address, login, password)
            VALUES (?, ?, ?, ?)
        ''', (name, address, login, password))
        conn.commit()
        print("Систему успішно додано.")
    except sqlite3.IntegrityError:
        print("Система з такою назвою вже існує.")
    conn.close()

def get_system_info():
    name = input("Введіть назву системи для пошуку: ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT address, login, password FROM systems WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        address, login, password = result
        print(f"\nНазва системи: {name}")
        print(f"Адреса: {address if address else '(немає адреси)'}")
        print(f"Логін: {login}")
        print(f"Пароль: {password}")
    else:
        print("Систему не знайдено.")

def main():
    create_db()
    while True:
        print("\nМеню:")
        print("1 — Додати нову систему")
        print("2 — Отримати логін/пароль за назвою системи")
        print("0 — Вихід")
        choice = input("Ваш вибір: ").strip()
        if choice == '1':
            add_system()
        elif choice == '2':
            get_system_info()
        elif choice == '0':
            print("До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
