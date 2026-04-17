import math
import datetime

imya_fayla = "calculator.log"

print("--- История последних 5 операций ---")
try:
    fayl_chtenie = open(imya_fayla, "r", encoding="utf-8")
    vse_stroki = fayl_chtenie.readlines()
    fayl_chtenie.close()

    poslednie_5 = vse_stroki[-5:]
    if len(poslednie_5) == 0:
        print("История пуста.")
    else:
        for stroka in poslednie_5:
            print(stroka.strip())
except FileNotFoundError:
    print("Лог-файл еще не создан, история пуста.")
except Exception as oshibka:
    print("Ошибка при чтении лога:", oshibka)

while True:
    print("\n--- Калькулятор ---")
    print("Доступные операции: +, -, *, /, log, sin")
    print("Введите 'clear' для очистки лога или '0' для выхода.")

    operaciya = input("Выберите операцию (или команду): ").strip().lower()

    if operaciya == '0':
        print("Работа с калькулятором завершена.")
        break

    if operaciya == 'clear':
        try:
            fayl_zapis = open(imya_fayla, "w", encoding="utf-8")
            fayl_zapis.close()
            print("Уведомление: Лог-файл успешно очищен!")
        except Exception as oshibka:
            print("Ошибка очистки:", oshibka)
        continue

    if operaciya not in ['+', '-', '*', '/', 'log', 'sin']:
        print("Ошибка: Введена неизвестная операция. Попробуйте снова.")
        continue

    try:
        chislo1 = float(input("Введите первое число: "))
        chislo2 = 0.0

        if operaciya not in ['log', 'sin']:
            chislo2 = float(input("Введите второе число: "))

        rezultat = 0
        vremya_seychas = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        zapis_v_log = ""

        if operaciya == '+':
            rezultat = chislo1 + chislo2
            zapis_v_log = f"[{vremya_seychas}] {chislo1} + {chislo2} = {rezultat}"
        elif operaciya == '-':
            rezultat = chislo1 - chislo2
            zapis_v_log = f"[{vremya_seychas}] {chislo1} - {chislo2} = {rezultat}"
        elif operaciya == '*':
            rezultat = chislo1 * chislo2
            zapis_v_log = f"[{vremya_seychas}] {chislo1} * {chislo2} = {rezultat}"
        elif operaciya == '/':
            if chislo2 == 0:
                print("Ошибка: На ноль делить нельзя!")
                continue
            rezultat = chislo1 / chislo2
            zapis_v_log = f"[{vremya_seychas}] {chislo1} / {chislo2} = {rezultat}"
        elif operaciya == 'log':
            if chislo1 <= 0:
                print("Ошибка: Логарифм вычисляется только из положительных чисел!")
                continue
            rezultat = math.log10(chislo1)
            zapis_v_log = f"[{vremya_seychas}] log({chislo1}) = {rezultat}"
        elif operaciya == 'sin':
            rezultat = math.sin(chislo1)
            zapis_v_log = f"[{vremya_seychas}] sin({chislo1}) = {rezultat}"

        print("Результат:", rezultat)

        try:
            fayl_log = open(imya_fayla, "a", encoding="utf-8")
            fayl_log.write(zapis_v_log + "\n")
            fayl_log.close()
        except Exception as oshibka:
            print("Ошибка при записи в лог-файл:", oshibka)

    except ValueError:
        print("Ошибка: Вводить нужно только числа (для дробей используйте точку)!")
    except Exception as oshibka:
        print("Неизвестная системная ошибка:", oshibka)