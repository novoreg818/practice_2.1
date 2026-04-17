imya_fayla = "text.txt"

spisok_strok = [
    "Первая строка текста.\n",
    "Вторая строка для задачи.\n",
    "Третья короткая.\n",
    "Четвертая строка будет самой длинной в этом текстовом файле.\n",
    "Пятая строка завершает работу программы.\n"
]

try:
    fayl_zapis = open(imya_fayla, "w", encoding="utf-8")
    for stroka in spisok_strok:
        fayl_zapis.write(stroka)
    fayl_zapis.close()
    print("Уведомление: Файл успешно создан и данные записаны.")

    fayl_chtenie = open(imya_fayla, "r", encoding="utf-8")
    vse_stroki = fayl_chtenie.readlines()
    fayl_chtenie.close()

    kolichestvo_strok = 0
    kolichestvo_slov = 0
    samaya_dlinnaya_stroka = ""
    kolichestvo_glasnyh = 0
    kolichestvo_soglasnyh = 0

    vse_glasnye = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
    vse_soglasnye = "бвгджзйклмнпрстфхцчшщБВГДЖЗЙКЛМНПРСТФХЦЧШЩ"

    for tekushaya_stroka in vse_stroki:
        kolichestvo_strok += 1
        chistaya_stroka = tekushaya_stroka.strip()

        slova = chistaya_stroka.split()
        kolichestvo_slov += len(slova)

        if len(chistaya_stroka) > len(samaya_dlinnaya_stroka):
            samaya_dlinnaya_stroka = chistaya_stroka

        for bukva in chistaya_stroka:
            if bukva in vse_glasnye:
                kolichestvo_glasnyh += 1
            elif bukva in vse_soglasnye:
                kolichestvo_soglasnyh += 1

    print("\n--- Результаты анализа файла ---")
    print("Количество строк в файле:", kolichestvo_strok)
    print("Общее количество слов:", kolichestvo_slov)
    print("Самая длинная строка:", samaya_dlinnaya_stroka)
    print("Количество гласных букв:", kolichestvo_glasnyh)
    print("Количество согласных букв:", kolichestvo_soglasnyh)

except Exception as oshibka:
    print("Произошла системная ошибка при работе с файлом! Детали:", oshibka)