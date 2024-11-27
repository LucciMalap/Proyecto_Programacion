import datetime
from PySide2.QtWidgets import QWidget,  QSizePolicy, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFileDialog
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QColor
class EstadisticasWindow(QWidget):
    def __init__(self, arduino, main_window):
        super().__init__()
        self.setWindowTitle('Estadísticas')
        self.arduino = arduino
        self.main_window = main_window
        self.contador_actual = 0
        self.table_promedio = None
        self.setStyleSheet("QWidget {background-color: rgb(110, 194, 234);}")
        # Crear una instancia de la clase Mes para el mes actual
        hoy = datetime.datetime.now()
        self.mes_actual = Mes(hoy.strftime('%B'), hoy.month)  # Nombre y número del mes actual
        self.ultimo_dia = datetime.datetime.now().date()

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        main_layout = QVBoxLayout(self)

        self.volver_button = self.crear_boton('Volver', self.volver_a_principal)
        self.menu_label = QLabel(f'{self.mes_actual}', alignment=Qt.AlignCenter)
        self.menu_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.menu_label.setFixedHeight(20)
        main_layout.addWidget(self.menu_label)

        # Widgets secundarios (menu lateral y área de funciones)
        self.setup_sidebar()
        self.setup_funciones_widget()

        # Contenedor horizontal para el contenido principal
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.menu_widget)
        self.horizontal_layout.addWidget(self.funciones_widget)

        main_layout.addLayout(self.horizontal_layout)
        main_layout.addWidget(self.volver_button)

    def setup_sidebar(self):
        """Configura el menú lateral."""
        self.menu_widget = QWidget()
        self.menu_widget.setFixedWidth(200)
        self.menu_layout = QVBoxLayout(self.menu_widget)

        botones = [
            ('Contador', self.mostrar_contador),
            ('Matriz', self.mostrar_matriz),
            ('La Mejor Semana', self.mostrar_la_mejor_semana),
            ('La Peor Semana', self.mostrar_la_peor_semana),
            ('Sumatoria del mes', self.sumar_todos_los_valores),
            ('Descargar Mes', self.descargar_json)
        ]

        for texto, callback in botones:
            boton = self.crear_boton(texto, callback, height=50)
            self.menu_layout.addWidget(boton)

    def setup_funciones_widget(self):
        """Configura el widget de funciones principal."""
        self.funciones_widget = QWidget()
        self.funciones_layout = QVBoxLayout(self.funciones_widget)

        self.funciones_label = QLabel('Ms Farma', alignment=Qt.AlignCenter)
        self.funciones_layout.addWidget(self.funciones_label)
        self.funciones_label.hide()
        self.label_imagen = QLabel()
        pixmap = QPixmap("el_pibe_blanco_stock_photo-removebg-preview.png")  # Cambia esto por la ruta de tu imagen
        self.label_imagen.setPixmap(pixmap)
        self.label_imagen.setAlignment(Qt.AlignCenter)  # Centra la imagen
        self.funciones_layout.addWidget(self.label_imagen)
        self.table = QTableWidget(5, 7)
        self.table.setHorizontalHeaderLabels(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])

    def crear_boton(self, texto, callback, height=40):
        """Crea un botón estándar."""
        boton = QPushButton(texto)
        boton.setFixedHeight(height)
        boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        boton.clicked.connect(callback)
        return boton

    # Cambios en métodos relacionados con el manejo de la matriz y los días
    def mostrar_contador(self):
        """Muestra el último dato leído del Arduino en el layout y actualiza el contador del día correspondiente."""
        contador = None
        dia_actual = datetime.datetime.now().day  # Día actual del mes (1-31)
        
        if self.arduino:
            while self.arduino.in_waiting > 0:
                dato = self.arduino.read()
                if dato == b'S':  # Si se recibe la señal 'S'
                    contador = 1  # Incrementar el contador por cada evento

        # Verificar si el día ha cambiado
        if dia_actual != self.ultimo_dia:
            print(f"Cambio de día detectado. Reiniciando contador. Día anterior: {self.ultimo_dia}, Día actual: {dia_actual}")
            self.contador_actual = 0
            self.ultimo_dia = dia_actual  # Actualizar el día registrado

        self.label_imagen.hide()
        self.table.hide()
        if hasattr(self, 'promedio_table'):
            self.promedio_table.hide()

        self.funciones_label.show()

        if contador:
            self.contador_actual += 0.5  # Incrementar el contador por cada evento
            self.mes_actual.dias[dia_actual][0] = self.contador_actual  # Actualizar el contador para el día actual

        self.funciones_label.setText(f"Contador: {self.contador_actual}")
        self.funciones_layout.addWidget(self.funciones_label)
        
    def mostrar_matriz(self):
        if hasattr(self, 'promedio_table'):
            self.promedio_table.hide()
        self.label_imagen.hide()

        if self.arduino:
            while self.arduino.in_waiting > 0:
                # Leer lo que Arduino envía
                data = self.arduino.readline().decode('utf-8').strip()

                # Si Arduino envía "S", muestra la matriz
                if data == "S":
                    self.contador_actual += 1

                    dia_actual = datetime.datetime.now().weekday()
                    semana_actual = (dia_actual + self.mes_actual.primer_dia_semana) // 7
                    self.mes_actual.actualizar_contador(semana_actual, dia_actual, int(self.contador_actual))

            self.actualizar_tabla()

            self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.table.setMinimumSize(800, 600)
            self.table.setColumnCount(7)
            self.table.setRowCount(5)
            self.table.horizontalHeader().setStretchLastSection(False)
            self.table.verticalHeader().setStretchLastSection(False)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

            self.funciones_layout.addWidget(self.table)
            self.reemplazar_dia_con_contador()  # Esto muestra el contador actual en la tabla
            self.funciones_label.hide()
            self.table.show()

    def reemplazar_dia_con_contador(self):
        """Reemplaza el valor del día actual en la tabla con el contador, manteniendo los valores previos."""
        dia_actual = datetime.datetime.now().day  # Día actual del mes (1-31)
        columna_actual = (datetime.datetime.now().weekday())  # Día de la semana (0 a 6)
        semana_actual = (dia_actual + self.mes_actual.primer_dia_semana - 1) // 7

        self.limpiar_resaltado_tabla()

        item = self.table.item(semana_actual, columna_actual)
        if item:
            item.setText(str(self.mes_actual.dias[dia_actual][0]))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor("lightgreen"))
        else:
            self.table.setItem(semana_actual, columna_actual, QTableWidgetItem(str(self.mes_actual.dias[dia_actual][0])))

    def actualizar_tabla(self):
        """Actualiza los valores de la tabla con los datos de los días."""
        for dia in range(1, self.mes_actual.cantidad_dias + 1):
            semana_actual = (dia + self.mes_actual.primer_dia_semana - 1) // 7
            columna_actual = (datetime.datetime(self.mes_actual.anio, self.mes_actual.numero_mes, dia).weekday())
            
            contador = self.mes_actual.dias[dia][0]
            item = QTableWidgetItem(str(contador))
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setBackground(QColor("white"))  # Fondo blanco para días válidos
            self.table.setItem(semana_actual, columna_actual, item)
    def mostrar_la_mejor_semana(self):
        """Encuentra la mejor semana y la resalta en la tabla."""
        mejor_semana_idx, _ = self.mes_actual.obtener_mejor_semana()

        if mejor_semana_idx is not None:
            # Limpiar resaltados previos
            self.limpiar_resaltado_tabla()

            # Resaltar la mejor semana en verde
            for dia_idx, dia in enumerate(self.mes_actual.matriz[mejor_semana_idx]):
                if dia[0] is not None:  # Solo resaltar días válidos
                    fila = mejor_semana_idx + 1  # Índice de la semana en la tabla
                    columna = dia_idx  # Índice del día en la tabla
                    item = self.table.item(fila, columna)
                    if item:
                        item.setBackground(Qt.green)  # Resaltar en verde
    def mostrar_la_peor_semana(self):
        """Encuentra la peor semana y la resalta en la tabla."""
        peor_semana_idx, _ = self.mes_actual.obtener_peor_semana()

        if peor_semana_idx is not None:
            # Limpiar resaltados previos
            self.limpiar_resaltado_tabla()

            # Resaltar la peor semana en rojo
            for dia_idx, dia in enumerate(self.mes_actual.matriz[peor_semana_idx]):
                if dia[0] is not None:  # Solo resaltar días válidos
                    fila = peor_semana_idx  # Índice de la semana en la tabla
                    columna = dia_idx  # Índice del día en la tabla
                    item = self.table.item(fila, columna)
                    if item:
                        item.setBackground(Qt.red)  # Resaltar en rojo

    def limpiar_resaltado_tabla(self):
        """Limpia el resaltado de todas las celdas de la tabla."""
        for week in range(self.table.rowCount()):
            for day in range(self.table.columnCount()):
                item = self.table.item(week, day)
                if item:
                    item.setBackground(Qt.white)
                    
    def sumar_todos_los_valores(self):
        """Muestra la suma total de todos los valores en la matriz del mes."""
        total = self.mes_actual.sumar_todos_los_valores()
        self.funciones_label.setText(f"Contador total: {total}")
        self.label_imagen.hide()
        self.table.hide()
        if hasattr(self, 'promedio_table'):
            self.promedio_table.hide()

        self.funciones_label.show()


    def descargar_json(self):
        import json
        """Convierte el mes a formato JSON y lo guarda en un archivo, permitiendo al usuario elegir la ubicación."""
        
        # Abre un cuadro de diálogo para elegir la ubicación y nombre del archivo a guardar
        archivo_guardar, _ = QFileDialog.getSaveFileName(
            self,  # La ventana principal de la aplicación
            'Guardar archivo',  # Título del cuadro de diálogo
            '',  # Ruta inicial (vacía para mostrar el directorio predeterminado)
            'Archivos JSON (*.json)'  # Filtro para mostrar solo archivos JSON
        )

        if archivo_guardar:
            # Crear el archivo JSON en la ubicación seleccionada por el usuario
            data = {
                'mes': self.mes_actual.nombre,
                'mes_numero': self.mes_actual.numero_mes,
                'matriz': self.mes_actual.obtener_matriz()
            }
            
            # Guardar el archivo JSON en la ubicación elegida
            with open(archivo_guardar, 'w') as json_file:
                json.dump(data, json_file)

            # Mensaje para confirmar que el archivo fue guardado
            self.funciones_label.setText(f"Datos descargados a {archivo_guardar}")
            self.funciones_label.show()

    def volver_a_principal(self):
        """Cierra la ventana actual y vuelve a la principal."""
        self.close()
        self.main_window.show()
    def crear_boton(self, texto, callback, height=40):
            """Crea un botón estándar."""
            boton = QPushButton(texto)
            boton.setFixedHeight(height)
            boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            boton.setStyleSheet("""
                QPushButton {
                    background-color: rgb(66, 181, 210);  /* Fondo del botón: rojo tomate */
                    color: black;  /* Color del texto: blanco */
                    border: 2px solid rgb(70, 170, 200);  /* Borde del botón: rojo anaranjado */
                    border-radius: 15px;  /* Bordes redondeados */
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: rgb(70, 170, 200);  /* Fondo del botón al pasar el mouse: rojo anaranjado */
                }
                QPushButton:pressed {
                    background-color: rgb(50, 190, 190);  /* Fondo del botón al hacer clic: rojo indio */
                }
            """)
            boton.clicked.connect(callback)
            return boton

