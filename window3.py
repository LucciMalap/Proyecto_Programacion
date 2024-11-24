import math
import datetime
import json
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt

class EstadisticasWindow(QWidget):
    def __init__(self, arduino, main_window):
        super().__init__()
        self.setWindowTitle('Estadísticas')
        self.arduino = arduino
        self.main_window = main_window
        self.contador_actual = 0
                
        # Inicializar la matriz
        self.matriz = [[0] * 7 for _ in range(5)]

        # Obtener el día actual
        hoy = datetime.datetime.now()

        # Calcular el día de la semana (0=lunes, 6=domingo)
        self.dia_actual = hoy.weekday()

        # Calcular la semana actual (1-5)
        self.semana_actual = math.ceil(hoy.day / 7)

        # Actualizar la matriz con el contador
        self.matriz[self.semana_actual - 1][self.dia_actual] = self.contador_actual  # Restamos 1 para que empiece en índice 0

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        main_layout = QVBoxLayout(self)

        self.volver_button = self.crear_boton('Volver', self.volver_a_principal)
        self.menu_label = QLabel('Menu', alignment=Qt.AlignCenter)
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
            ('Promedio Diario', self.mostrar_promedio_diario),
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
        
        self.table = QTableWidget(5, 7)
        self.table.setHorizontalHeaderLabels(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])
    
    def crear_boton(self, texto, callback, height=40):
        """Crea un botón estándar."""
        boton = QPushButton(texto)
        boton.setFixedHeight(height)
        boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        boton.clicked.connect(callback)
        return boton

    def mostrar_contador(self):
        """Muestra el último dato leído del Arduino en el layout."""
        contador = None
        if self.arduino:
            while self.arduino.in_waiting > 0:
                contador = self.arduino.readline().decode('utf-8').strip()
        
        self.table.hide()
        self.funciones_label.show()
        
        if contador:
            self.contador_actual = contador
        
        
        print(f'Datos recibidos del Arduino: {self.contador_actual}')
        self.funciones_label.setText(f"Contador: {self.contador_actual}")
        self.funciones_layout.addWidget(self.funciones_label)

    def mostrar_matriz(self):
        """Muestra la matriz de contadores (calendario) en el layout."""
        if self.arduino:
            while self.arduino.in_waiting > 0:
                self.contador_actual = self.arduino.readline().decode('utf-8').strip()
                self.matriz[self.semana_actual][self.dia_actual] = int(self.contador_actual)
        
        self.actualizar_tabla()

        # Asegurarse de que la tabla ocupe todo el espacio disponible
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Expandir a todo el espacio disponible
        self.table.setMinimumSize(800, 600)  # Puedes ajustar estos valores para darle el tamaño que desees

        # Ajustar la tabla para que las celdas se expandan por igual
        self.table.horizontalHeader().setStretchLastSection(False)  # Desactiva el estiramiento solo de la última columna
        self.table.verticalHeader().setStretchLastSection(False)    # Desactiva el estiramiento solo de la última fila

        self.table.setColumnCount(7)  # Aseguramos que tenga 7 columnas (uno por cada día)
        self.table.setRowCount(5)     # Aseguramos que tenga 5 filas (uno por cada semana)

        # Hacer que todas las celdas se estiren por igual
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Ajusta todas las columnas
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)    # Ajusta todas las filas

        # Agregar la tabla al layout
        self.funciones_layout.addWidget(self.table)

        self.funciones_label.hide()
        self.table.show()

    def actualizar_tabla(self):
        """Actualiza los valores de la tabla con los datos de la matriz."""
        for semana in range(5):
            for dia in range(7):
                # Crear un nuevo QTableWidgetItem para cada celda
                item = QTableWidgetItem(str(self.matriz[semana][dia]))

                # Centrar el texto en cada celda
                item.setTextAlignment(Qt.AlignCenter)

                # Hacer la celda de solo lectura (no editable)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                # Insertar el item en la tabla en la posición correspondiente
                self.table.setItem(semana, dia, item)

        # Ajustar las celdas de acuerdo al tamaño de la tabla
        for col in range(7):  # 7 columnas (Lunes, Martes, etc.)
            self.table.setColumnWidth(col, self.table.width() // 7)  # Divide el ancho total entre las 7 columnas

        for row in range(5):  # 5 filas (semanas)
            self.table.setRowHeight(row, self.table.height() // 5)  # Divide la altura total entre las 5 filas

    def mostrar_la_mejor_semana(self):
        """Encuentra la semana con la mayor suma de contadores y la devuelve."""
        
        if self.arduino:
            while self.arduino.in_waiting > 0:
                self.contador_actual = self.arduino.readline().decode('utf-8').strip()
                self.matriz[self.semana_actual][self.dia_actual] = int(self.contador_actual)
        
        self.table.hide()
        self.funciones_label.show()
        
        # Creamos una lista de tuplas (suma de la semana, índice de la semana)
        semanas_con_suma = [(sum(self.matriz[fila]), fila) for fila in range(len(self.matriz))]
        
        # Ordenamos la lista de semanas por la suma en orden descendente
        semanas_con_suma.sort(reverse=True, key=lambda x: x[0])

        # La mejor semana es la que tiene la mayor suma
        mejor_semana = semanas_con_suma[0][1]

        self.funciones_label.setText(f"La mejor semana es la semana {mejor_semana + 1} con una suma total de contadores de {semanas_con_suma[0][0]}.")

    def mostrar_la_peor_semana(self):
        """Encuentra la semana con la menor suma de contadores y la devuelve."""
        
        if self.arduino:
            while self.arduino.in_waiting > 0:
                self.contador_actual = self.arduino.readline().decode('utf-8').strip()
                self.matriz[self.semana_actual][self.dia_actual] = int(self.contador_actual)
        
        self.table.hide()
        self.funciones_label.show()
        
        # Creamos una lista de tuplas (suma de la semana, índice de la semana)
        semanas_con_suma = [(sum(self.matriz[fila]), fila) for fila in range(len(self.matriz))]
        
        # Ordenamos la lista de semanas por la suma en orden ascendente (de menor a mayor)
        semanas_con_suma.sort(key=lambda x: x[0])

        # La peor semana es la que tiene la menor suma
        peor_semana = semanas_con_suma[0][1]

        self.funciones_label.setText(f"La peor semana es la semana {peor_semana + 1} con una suma total de contadores de {semanas_con_suma[0][0]}.")

    def mostrar_promedio_diario(self):
        """Muestra el promedio de los valores de la matriz para cada día de la semana, ignorando los valores en 0."""
        
        if self.arduino:
            while self.arduino.in_waiting > 0:
                self.contador_actual = self.arduino.readline().decode('utf-8').strip()
                self.matriz[self.semana_actual][self.dia_actual] = int(self.contador_actual)
                
        self.table.hide()
        self.funciones_label.show()
        
        promedios = []
        
        semanas_a_considerar = self.semana_actual + 1  # Consideramos todas las semanas transcurridas

        for dia in range(7):  # 7 días de la semana
            total = 0
            count = 0
            for semana in range(semanas_a_considerar):  # Solo semanas transcurridas
                valor = self.matriz[semana][dia]
                total += valor
                count += 1  # Contamos todos los valores, incluidos los ceros
                
            promedio = total / count if count > 0 else 0  # Promedio incluye ceros
            promedios.append(promedio)

        # Mostrar los promedios de cada día en el label
        promedio_texto = "Promedio Diario:\n"
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        for i, promedio in enumerate(promedios):
            promedio_texto += f"{dias[i]}: {promedio:.2f}\n"

        self.funciones_label.setText(promedio_texto)
        self.funciones_layout.addWidget(self.funciones_label)
        
    def descargar_json(self):
        """Exporta los valores de la matriz a un archivo JSON, solo incluyendo las semanas con datos."""
        
        calendario = []
        
        # Iteramos sobre las semanas y guardamos solo las que tienen datos (donde al menos uno de los días es distinto de cero)
        for semana_idx, semana in enumerate(self.matriz):
            # Si la semana tiene al menos un valor distinto de 0
            if any(valor != 0 for valor in semana):
                semana_dict = {
                    "semana": semana_idx + 1,  # Semana (empezamos desde 1)
                    "lunes": semana[0],
                    "martes": semana[1],
                    "miercoles": semana[2],
                    "jueves": semana[3],
                    "viernes": semana[4],
                    "sabado": semana[5],
                    "domingo": semana[6],
                }
                calendario.append(semana_dict)
        
        # Crear un diccionario con los datos
        datos = {
            "calendario": calendario,
        }

        # Abrir un diálogo para guardar el archivo
        ruta_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Matriz como JSON", "", "Archivos JSON (*.json)")

        if ruta_archivo:
            try:
                # Guardar el archivo como JSON
                with open(ruta_archivo, 'w') as archivo_json:
                    json.dump(datos, archivo_json, indent=4)  # El indent asegura que el JSON sea legible
                print(f"Matriz exportada exitosamente a: {ruta_archivo}")
            except Exception as e:
                print(f"Error al exportar la matriz: {e}")

    def volver_a_principal(self):
        from window1 import MainWindow  # Importar aquí para evitar la importación circular
        self.ventana_principal = MainWindow()  # Crear la ventana principal
        self.ventana_principal.show()  # Mostrar la ventana principal
        self.close()  # Cerrar la ventana secundaria
