from PySide2.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QLabel, QVBoxLayout, QSlider, QHBoxLayout, QComboBox, QPushButton
from PySide2.QtCore import  Qt
from PySide2.QtGui import QPixmap

class FuncionesWindow(QWidget):
    def __init__(self, arduino, main_window):
        super().__init__()
        self.setWindowTitle('Funciones')
        self.arduino = arduino
        self.main_window = main_window
        self.sistema_encendido = False
        self.toggle = True
        self.setStyleSheet("QWidget {background-color: rgb(110, 194, 234);}")

        # Configurar el diseño principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # Slider para regular brillo
        self.horizontalSlider = QSlider(Qt.Horizontal)
        combo_layout = QHBoxLayout()
        self.comboBox1 = QComboBox()
        self.comboBox2 = QComboBox()
        
        self.comboBox1.setFixedHeight(40)  # Alto fijo
        self.comboBox2.setFixedHeight(40)  # Alto fijo
        
        niveles1 = ["Buzzer apagado", "Buzzer bajo", "Buzzer medio", "Buzzer alto"]
        self.comboBox1.addItems(niveles1)
        combo_layout.addWidget(self.comboBox1)
        main_layout.addLayout(combo_layout)
        
        self.comboBox1.currentIndexChanged.connect(lambda: self.enviar_señal_combobox(self.comboBox1, 1))

        
        

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
   
    def enviar_señal_combobox(self, combobox, combobox_id):
        """Envía la señal seleccionada en el combobox al Arduino."""
        if self.arduino:
            try:
                valor = combobox.currentText()
                print(f"Valor seleccionado: {valor}")
                if valor == 'Buzzer apagado':
                    self.arduino.write(b'C')  # Comando para apagar el buzzer
                elif valor == 'Buzzer bajo':
                    self.arduino.write(b'D')  # Comando para buzzer en nivel bajo
                elif valor == 'Buzzer medio':
                    self.arduino.write(b'E')  # Comando para buzzer en nivel medio
                elif valor == 'Buzzer alto':
                    self.arduino.write(b'F')  # Comando para buzzer en nivel alto
            except Exception as e:
                print(f"Error al enviar al Arduino: {e}")
        else:
            print("Error: Arduino no está conectado.")

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
        self.ventana_principal.showMaximized()  # Mostrar la ventana principal
        self.close()  # Cerrar la ventana secundaria
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
                    border-radius: 10px;  /* Bordes redondeados */
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