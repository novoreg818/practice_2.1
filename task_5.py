import json

imya_fayla_json = "library.json"

try:
    fayl_proverka = open(imya_fayla_json, "r", encoding="utf-8")
    fayl_proverka.close()
except FileNotFoundError:
    startovye_knigi = [
        {
            "id": 1,
            "title": "Мастер и Маргарита",
            "author": "Булгаков",
            "year": 1967,
            "available": True
        },
        {
            "id": 2,
            "title": "Преступление и наказание",
            "author": "Достоевский",
            "year": 1866,
            "available": False
        }
    ]
    fayl_sozdanie = open(imya_fayla_json, "w", encoding="utf-8")
    json.dump(startovye_knigi, fayl_sozdanie, ensure_ascii=False, indent=4)
    fayl_sozdanie.close()
    print("Уведомление: База данных 'library.json' успешно создана с начальными данными.")

spisok_knig = []
try:
    fayl_chtenie = open(imya_fayla_json, "r", encoding="utf-8")
    spisok_knig = json.load(fayl_chtenie)
    fayl_chtenie.close()
except Exception as oshibka:
    print("Ошибка при чтении JSON:", oshibka)

while True:
    print("\n--- Система учета книг ---")
    print("1. Просмотр всех книг")
    print("2. Поиск по автору или названию")
    print("3. Добавление новой книги")
    print("4. Изменение статуса (взята/возвращена)")
    print("5. Удаление книги по ID")
    print("6. Экспорт доступных книг в txt")
    print("0. Выход")

    vybor = input("Выберите действие: ").strip()

    if vybor == "1":
        print("\nКаталог библиотеки:")
        for kniga in spisok_knig:
            status = "Доступна" if kniga["available"] else "На руках"
            print("ID:", kniga["id"], "|", kniga["author"], "-", kniga["title"], "(", kniga["year"], ") -", status)

    elif vybor == "2":
        zapros = input("Введите автора или название для поиска: ").strip().lower()
        naydeno = False
        for kniga in spisok_knig:
            if zapros in kniga["author"].lower() or zapros in kniga["title"].lower():
                status = "Доступна" if kniga["available"] else "На руках"
                print("Найдено: ID", kniga["id"], "|", kniga["author"], "-", kniga["title"], "-", status)
                naydeno = True
        if not naydeno:
            print("Уведомление: По вашему запросу ничего не найдено.")

    elif vybor == "3":
        try:
            novoe_nazvanie = input("Введите название книги: ").strip()
            novyy_avtor = input("Введите автора: ").strip()
            novyy_god = int(input("Введите год издания: "))

            maksimalnyy_id = 0
            for kniga in spisok_knig:
                if kniga["id"] > maksimalnyy_id:
                    maksimalnyy_id = kniga["id"]
            novyy_id = maksimalnyy_id + 1

            novaya_kniga = {
                "id": novyy_id,
                "title": novoe_nazvanie,
                "author": novyy_avtor,
                "year": novyy_god,
                "available": True
            }
            spisok_knig.append(novaya_kniga)

            fayl_zapis = open(imya_fayla_json, "w", encoding="utf-8")
            json.dump(spisok_knig, fayl_zapis, ensure_ascii=False, indent=4)
            fayl_zapis.close()
            print("Уведомление: Книга успешно добавлена и сохранена в файл!")

        except ValueError:
            print("Ошибка: Год издания должен быть числом! Добавление отменено.")

    elif vybor == "4":
        try:
            id_dlya_izmeneniya = int(input("Введите ID книги для изменения статуса: "))
            kniga_naydena = False
            for kniga in spisok_knig:
                if kniga["id"] == id_dlya_izmeneniya:
                    kniga_naydena = True
                    if kniga["available"] == True:
                        kniga["available"] = False
                        print("Уведомление: Книга теперь числится 'На руках'.")
                    else:
                        kniga["available"] = True
                        print("Уведомление: Книга успешно возвращена и 'Доступна'.")

                    fayl_zapis = open(imya_fayla_json, "w", encoding="utf-8")
                    json.dump(spisok_knig, fayl_zapis, ensure_ascii=False, indent=4)
                    fayl_zapis.close()
                    break

            if not kniga_naydena:
                print("Уведомление: Книга с таким ID не найдена.")
        except ValueError:
            print("Ошибка: ID должен быть числом!")

    elif vybor == "5":
        try:
            id_dlya_udaleniya = int(input("Введите ID книги для удаления: "))
            indeks_dlya_udaleniya = -1

            for i in range(len(spisok_knig)):
                if spisok_knig[i]["id"] == id_dlya_udaleniya:
                    indeks_dlya_udaleniya = i
                    break

            if indeks_dlya_udaleniya != -1:
                udalennaya_kniga = spisok_knig.pop(indeks_dlya_udaleniya)
                fayl_zapis = open(imya_fayla_json, "w", encoding="utf-8")
                json.dump(spisok_knig, fayl_zapis, ensure_ascii=False, indent=4)
                fayl_zapis.close()
                print("Уведомление: Книга", udalennaya_kniga["title"], "успешно удалена.")
            else:
                print("Уведомление: Книга с таким ID не найдена.")
        except ValueError:
            print("Ошибка: ID должен быть числом!")

    elif vybor == "6":
        try:
            fayl_eksport = open("available_books.txt", "w", encoding="utf-8")
            fayl_eksport.write("Список доступных книг на данный момент:\n")
            kolichestvo = 0
            for kniga in spisok_knig:
                if kniga["available"] == True:
                    fayl_eksport.write(
                        "ID: " + str(kniga["id"]) + " | " + kniga["author"] + " - " + kniga["title"] + "\n")
                    kolichestvo += 1
            fayl_eksport.close()
            print("Уведомление: Экспорт завершен. В 'available_books.txt' записано", kolichestvo, "книг.")
        except Exception as oshibka:
            print("Ошибка при экспорте:", oshibka)

    elif vybor == "0":
        print("Работа с библиотекой завершена.")
        break

    else:
        print("Ошибка: Выберите правильный пункт меню.")