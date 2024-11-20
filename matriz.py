"""semana1 = []
semana2 = []
semana3 = []
semana4 = []
cant_weeks = 0
M1 = [semana1,
      semana2,
      semana3,
      semana4
]
if cant_weeks == 0:
    for i in range(7):
        semana1.append(int(input("cuantas personas entraron? ")))
    ver_reporte_semanal = int(input("queres ver la cant de personas por semana? "))
    if ver_reporte_semanal == 1:
        print(f"la semana 1 fue {semana1}")
    cant_weeks += 1

if cant_weeks == 1:
    for i in range(7):
        semana2.append(int(input("cuantas personas entraron? ")))
    ver_reporte_semanal = int(input("queres ver la cant de personas por semana? "))
    if ver_reporte_semanal == 1:
        print(f"la semana 2 fue {semana2}")
    cant_weeks += 1   
if cant_weeks == 2:
    for i in range(7):
        semana3.append(int(input("cuantas personas entraron? ")))
    ver_reporte_semanal = int(input("queres ver la cant de personas por semana? "))
    if ver_reporte_semanal == 1:
        print(f"la semana 3 fue {semana3}")
    cant_weeks += 1
if cant_weeks == 3:
    for i in range(7):
        semana4.append(int(input("cuantas personas entraron? ")))
    ver_reporte_semanal = int(input("queres ver la cant de personas por semana? "))
    if ver_reporte_semanal == 1:
        print(f"la semana 4 fue {semana4}")
    cant_weeks += 1
for i in range(len(M1)):
    print(M1[i])

print("el tercer dia de la primera semana fue asi", M1[2][1])

total_personas = sum(sum(semana) for semana in M1)

print(f"El total de personas que entraron en el mes es: {total_personas}")"""
import datetime
import math
import serial
# Crear una matriz de 5 filas y 7 columnas, inicializada con ceros
matriz = [[0] * 7 for _ in range(5)]

# Mostrar la matriz
for fila in matriz:
    print(fila)

dia_actual = datetime.datetime.now().weekday()  # 0 = Lunes, 6 = Domingo
semana_actual = math.ceil(dia_actual / 7)

arduino = serial.Serial('COM7', 9600)
print('Conexión establecida con el Arduino.')
while arduino:
    while arduino.in_waiting > 0:
        contador = arduino.readline().decode('utf-8').strip()
        print(contador)
        matriz[semana_actual][dia_actual] = int(contador)
        
        for fila in matriz:
            print(fila)


print(dia_actual)
print(semana_actual)
