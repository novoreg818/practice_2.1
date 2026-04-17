try:
    fayl_proverka = open("products.csv", "r", encoding="utf-8")
    fayl_proverka.close()
except FileNotFoundError:
    sozdanie = open("products.csv", "w", encoding="utf-8")
    sozdanie.write("Название,Цена,Количество\n")
    sozdanie.write("Яблоки,100,50\n")
    sozdanie.write("Бананы,80,30\n")
    sozdanie.write("Молоко,120,20\n")
    sozdanie.write("Хлеб,40,100\n")
    sozdanie.close()
    print("Уведомление: Файл 'products.csv' успешно создан с начальными данными.")

spisok_tovarov = []
zagolovok = ""

try:
    fayl_chtenie = open("products.csv", "r", encoding="utf-8")
    vse_stroki = fayl_chtenie.readlines()
    fayl_chtenie.close()

    if len(vse_stroki) > 0:
        zagolovok = vse_stroki[0].strip()

        for stroka in vse_stroki[1:]:
            chistaya = stroka.strip()
            if chistaya != "":
                danye = chistaya.split(",")
                nazvanie = danye[0]
                cena = int(danye[1])
                kolichestvo = int(danye[2])
                spisok_tovarov.append([nazvanie, cena, kolichestvo])
except Exception as oshibka:
    print("Системная ошибка при чтении файла:", oshibka)

while True:
    print("\n--- Управление складом ---")
    print("1. Показать все товары")
    print("2. Добавить новый товар")
    print("3. Найти товар по названию")
    print("4. Расчет общей стоимости склада")
    print("5. Сохранить обновленные данные в products.csv")
    print("6. Сохранить отсортированные товары в sorted_products.csv")
    print("0. Выход из программы")

    vybor = input("Выберите пункт меню: ").strip()

    if vybor == "1":
        print("\nТекущий список товаров:")
        for tovar in spisok_tovarov:
            print("Товар:", tovar[0], "| Цена:", tovar[1], "| Кол-во:", tovar[2])

    elif vybor == "2":
        try:
            novoe_nazvanie = input("Введите название товара: ").strip()
            novaya_cena = int(input("Введите цену товара: "))
            novoe_kolichestvo = int(input("Введите количество товара: "))
            spisok_tovarov.append([novoe_nazvanie, novaya_cena, novoe_kolichestvo])
            print("Уведомление: Товар", novoe_nazvanie, "успешно добавлен в память!")
        except ValueError:
            print("Ошибка ввода: Цена и количество должны быть целыми числами! Попробуйте снова.")

    elif vybor == "3":
        iskomyi_tovar = input("Введите название для поиска: ").strip().lower()
        nayden = False
        for tovar in spisok_tovarov:
            if iskomyi_tovar == tovar[0].lower():
                print("\nНайден товар:", tovar[0], "| Цена:", tovar[1], "| Кол-во:", tovar[2])
                nayden = True
        if not nayden:
            print("Уведомление: Товар с таким названием не найден на складе.")

    elif vybor == "4":
        obshaya_stoimost = 0
        for tovar in spisok_tovarov:
            obshaya_stoimost += tovar[1] * tovar[2]
        print("\nОбщая стоимость всех товаров на складе:", obshaya_stoimost)

    elif vybor == "5":
        try:
            fayl_zapis = open("products.csv", "w", encoding="utf-8")
            fayl_zapis.write(zagolovok + "\n")
            for tovar in spisok_tovarov:
                fayl_zapis.write(tovar[0] + "," + str(tovar[1]) + "," + str(tovar[2]) + "\n")
            fayl_zapis.close()
            print("Уведомление: Данные успешно сохранены обратно в файл products.csv")
        except Exception as oshibka:
            print("Ошибка при сохранении файла:", oshibka)

    elif vybor == "6":
        def sortirovka_po_cene(element):
            return element[1]


        otsortirovannyy_spisok = list(spisok_tovarov)
        otsortirovannyy_spisok.sort(key=sortirovka_po_cene)

        try:
            fayl_sort = open("sorted_products.csv", "w", encoding="utf-8")
            fayl_sort.write(zagolovok + "\n")
            for tovar in otsortirovannyy_spisok:
                fayl_sort.write(tovar[0] + "," + str(tovar[1]) + "," + str(tovar[2]) + "\n")
            fayl_sort.close()
            print("Уведомление: Отсортированные продукты сохранены в sorted_products.csv")
        except Exception as oshibka:
            print("Ошибка при сохранении файла сортировки:", oshibka)

    elif vybor == "0":
        print("Работа со складом завершена. До свидания!")
        break

    else:
        print("Ошибка: Пожалуйста, выберите существующий пункт меню (от 0 до 6).")