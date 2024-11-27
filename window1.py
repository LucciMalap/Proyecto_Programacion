from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
import serial
from PySide2.QtGui import QPixmap
from window2 import FuncionesWindow
from window3 import EstadisticasWindow
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto Final")
        self.arduino = self.configurar_arduino()
        self.setStyleSheet("MainWindow {background-color: rgb(110, 194, 234);}")

        # Ventanas secundarias
        self.funciones_window = FuncionesWindow(self.arduino, self)
        self.estadisticas_window = EstadisticasWindow(self.arduino, self)

        # Configuración de la interfaz principal
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario principal."""
        layout_principal = QVBoxLayout()

        # Espaciador
        layout_principal.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones principales
        layout_botones = QHBoxLayout()
        botones = [
            ('Estadísticas', self.mostrar_estadisticas),
            ('Inicio', self.mostrar_funciones),
        ]

        for texto, callback in botones:
            boton = self.crear_boton(texto, callback, height=75)
            layout_botones.addWidget(boton)

        # Configurar como widget central
        central_widget = QWidget()
        central_widget.setLayout(layout_principal)
        self.setCentralWidget(central_widget)
                
        self.label_imagen = QLabel()
        pixmap = QPixmap("msfarma.jpeg")  # Cambia esto por la ruta de tu imagen
        self.label_imagen.setPixmap(pixmap)
        self.label_imagen.setAlignment(Qt.AlignCenter)  # Centra la imagen
        layout_principal.addWidget(self.label_imagen)

        layout_principal.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout_principal.addLayout(layout_botones)

    def configurar_arduino(self):
        """Intenta configurar la conexión con el Arduino."""
        try:
            arduino = serial.Serial('COM7', 9600)
            print('Conexión establecida con el Arduino.')
            return arduino
        except serial.SerialException as e:
            print(f'Error al conectar con el Arduino: {e}')
            return None

    def crear_boton(self, texto, callback, height=40):
        """Crea un botón estándar."""
        boton = QPushButton(texto)
        boton.setFixedHeight(height)
        boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        boton.clicked.connect(callback)
        return boton

    def mostrar_funciones(self):
        """Abre la ventana de Funciones."""
        self.funciones_window.showMaximized()
        self.hide()

    def mostrar_estadisticas(self):
        """Abre la ventana de Estadísticas."""
        self.estadisticas_window.showMaximized()
        self.hide()
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
                    padding: 15px;
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