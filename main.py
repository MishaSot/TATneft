import argparse
import sys
from base import SQL

db = SQL('db.db')

def add_event(date, event, description, year, month):
    db.add_event(date, event, description, year, month)
    print(f"Событие '{event}' на дату {date}.{month}.{year} добавлено.")

def add_people(event, people):
    db.add_people(event, people)

def search_event(text):
    years = db.get_years()
    descriptions = db.get_description()
    events = db.get_event()
    text = text[2:-2]

    if not text.strip():
        print("Текст пустой или состоит из пробелов")
    elif not any(char.isalnum() for char in text):
        print("Текст состоит только из специальных символов")
    else:
        found_in_events = False
        found_in_years = False
        found_in_descriptions = False

        print('Поиск по событиям:')
        for i in range(len(events)):
            if text in str(events[i])[2:-3]:
                print(
                    f"{i + 1}) событие: <<{str(events[i])[2:-3]}>>, дата: {str(years[i])[2:-3]}, описание: {str(descriptions[i])[2:-3]}"
                )
                found_in_events = True
        if not found_in_events:
            print("Ничего не найдено")

        print('Поиск по годам:')
        for i in range(len(events)):
            if text in str(years[i])[2:-3]:
                print(
                    f"{i + 1}) событие: {str(events[i])[2:-3]}, дата: <<{str(years[i])[2:-3]}>>, описание: {str(descriptions[i])[2:-3]}"
                )
                found_in_years = True
        if not found_in_years:
            print("Ничего не найдено")

        print('Поиск по описаниям:')
        for i in range(len(events)):
            if text in str(descriptions[i])[2:-3]:
                print(
                    f"{i + 1}) событие: {str(events[i])[2:-3]}, дата: {str(years[i])[2:-3]}, описание: <<{str(descriptions[i])[2:-3]}>>"
                )
                found_in_descriptions = True
        if not found_in_descriptions:
            print("Ничего не найдено")

def stats():
    events = db.get_event()
    print(f"Всего событий: {len(events)}")

    events_by_year = db.count_events_by_year()
    print("\nКоличество событий по годам:")
    for year, count in events_by_year:
        print(f"{year}: {count} событий")

    top_people = db.top_5_people()
    print("\nТоп-5 людей по участию в событиях:")
    for i, (person, count) in enumerate(top_people, start=1):
        print(f"{i}. {person}: {count} событий")

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"Ошибка: {message}. Используйте --help для получения справки.")
        sys.exit(1)

def main():
    parser = CustomArgumentParser(description="Командное приложение для работы с событиями.")

    parser.add_argument('--add', nargs=4, metavar=('date', 'event', 'people', 'description'), help="Добавить событие.")
    parser.add_argument('--search', nargs=1, metavar='text', help="Поиск события по части названия, описания или даты.")
    parser.add_argument('--stats', action='store_true', help="Показать статистику.")

    args = parser.parse_args()

    if not any(vars(args).values()):
        print("Не указана команда. Используйте --help для получения справки.")
        sys.exit(1)

    if args.add:
        date, event, people, description = args.add
        ind = date.find("-")
        ind2 = date.rfind("-")
        f = 0

        if date.count("-") == 2:
            year, month, day = date.split("-")
            if 1900 <= int(year) <= 2025 and 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
                f += 1
            else:
                print("Некорректная дата. Год должен быть от 1900 до 2025, месяц от 1 до 12, день от 1 до 31.")
        else:
            print('Некорректный формат даты. Используйте формат гггг-мм-дд.')

        if f == 1:
            add_event(day, event, description, year, month)
            for person in people.split(","):
                if person.strip():
                    add_people(event, person.strip())

    elif args.search:
        search_event(str(args.search[0]))

    elif args.stats:
        stats()

if __name__ == "__main__":
    main()