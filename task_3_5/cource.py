# --*--: coding:utf-8 --*--
import osa
import os


def load_task1(file_name):
    fstrings = []
    print()
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
    print("{:.2f}\u00B0C".format(srv_response))


if __name__ == '__main__':
    load_task1('temps.txt')