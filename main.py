# Общие рекомендации:
# - оставлять документацию для всех публичных модулей, функций, классов, методов.
# - можно использовать generator expressions для итерации по циклам с условием вида:
#       for i in items:
#           if condition:
#               ...
# - нарушено требование НЕ применять бэкслеши для переносов
#   (https://docs.google.com/document/d/1s_FqVkqOASwXK0DkOJZj5RzOm4iWBO5voc_8kenxXbw/)


import datetime as dt


class Record:
    # почему значение по умолчанию для date - пустая строка?
    # возможно, для неинициализированный даты можно выбрать более информативное значение? Например, None
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # 1) такое форматирование тернарного оператора (условие на 3 разных строчках) имеет слабочитаемую струтуру
        # 2) входные данные могут не быть приведены к ожидаемому формату (date='123')
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # наименование переменный не соответствует стандарту PEP8
        # + как следствие, есть пересечение в названии локальной переменной и класса Record
        for Record in self.records:
            # на каждой итерации цикла идет вызов целой цепочки методов для вычисления сегодняшней даты,
            # сама же дата за это время не меняется.
            if Record.date == dt.datetime.now().date():
                # есть более компактная запись присвоения - "+="
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # в случае сравнения диапозонов, лучше использовать chaining comparison (цепочки операторов сравнения)
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # документация гораздо читаемей и поддерживается в автоподсказках многих IDE,
    # см. PEP 257 и общие рекомендации в начале файла
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # неинформатичное название переменной
        x = self.limit - self.get_today_stats()
        # с помощью тернарного оператора можно сделать код компактней
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # скобки являются лишними символами
            return('Хватит есть!')


class CashCalculator(Calculator):
    # нет необходимости приводить к float
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # согласно исходной задаче, входной параметр для метода только валюта
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # не учтен случай, когда currency не является ни одной из валют (else условие)

        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # тут перемутан оператор присвоения с оператором сравнения?
            cash_remained == 1.00
            currency_type = 'руб'
        # для улучшения читабильности лучше отделять большие блоки логически связанного кода (один блок if от другого)
        if cash_remained > 0:
            # в f-строках применяется только подстановка переменных и нет логических или арифметических операций, вызовов функций и подобной динамики.
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # плохая идея точного сравнения для чисел с плавающей точкой
        # например:
        # 2.2 * 3.0 == 6.6 - False
        # 3.3 * 2.0 == 6.6 - True
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # фактически, этот elif лишний - основные условия проверены выше, а тут остаточный кейс
        elif cash_remained < 0:
            # если по коду везде используется f'', то лучше сохранить этот стиль и удалить format отсюда
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # метод с такой функциональностью и названием уже есть в базовом классе
    def get_week_stats(self):
        # к тому же, метод с названием get_*** ничего не возвращает
        super().get_week_stats()
