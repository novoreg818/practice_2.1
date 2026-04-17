try:
    fayl_sozdanie = open("students.txt", "w", encoding="utf-8")
    fayl_sozdanie.write("Иванов Иван:5,4,3,5\nПетров Петр:4,3,4,4\nСидорова Мария:5,5,5,5\nСмирнов Алексей:2,3,2,3\n")
    fayl_sozdanie.close()
    print("Уведомление: Исходный файл 'students.txt' автоматически создан для проверки.")

    fayl_chtenie = open("students.txt", "r", encoding="utf-8")
    vse_studenty = fayl_chtenie.readlines()
    fayl_chtenie.close()

    fayl_zapis = open("result.txt", "w", encoding="utf-8")

    luchshiy_student = ""
    hudshiy_student = ""
    max_ball = 0.0
    min_ball = 6.0

    for student in vse_studenty:
        chistaya_stroka = student.strip()
        if chistaya_stroka == "":
            continue

        chasti = chistaya_stroka.split(":")
        imya_studenta = chasti[0]
        ocenki_tekstom = chasti[1].split(",")

        summa = 0
        kolichestvo = len(ocenki_tekstom)

        for ocenka in ocenki_tekstom:
            summa += int(ocenka)

        sredniy_ball = summa / kolichestvo

        if sredniy_ball > 4.0:
            fayl_zapis.write(imya_studenta + " - " + str(sredniy_ball) + "\n")

        if sredniy_ball > max_ball:
            max_ball = sredniy_ball
            luchshiy_student = imya_studenta

        if sredniy_ball < min_ball:
            min_ball = sredniy_ball
            hudshiy_student = imya_studenta

    fayl_zapis.close()

    print("Уведомление: Анализ завершен. Отличники и хорошисты сохранены в 'result.txt'.")
    print("\n--- Статистика по группе ---")
    print("Лучший студент:", luchshiy_student, "- средний балл:", max_ball)
    print("Худший студент:", hudshiy_student, "- средний балл:", min_ball)

except FileNotFoundError:
    print("Ошибка: Файл 'students.txt' не найден на диске!")
except ValueError:
    print("Ошибка в данных: Проверьте файл, оценки должны быть цифрами, а не буквами!")
except Exception as oshibka:
    print("Произошла неизвестная системная ошибка:", oshibka)