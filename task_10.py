def serializovat(dannye, imya="koren", uroven=0):
    probely = " " * (uroven * 4)

    if not isinstance(dannye, (dict, list)):
        return f"{probely}<{imya}>{dannye}</{imya}>\n"

    if isinstance(dannye, list):
        rezultat = ""
        for element in dannye:
            rezultat += serializovat(element, imya, uroven)
        return rezultat

    atr_stroka = ""
    vnutrennosti = ""
    est_vlozhenie = False

    for klyuch, znachenie in dannye.items():
        if klyuch.startswith('@'):
            atr_stroka += f' {klyuch[1:]}="{znachenie}"'
        elif klyuch == '#text':
            vnutrennosti += str(znachenie)
            est_vlozhenie = True
        else:
            est_vlozhenie = True
            if isinstance(znachenie, list):
                for element in znachenie:
                    vnutrennosti += serializovat(element, klyuch, uroven + 1)
            else:
                vnutrennosti += serializovat(znachenie, klyuch, uroven + 1)

    if not est_vlozhenie:
        return f"{probely}<{imya}{atr_stroka}/>\n"
    else:
        if "<" in vnutrennosti:
            return f"{probely}<{imya}{atr_stroka}>\n{vnutrennosti}{probely}</{imya}>\n"
        else:
            return f"{probely}<{imya}{atr_stroka}>{vnutrennosti}</{imya}>\n"


def deserializovat(stroka):
    nachalo_zag = stroka.find('<?')
    if nachalo_zag != -1:
        konec_zag = stroka.find('?>', nachalo_zag)
        if konec_zag != -1:
            dlina = konec_zag + 2 - nachalo_zag
            stroka = stroka[:nachalo_zag] + " " * dlina + stroka[konec_zag + 2:]

    ukazatel = 0

    def propustit_probely():
        nonlocal ukazatel
        while ukazatel < len(stroka) and stroka[ukazatel] in " \n\r\t":
            ukazatel += 1

    def parsit_uzel():
        nonlocal ukazatel
        propustit_probely()
        if ukazatel >= len(stroka): return None

        nachalo = stroka.find('<', ukazatel)
        if nachalo == -1: return None

        tekst_do = stroka[ukazatel:nachalo].strip()
        ukazatel = nachalo

        konec_tega = stroka.find('>', ukazatel)
        if konec_tega == -1:
            raise ValueError(f"na {ukazatel}")

        vnutri_tega = stroka[ukazatel + 1:konec_tega].strip()
        ukazatel = konec_tega + 1

        if vnutri_tega.startswith('/'):
            return ('konec', vnutri_tega[1:].strip(), tekst_do)

        samozakriv = False
        if vnutri_tega.endswith('/'):
            samozakriv = True
            vnutri_tega = vnutri_tega[:-1].strip()

        chasti = vnutri_tega.split(None, 1)
        imya_tega = chasti[0]

        uzel = {}
        if len(chasti) > 1:
            kuski = chasti[1].split('"')
            for i in range(0, len(kuski) - 1, 2):
                klyuch = kuski[i].replace('=', '').strip()
                if klyuch:
                    uzel["@" + klyuch] = kuski[i + 1]

        if samozakriv:
            return ('uzel', imya_tega, uzel)

        tekst_vnutri = ""
        while True:
            propustit_probely()
            if ukazatel >= len(stroka):
                raise ValueError(f"na {nachalo}")

            if stroka[ukazatel] != '<':
                sled_teg = stroka.find('<', ukazatel)
                if sled_teg == -1:
                    raise ValueError(f"na {ukazatel}")
                tekst_vnutri += stroka[ukazatel:sled_teg]
                ukazatel = sled_teg
                continue

            sohr_ukazatel = ukazatel
            rezultat = parsit_uzel()

            if rezultat is None:
                raise ValueError(f"na {ukazatel}")

            if rezultat[0] == 'konec':
                if rezultat[1] != imya_tega:
                    raise ValueError(f"na {sohr_ukazatel}")

                if rezultat[2]:
                    tekst_vnutri += rezultat[2]

                if tekst_vnutri.strip() and not uzel:
                    znachenie = tekst_vnutri.strip()
                    if znachenie.replace('.', '', 1).isdigit() and znachenie.count('.') <= 1:
                        znachenie = float(znachenie) if '.' in znachenie else int(znachenie)
                    return ('uzel', imya_tega, znachenie)
                elif tekst_vnutri.strip():
                    uzel["#text"] = tekst_vnutri.strip()

                return ('uzel', imya_tega, uzel)

            elif rezultat[0] == 'uzel':
                reb_imya = rezultat[1]
                reb_znach = rezultat[2]

                if reb_imya in uzel:
                    if type(uzel[reb_imya]) is not list:
                        uzel[reb_imya] = [uzel[reb_imya]]
                    uzel[reb_imya].append(reb_znach)
                else:
                    uzel[reb_imya] = reb_znach

    osnovnoy_uzel = parsit_uzel()
    if osnovnoy_uzel and osnovnoy_uzel[0] == 'uzel':
        return {osnovnoy_uzel[1]: osnovnoy_uzel[2]}
    return {}


def validaciya(dokument):
    try:
        deserializovat(dokument)
        print("-> Валидация: XML файл корректный и парсится без ошибок.")
        return True
    except Exception as oshibka:
        opisanie = str(oshibka)
        if "na " in opisanie:
            poziciya = int(opisanie.split("na ")[-1])
            nomer_stroki = dokument[:poziciya].count('\n') + 1
            print(f"-> Валидация: Найдена ошибка на строке {nomer_stroki}")
        else:
            print(f"-> Валидация: Ошибка в структуре XML")
        return False



if __name__ == "__main__":
    while True:
        imya_fayla = input("Введите имя XML файла (или 'vyhod' для отмены): ").strip()

        if imya_fayla.lower() == 'vyhod':
            print("Программа завершена.")
            break

        try:
            f = open(imya_fayla, "r", encoding="utf-8")
            xml_tekst = f.read()
            f.close()

            print("\n--- 1. Валидация ---")
            uspeshno = validaciya(xml_tekst)

            if uspeshno:
                print("\n--- 2. Десериализация (XML -> Python словарь) ---")
                dannie = deserializovat(xml_tekst)

                koren_teg = list(dannie.keys())[0] if dannie else "koren"
                print(f"Корневой тег определен как: <{koren_teg}>")
                print(dannie)

                print("\n--- 3. Сериализация (Python словарь -> XML) ---")
                obratniy_xml = serializovat(dannie[koren_teg], koren_teg)
                print(obratniy_xml)

            break

        except FileNotFoundError:
            print("-> ОШИБКА: Файл не найден! Убедитесь, что название введено верно и файл лежит в той же папке.\n")