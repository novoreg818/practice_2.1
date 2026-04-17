try:
    fayl_test = open("secret_test.txt", "rb")
    fayl_test.close()
except FileNotFoundError:
    try:
        fayl_sozdanie = open("secret_test.txt", "wb")
        fayl_sozdanie.write(b"Hello! This is a secret message for testing.")
        fayl_sozdanie.close()
        print("Уведомление: Автоматически создан тестовый файл 'secret_test.txt'.")
    except Exception as oshibka:
        print("Ошибка при создании тестового файла:", oshibka)

while True:
    print("\n--- Программа шифрования ---")
    print("1. Зашифровать файл")
    print("2. Расшифровать файл")
    print("0. Выход")

    vybor = input("Выберите действие: ").strip()

    if vybor == "0":
        print("Работа завершена.")
        break

    if vybor not in ["1", "2"]:
        print("Ошибка: выберите 1, 2 или 0.")
        continue

    vhodnoy_fayl = input("Введите имя исходного файла (например, secret_test.txt): ").strip()
    vyhodnoy_fayl = input("Введите имя файла для сохранения результата: ").strip()

    try:
        klyuch = int(input("Введите числовой ключ шифрования (от 0 до 255): "))
        if klyuch < 0 or klyuch > 255:
            print("Ошибка: ключ должен занимать ровно 1 байт (быть от 0 до 255)!")
            continue

        fayl_chtenie = open(vhodnoy_fayl, "rb")
        ishodnye_bayty = fayl_chtenie.read()
        fayl_chtenie.close()

        rezultat_bayty = bytearray()

        if vybor == "1":
            for bayt in ishodnye_bayty:
                sdvig_vlevo = ((bayt << 2) | (bayt >> 6)) & 255
                zashifrovannyy_bayt = sdvig_vlevo ^ klyuch
                rezultat_bayty.append(zashifrovannyy_bayt)
            print("Уведомление: Файл успешно зашифрован!")

        elif vybor == "2":
            for bayt in ishodnye_bayty:
                posle_xor = bayt ^ klyuch
                sdvig_vpravo = ((posle_xor >> 2) | (posle_xor << 6)) & 255
                rezultat_bayty.append(sdvig_vpravo)
            print("Уведомление: Файл успешно расшифрован!")

        fayl_zapis = open(vyhodnoy_fayl, "wb")
        fayl_zapis.write(rezultat_bayty)
        fayl_zapis.close()

    except FileNotFoundError:
        print("Ошибка: Исходный файл с таким именем не найден!")
    except ValueError:
        print("Ошибка ввода: Ключ должен быть целым числом!")
    except Exception as oshibka:
        print("Неизвестная ошибка:", oshibka)