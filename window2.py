import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import  Qt
import serial
import math
import datetime
import json

class FuncionesWindow(QWidget):
    def __init__(self, arduino, main_window):
        super().__init__()
        self.setWindowTitle('Funciones')
        self.arduino = arduino
        self.main_window = main_window
        self.sistema_encendido = False
        self.toggle = True

        # Configurar el diseño principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Espaciador superior para empujar elementos hacia abajo
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Slider para regular brillo
        self.horizontalSlider = QSlider(Qt.Horizontal)
        self.horizontalSlider.setRange(0, 255)
        self.horizontalSlider.setValue(255)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider.valueChanged.connect(self.regular_brillo)
        main_layout.addWidget(self.horizontalSlider)

        # Diseño horizontal para botones de encendido y apagado
        power_buttons_layout = QHBoxLayout()
        self.pushButton_4 = self.crear_boton('Encender Sistema', self.enviar_senal_b)
        self.pushButton_5 = self.crear_boton('Apagar Sistema', self.enviar_senal_a)
        power_buttons_layout.addWidget(self.pushButton_4)
        power_buttons_layout.addWidget(self.pushButton_5)
        main_layout.addLayout(power_buttons_layout)

        # Botón para volver al menú principal
        self.boton_volver = self.crear_boton('Volver a Principal', self.volver_a_principal)
        main_layout.addWidget(self.boton_volver)

        self.setLayout(main_layout)

    def crear_boton(self, texto, callback):
        """Crea un botón estándar."""
        boton = QPushButton(texto)
        boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        boton.setFixedHeight(50)
        boton.clicked.connect(callback)
        return boton

    def leer_datos_arduino(self):
        """Lee datos del Arduino."""
        if self.arduino.in_waiting > 0:
            datos = self.arduino.readline().decode('utf-8').strip()
            print(f'Datos recibidos del Arduino: {datos}')

    def enviar_senal_a(self):
        """Envía señal 'A' al Arduino."""
        self.arduino.write(b'A')
        self.toggle = False

    def enviar_senal_b(self):
        """Envía señal 'B' al Arduino."""
        self.arduino.write(b'B')
        self.toggle = True

    def regular_brillo(self):
        """Regula el brillo según el slider."""
        brillo = self.horizontalSlider.value()
        self.arduino.write(f'{brillo}'.encode())
        print(f'Brillo ajustado a: {brillo}')

    def volver_a_principal(self):
        from window1 import MainWindow  # Importar aquí para evitar la importación circular
        self.ventana_principal = MainWindow()  # Crear la ventana principal
        self.ventana_principal.show()  # Mostrar la ventana principal
        self.close()  # Cerrar la ventana secundaria
