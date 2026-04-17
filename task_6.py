import struct
import time

imya_fayla = "telemetry.bin"

try:
    fayl_proverka = open(imya_fayla, "rb")
    fayl_proverka.close()
except FileNotFoundError:
    try:
        fayl_sozdanie = open(imya_fayla, "wb")

        zagolovok = struct.pack("<4s H I", b"DATA", 1, 3)
        fayl_sozdanie.write(zagolovok)

        vremya_seychas = int(time.time())
        zapis_1 = struct.pack("<Q I h B", vremya_seychas, 1001, 2450, 1)
        zapis_2 = struct.pack("<Q I h B", vremya_seychas - 3600, 1002, 2200, 0)
        zapis_3 = struct.pack("<Q I h B", vremya_seychas - 7200, 1003, -150, 3)

        fayl_sozdanie.write(zapis_1)
        fayl_sozdanie.write(zapis_2)
        fayl_sozdanie.write(zapis_3)
        fayl_sozdanie.close()
        print("Уведомление: Тестовый бинарный файл успешно создан.")
    except Exception as oshibka:
        print("Ошибка при подготовке данных:", oshibka)

try:
    fayl_chtenie = open(imya_fayla, "rb")

    bayty_zagolovka = fayl_chtenie.read(10)

    raspakovannyy_zagolovok = struct.unpack("<4s H I", bayty_zagolovka)
    signatura = raspakovannyy_zagolovok[0]
    versiya = raspakovannyy_zagolovok[1]
    kolichestvo_zapisey = raspakovannyy_zagolovok[2]

    if signatura != b'DATA':
        print("Ошибка: Неверный формат файла.")
    else:
        print("Файл прочитан. Версия:", versiya, "| Записей:", kolichestvo_zapisey)

        summa_temperatur = 0.0
        kolichestvo_aktivnyh_flagov = 0

        for i in range(kolichestvo_zapisey):
            bayty_zapisi = fayl_chtenie.read(15)

            if len(bayty_zapisi) < 15:
                break

            raspakovannaya_zapis = struct.unpack("<Q I h B", bayty_zapisi)

            metka_vremeni = raspakovannaya_zapis[0]
            id_zapisi = raspakovannaya_zapis[1]
            syraya_temperatura = raspakovannaya_zapis[2]
            flag_sostoyaniya = raspakovannaya_zapis[3]

            realnaya_temperatura = syraya_temperatura / 100
            summa_temperatur += realnaya_temperatura

            if flag_sostoyaniya > 0:
                kolichestvo_aktivnyh_flagov += 1

            print(f"ID: {id_zapisi} | Температура: {realnaya_temperatura} C | Флаг: {flag_sostoyaniya}")

        if kolichestvo_zapisey > 0:
            srednyaya_temperatura = summa_temperatur / kolichestvo_zapisey
            print("\n--- Итоговые показатели ---")
            print("Средняя температура:", round(srednyaya_temperatura, 2))
            print("Всего активных флагов:", kolichestvo_aktivnyh_flagov)

    fayl_chtenie.close()

except FileNotFoundError:
    print("Ошибка: Файл не найден.")
except struct.error:
    print("Ошибка: Нарушена структура данных в файле.")
except Exception as oshibka:
    print("Системная ошибка:", oshibka)