semana1 = []
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

print(f"El total de personas que entraron en el mes es: {total_personas}")