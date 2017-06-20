# --*--: coding:utf-8 --*--
import osa
import os


def load_task1(file_name):
    fstrings = []
    URL = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
    if os.path.isfile(file_name):
        with open(file_name, 'r') as fhndl:
            fstrings = fhndl.readlines()
    avg_temperature = 0
    for value in fstrings:
        avg_temperature += float(value.split(' ')[0])
    avg_temperature /= len(fstrings)
    sclient = osa.Client(URL)
    fromUnit = 'degreeFahrenheit'
    toUnit = 'degreeCelsius'
    srv_response = sclient.service.ConvertTemp(avg_temperature, fromUnit, toUnit)
    print("Средняя температура: {:.2f}\u00B0C".format(srv_response))

def load_task2(file_name):
    CONVERT_URL = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
    sclient = osa.Client(CONVERT_URL)
    # srv_response = sclient.service.ConvertToNum(fromCurrency = 'USD', toCurrency = 'RUB', amount = 100.0, rounding = True)
    trip_cost = 0
    if os.path.isfile(file_name):
        with open(file_name, 'r') as fhndl:
            for file_line in fhndl.readlines():
                line_components = file_line.split(' ')
                currency = line_components[2].strip()
                read_amount = line_components[1]
                srv_response = sclient.service.ConvertToNum(fromCurrency=currency, toCurrency='RUB',
                                                            amount=read_amount, rounding=True)
                trip_cost += round(srv_response, 0)
    print('Стоимость путешевствия: {} руб.'.format(int(trip_cost)))

def load_task3(file_name):
    pass


if __name__ == '__main__':
    # load_task1('temps.txt')
    load_task2('currencies.txt')