#!/usr/bin/python3

import csv

dest = open("destino.csv", "w")
fields = ["Año", "Mes/dia", "DESCRIPCIÓN", "VALOR", "CORREGIDO", "SALDO"]
dicw = csv.DictWriter(dest, fieldnames=fields)
dicw.writeheader()

with open("ExtractoCuenta.csv") as csv_file:
    dicr = csv.DictReader(csv_file)

    for i in dicr:
        print("valor:", i["VALOR"], "Corregido:", i["CORREGIDO"])
        data = i["VALOR"]
        i["CORREGIDO"] = data.replace(",", "").replace(".", ",")
        print("valor:", i["VALOR"], "Corregido:", i["CORREGIDO"])
        print(i)

        dicw.writerow(i)
