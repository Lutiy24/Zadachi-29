import sqlite3

DB_NAME = "real_estate.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблиця об'єктів нерухомості
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_estate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            address TEXT NOT NULL,
            total_area REAL NOT NULL,
            room_count INTEGER NOT NULL
        )
    ''')

    # Таблиця кімнат
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estate_id INTEGER,
            purpose TEXT NOT NULL,
            area REAL NOT NULL,
            FOREIGN KEY (estate_id) REFERENCES real_estate(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_estate():
    type_ = input("Вид об'єкта (будинок, квартира тощо): ").strip()
    address = input("Адреса: ").strip()
    total_area = float(input("Загальна площа (м²): "))
    room_count = int(input("Кількість кімнат: "))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO real_estate (type, address, total_area, room_count)
        VALUES (?, ?, ?, ?)
    ''', (type_, address, total_area, room_count))
    conn.commit()
    conn.close()
    print("Об'єкт нерухомості додано.")

def add_room():
    estate_id = int(input("ID об'єкта нерухомості: "))
    purpose = input("Призначення кімнати (спальня, кухня, тощо): ").strip()
    area = float(input("Площа кімнати (м²): "))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM real_estate WHERE id = ?", (estate_id,))
    if cursor.fetchone():
        cursor.execute('''
            INSERT INTO rooms (estate_id, purpose, area)
            VALUES (?, ?, ?)
        ''', (estate_id, purpose, area))
        conn.commit()
        print("Кімнату додано.")
    else:
        print("Об'єкт із таким ID не знайдено.")
    conn.close()

def search_estates_by_type_and_area():
    type_ = input("Введіть вид об'єкта для пошуку: ").strip()
    min_area = float(input("Мінімальна загальна площа (м²): "))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, type, address, total_area, room_count
        FROM real_estate
        WHERE type = ? AND total_area >= ?
    ''', (type_, min_area))
    
    estates = cursor.fetchall()
    
    if not estates:
        print("Об'єкти не знайдено.")
        conn.close()
        return

    for estate in estates:
        estate_id, type_, address, total_area, room_count = estate
        print(f"\nОб'єкт ID: {estate_id}")
        print(f"Вид: {type_}")
        print(f"Адреса: {address}")
        print(f"Загальна площа: {total_area} м²")
        print(f"Кількість кімнат: {room_count}")

        # Показати кімнати цього об'єкта
        cursor.execute('''
            SELECT purpose, area FROM rooms
            WHERE estate_id = ?
        ''', (estate_id,))
        rooms = cursor.fetchall()
        if rooms:
            print("Кімнати:")
            for i, (purpose, area) in enumerate(rooms, start=1):
                print(f"  {i}) {purpose} — {area} м²")
        else:
            print("  (немає даних про кімнати)")
    
    conn.close()

def main():
    create_db()
    while True:
        print("\nМеню:")
        print("1 — Додати об'єкт нерухомості")
        print("2 — Додати кімнату до об'єкта")
        print("3 — Пошук об'єктів за видом та площею")
        print("0 — Вихід")
        choice = input("Ваш вибір: ").strip()
        if choice == '1':
            add_estate()
        elif choice == '2':
            add_room()
        elif choice == '3':
            search_estates_by_type_and_area()
        elif choice == '0':
            print("До зустрічі!")
            break
        else:
            print("Невірний вибір. Спробуйте ще.")

if __name__ == "__main__":
    main()
