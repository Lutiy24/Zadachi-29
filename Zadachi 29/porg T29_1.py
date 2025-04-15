import sqlite3
from datetime import datetime, timedelta

DB_NAME = "birthdays.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surname TEXT NOT NULL,
            birthdate TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_friend():
    surname = input("Введіть прізвище: ").strip()
    birthdate_str = input("Введіть дату народження (у форматі РРРР-ММ-ДД): ").strip()
    try:
        datetime.strptime(birthdate_str, "%Y-%m-%d")  # перевірка формату
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO friends (surname, birthdate) VALUES (?, ?)", (surname, birthdate_str))
        conn.commit()
        conn.close()
        print("Знайомого додано.")
    except ValueError:
        print("Невірний формат дати. Спробуйте ще раз.")

def show_birthday_by_surname():
    surname = input("Введіть прізвище для пошуку: ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT birthdate FROM friends WHERE surname = ?", (surname,))
    result = cursor.fetchone()
    if result:
        print(f"Дата народження: {result[0]}")
    else:
        print("Знайомого з таким прізвищем не знайдено.")
    conn.close()

def show_upcoming_birthdays():
    today = datetime.today()
    upcoming_limit = today + timedelta(days=7)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT surname, birthdate FROM friends")
    rows = cursor.fetchall()
    conn.close()

    print("Найближчі дні народження (до 7 днів):")
    for surname, birthdate_str in rows:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
        this_year_birthday = birthdate.replace(year=today.year)
        # Якщо вже пройшов день народження цього року, беремо наступний рік
        if this_year_birthday < today:
            this_year_birthday = this_year_birthday.replace(year=today.year + 1)
        days_left = (this_year_birthday - today).days
        if days_left <= 7:
            print(f"{surname} — {birthdate_str} (через {days_left} дн.)")

def main():
    create_db()
    show_upcoming_birthdays()
    while True:
        print("\nМеню:")
        print("1 — Додати знайомого")
        print("2 — Показати дату народження за прізвищем")
        print("0 — Вихід")
        choice = input("Ваш вибір: ").strip()
        if choice == '1':
            add_friend()
        elif choice == '2':
            show_birthday_by_surname()
        elif choice == '0':
            print("До побачення!")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
