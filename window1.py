import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
import serial
from window2 import FuncionesWindow
from window3 import EstadisticasWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto Final")
        self.arduino = self.configurar_arduino()

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

        layout_principal.addLayout(layout_botones)

        # Configurar como widget central
        central_widget = QWidget()
        central_widget.setLayout(layout_principal)
        self.setCentralWidget(central_widget)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
