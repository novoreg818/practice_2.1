import os

nazvanie_fayla = "dannye.txt"
vremenny_fayl = "vremenny_fayl.txt"

if not os.path.exists(nazvanie_fayla):
    with open(nazvanie_fayla, "w") as f:
        pass

while True:
    print("\n--- Программа запущена (введите число или нажмите Ctrl+C для выхода) ---")
    vvod_polzovatelya = input("Введите число: ")

    try:
        chislo = float(vvod_polzovatelya)

        if chislo % 7 == 0:
            print(f"Число {chislo} кратно 7! Оно будет обработано по формуле.")
        else:
            print(f"Число {chislo} не кратно 7. Просто сохраняем в файл.")


        with open(nazvanie_fayla, "a") as f_zapis:
            f_zapis.write(str(chislo) + "\n")


        with open(nazvanie_fayla, "r") as f_chtenie:
            with open(vremenny_fayl, "w") as f_novy:
                for stroka in f_chtenie:
                    znachenie_v_stroke = stroka.strip()
                    if not znachenie_v_stroke:
                        continue

                    tekushee_chislo = float(znachenie_v_stroke)

                    if tekushee_chislo % 7 == 0:
                        # x * 100 / (73**2 + 29)
                        itog = tekushee_chislo * 100 / (73 ** 2 + 29)
                        f_novy.write(str(itog) + "\n")
                        print(f"Результат операции для {tekushee_chislo}: {itog}")
                    else:
                        f_novy.write(str(tekushee_chislo) + "\n")


        if os.path.exists(nazvanie_fayla):
            os.remove(nazvanie_fayla)
        os.rename(vremenny_fayl, nazvanie_fayla)

        print("Данные в файле успешно обновлены.")

    except ValueError:
        print("Ошибка: Вы ввели не число. Программа продолжает работу...")
    except Exception as oshibka:
        print(f"Произошла непредвиденная ошибка: {oshibka}")