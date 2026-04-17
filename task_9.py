def serializovat(dannye, otstup=None, uroven=0):
    probely = " " * (otstup * uroven) if otstup is not None else ""
    sleduyushiy_probely = " " * (otstup * (uroven + 1)) if otstup is not None else ""
    razdelitel = ",\n" if otstup is not None else ","
    klyuch_razdelitel = ": " if otstup is not None else ":"

    if dannye is None:
        return "null"
    elif isinstance(dannye, bool):
        return "true" if dannye else "false"
    elif isinstance(dannye, (int, float)):
        return str(dannye)
    elif isinstance(dannye, str):
        return f'"{dannye}"'
    elif isinstance(dannye, list):
        if not dannye:
            return "[]"
        elementy = [serializovat(it, otstup, uroven + 1) for it in dannye]
        if otstup is not None:
            vnutri = razdelitel.join(sleduyushiy_probely + e for e in elementy)
            return f"[\n{vnutri}\n{probely}]"
        return f"[{','.join(elementy)}]"
    elif isinstance(dannye, dict):
        if not dannye:
            return "{}"
        pary = []
        for klyuch, znachenie in dannye.items():
            s_klyuch = f'"{klyuch}"'
            s_znachenie = serializovat(znachenie, otstup, uroven + 1)
            if otstup is not None:
                pary.append(f"{sleduyushiy_probely}{s_klyuch}{klyuch_razdelitel}{s_znachenie}")
            else:
                pary.append(f"{s_klyuch}:{s_znachenie}")
        if otstup is not None:
            return "{\n" + razdelitel.join(pary) + "\n" + probely + "}"
        return "{" + ",".join(pary) + "}"


def deserializovat(stroka):
    ukazatel = 0

    def propustit_pustotu():
        nonlocal ukazatel
        while ukazatel < len(stroka) and stroka[ukazatel] in " \n\r\t":
            ukazatel += 1

    def parsit():
        nonlocal ukazatel
        propustit_pustotu()
        if ukazatel >= len(stroka):
            raise ValueError(f"na {ukazatel}")

        simvol = stroka[ukazatel]
        if simvol == '"': return parsit_stroku()
        if simvol == '{': return parsit_slovar()
        if simvol == '[': return parsit_spisok()
        if stroka.startswith("true", ukazatel):
            ukazatel += 4
            return True
        if stroka.startswith("false", ukazatel):
            ukazatel += 5
            return False
        if stroka.startswith("null", ukazatel):
            ukazatel += 4
            return None
        return parsit_chislo()

    def parsit_stroku():
        nonlocal ukazatel
        ukazatel += 1
        nachalo = ukazatel
        while ukazatel < len(stroka) and stroka[ukazatel] != '"':
            ukazatel += 1
        rezultat = stroka[nachalo:ukazatel]
        ukazatel += 1
        return rezultat

    def parsit_chislo():
        nonlocal ukazatel
        nachalo = ukazatel
        if stroka[ukazatel] == '-':
            ukazatel += 1
        while ukazatel < len(stroka) and (stroka[ukazatel].isdigit() or stroka[ukazatel] == '.'):
            ukazatel += 1
        fragment = stroka[nachalo:ukazatel]
        if not fragment or fragment == '-':
            raise ValueError(f"na {ukazatel}")
        return float(fragment) if '.' in fragment else int(fragment)

    def parsit_spisok():
        nonlocal ukazatel
        ukazatel += 1
        spisok = []
        propustit_pustotu()
        if ukazatel < len(stroka) and stroka[ukazatel] == ']':
            ukazatel += 1
            return spisok
        while True:
            spisok.append(parsit())
            propustit_pustotu()
            if ukazatel >= len(stroka):
                raise ValueError(f"na {ukazatel}")
            if stroka[ukazatel] == ']':
                ukazatel += 1
                break
            if stroka[ukazatel] != ',':
                raise ValueError(f"na {ukazatel}")
            ukazatel += 1
        return spisok

    def parsit_slovar():
        nonlocal ukazatel
        ukazatel += 1
        slovar = {}
        propustit_pustotu()
        if ukazatel < len(stroka) and stroka[ukazatel] == '}':
            ukazatel += 1
            return slovar
        while True:
            propustit_pustotu()
            if ukazatel >= len(stroka) or stroka[ukazatel] != '"':
                raise ValueError(f"na {ukazatel}")
            klyuch = parsit_stroku()
            propustit_pustotu()
            if ukazatel >= len(stroka) or stroka[ukazatel] != ':':
                raise ValueError(f"na {ukazatel}")
            ukazatel += 1
            slovar[klyuch] = parsit()
            propustit_pustotu()
            if ukazatel >= len(stroka):
                raise ValueError(f"na {ukazatel}")
            if stroka[ukazatel] == '}':
                ukazatel += 1
                break
            if stroka[ukazatel] != ',':
                raise ValueError(f"na {ukazatel}")
            ukazatel += 1
        return slovar

    rezultat = parsit()
    propustit_pustotu()
    if ukazatel < len(stroka):
        raise ValueError(f"na {ukazatel}")
    return rezultat


def validaciya(tekst):
    try:
        deserializovat(tekst)
        print("-> Валидация: JSON файл корректный и парсится без ошибок.")
        return True
    except Exception as oshibka:
        opisanie = str(oshibka)
        if "na " in opisanie:
            poziciya = int(opisanie.split("na ")[-1])
            nomer_stroki = tekst[:poziciya].count('\n') + 1
            print(f"-> Валидация: Найдена ошибка в JSON на строке {nomer_stroki}")
        else:
            print(f"-> Валидация: Ошибка в структуре JSON")
        return False


if __name__ == "__main__":
    while True:
        imya_fayla = input("\nВведите имя JSON файла (или 'vyhod' для отмены): ").strip()

        if imya_fayla.lower() == 'vyhod':
            print("Программа завершена.")
            break

        try:
            f = open(imya_fayla, "r", encoding="utf-8")
            json_tekst = f.read()
            f.close()

            print("\n--- 1. Валидация ---")
            uspeshno = validaciya(json_tekst)

            if uspeshno:
                print("\n--- 2. Десериализация (JSON -> Python словарь) ---")
                dannie = deserializovat(json_tekst)
                print(dannie)

                print("\n--- 3. Вывод JSON объекта с N-отступами (Сериализация) ---")
                vvod_otstupa = input("Введите количество пробелов N для отступа (например, 4 или 2): ").strip()
                try:
                    n = int(vvod_otstupa)
                except ValueError:
                    print("Введено не число. Используем отступ 4 по умолчанию.")
                    n = 4

                obratniy_json = serializovat(dannie, otstup=n)
                print("\nРезультат:")
                print(obratniy_json)

            break

        except FileNotFoundError:
            print("-> ОШИБКА: Файл не найден! Убедитесь, что название введено верно и файл лежит в той же папке.")