from calendar import monthrange
class Mes:
    def __init__(self, nombre, numero_mes):
        self.nombre = nombre  # Nombre del mes, como "Enero"
        self.numero_mes = numero_mes  # Número del mes (1-12)
        self.anio = datetime.datetime.now().year  # Año actual
        self.mes = datetime.datetime.now().month
        self.hoy = datetime.datetime.now().day

        # Calcular el primer día del mes y la cantidad de días del mes
        self.primer_dia_semana, self.cantidad_dias = monthrange(self.anio, self.numero_mes)
        
        # Crear las variables para cada día (dia_1 a dia_31)
        self.dia_1 = [0]  # Lista para el Día 1
        self.dia_2 = [0]  # Lista para el Día 2
        self.dia_3 = [0]  # Lista para el Día 3
        self.dia_4 = [0]  # Lista para el Día 4
        self.dia_5 = [0]  # Lista para el Día 5
        self.dia_6 = [0]  # Lista para el Día 6
        self.dia_7 = [0]  # Lista para el Día 7
        self.dia_8 = [0]  # Lista para el Día 8
        self.dia_9 = [0]  # Lista para el Día 9
        self.dia_10 = [0]  # Lista para el Día 10
        self.dia_11 = [0]  # Lista para el Día 11
        self.dia_12 = [0]  # Lista para el Día 12
        self.dia_13 = [0]  # Lista para el Día 13
        self.dia_14 = [0]  # Lista para el Día 14
        self.dia_15 = [0]  # Lista para el Día 15
        self.dia_16 = [0]  # Lista para el Día 16
        self.dia_17 = [0]  # Lista para el Día 17
        self.dia_18 = [0]  # Lista para el Día 18
        self.dia_19 = [0]  # Lista para el Día 19
        self.dia_20 = [0]  # Lista para el Día 20
        self.dia_21 = [0]  # Lista para el Día 21
        self.dia_22 = [0]  # Lista para el Día 22
        self.dia_23 = [0]  # Lista para el Día 23
        self.dia_24 = [0]  # Lista para el Día 24
        self.dia_25 = [0]  # Lista para el Día 25
        self.dia_26 = [0]  # Lista para el Día 26
        self.dia_27 = [0]  # Lista para el Día 27
        self.dia_28 = [0]  # Lista para el Día 28
        self.dia_29 = [0]  # Lista para el Día 29
        self.dia_30 = [0]  # Lista para el Día 30
        self.dia_31 = [0]  # Lista para el Día 31

        # Un diccionario para acceder a los días de manera flexible
        self.dias = {
            1: self.dia_1,
            2: self.dia_2,
            3: self.dia_3,
            4: self.dia_4,
            5: self.dia_5,
            6: self.dia_6,
            7: self.dia_7,
            8: self.dia_8,
            9: self.dia_9,
            10: self.dia_10,
            11: self.dia_11,
            12: self.dia_12,
            13: self.dia_13,
            14: self.dia_14,
            15: self.dia_15,
            16: self.dia_16,
            17: self.dia_17,
            18: self.dia_18,
            19: self.dia_19,
            20: self.dia_20,
            21: self.dia_21,
            22: self.dia_22,
            23: self.dia_23,
            24: self.dia_24,
            25: self.dia_25,
            26: self.dia_26,
            27: self.dia_27,
            28: self.dia_28,
            29: self.dia_29,
            30: self.dia_30,
            31: self.dia_31
        }

        # Crear una matriz 5x7 (5 semanas, 7 días)
        self.matriz = self.crear_matriz()

        # Diccionario para almacenar los contadores diarios
        self.contador_diario = {i: 0 for i in range(1, self.cantidad_dias + 1)}  # Se inicializa con 0 para cada día

    def crear_matriz(self):
        """Devuelve la matriz del mes con los días correctos en cada celda."""
        semanas = []
        dia_actual = 1
        for semana in range(5):  # 5 semanas posibles
            semana_actual = []
            for dia in range(7):  # 7 días en cada semana
                if dia_actual <= self.cantidad_dias:
                    semana_actual.append(self.dias[dia_actual])  # Agrega el contador correspondiente al día
                    dia_actual += 1
                else:
                    semana_actual.append([0])  # Si no hay más días, agrega un 0
            semanas.append(semana_actual)
        return semanas

    def obtener_matriz(self):
        """Devuelve la matriz del mes."""
        return self.matriz

    def es_dia_valido(self, semana, dia):
        """Verifica si un día es válido dentro del mes."""
        dia_del_mes = semana * 7 + dia - self.primer_dia_semana + 1
        return 1 <= dia_del_mes <= self.cantidad_dias

    def actualizar_contador(self, semana, dia, contador):
        """Actualiza el valor del contador en la celda correspondiente de la matriz y guarda el total por día."""
        if self.es_dia_valido(semana, dia):
            dia_del_mes = semana * 7 + dia - self.primer_dia_semana + 1
            if 1 <= dia_del_mes <= self.cantidad_dias:
                self.dias[dia_del_mes][0] += contador  # Actualiza el contador del día
                self.contador_diario[dia_del_mes] += contador  # Actualiza el diccionario de contadores diarios
    
    def nombre_del_dia(self):
        fecha = datetime.date(self.anio, self.mes, self.hoy)
        self.nombre_dia = fecha.strftime("%A")
        
    def obtener_primer_dia_semana(self):
        """Obtiene el día de la semana del primer día del mes (0 = lunes, 6 = domingo)."""
        primer_dia = datetime.datetime(self.anio, self.numero, 1)
        return primer_dia.weekday()

    def obtener_mejor_semana(self):
        """Calcula la semana con la mayor suma de contadores."""
        semanas_con_suma = []  # Lista para almacenar la suma de los contadores de cada semana

        # Recorremos cada fila de la matriz (semana)
        for semana_idx, semana in enumerate(self.matriz):
            # Sumar los valores de los días válidos en la semana
            suma_semana = sum(dia[0] for dia in semana if dia[0] is not None)
            semanas_con_suma.append((suma_semana, semana_idx))

        # Encontrar la semana con la mayor suma
        if semanas_con_suma:
            mejor_semana = max(semanas_con_suma, key=lambda x: x[0])
            return mejor_semana[1], mejor_semana[0]  # Índice de la mejor semana y su suma
        return None, 0  # En caso de que no haya datos
    def obtener_peor_semana(self):
        """Calcula la semana con la menor suma de contadores."""
        semanas_con_suma = []  # Lista para almacenar la suma de los contadores de cada semana

        # Recorremos cada fila de la matriz (semana)
        for semana_idx, semana in enumerate(self.matriz):
            # Sumar los valores de los días válidos en la semana
            suma_semana = sum(dia[0] for dia in semana if dia[0] is not None)
            semanas_con_suma.append((suma_semana, semana_idx))

        # Encontrar la semana con la menor suma
        if semanas_con_suma:
            peor_semana = min(semanas_con_suma, key=lambda x: x[0])
            return peor_semana[1], peor_semana[0]  # Índice de la peor semana y su suma
        return None, 0  # En caso de que no haya datos
    
    def sumar_todos_los_valores(self):
        """Suma todos los valores almacenados en los días del mes."""
        total = 0
        for dia, contador in self.dias.items():
            total += contador[0]  # Sumar el contador del día
        return total

    def __str__(self):
        return self.nombre
    
