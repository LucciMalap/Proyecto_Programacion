import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import Slot, QTimer, Qt
import serial
from ui_Proyecto_final import Ui_MainWindow

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

        # Timer para leer datos del Arduino
        self.timer = QTimer(self)
        # self.timer.timeout.connect(self.leer_datos_arduino)
        self.timer.start(1000)

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
            if datos == 'Sistema encendido':
                self.sistema_encendido = True
                self.toggle = True
            elif datos == 'Sistema apagado':
                self.sistema_encendido = False
                self.toggle = False

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
        """Vuelve al menú principal."""
        self.hide()
        self.main_window.show()

class EstadisticasWindow(QWidget):
    def __init__(self, arduino, main_window):
        super().__init__()
        self.setWindowTitle('Estadísticas')
        self.arduino = arduino
        self.main_window = main_window
        self.toggle = False

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario."""
        main_layout = QVBoxLayout(self)

        # Botones principales
        self.menu_button = self.crear_boton('Menú', self.toggle_sidebar)
        self.volver_button = self.crear_boton('Volver', self.volver_a_principal)

        main_layout.addWidget(self.menu_button)

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
            ('Promedio Mensual', self.mostrar_promedio_mensual),
            ('Promedio Diario', self.mostrar_promedio_diario),
        ]

        for texto, callback in botones:
            boton = self.crear_boton(texto, callback, height=50)
            self.menu_layout.addWidget(boton)

        self.menu_widget.setVisible(False)

    def setup_funciones_widget(self):
        """Configura el widget de funciones principal."""
        self.funciones_widget = QWidget()
        self.funciones_widget.setFixedWidth(200)
        self.funciones_layout = QVBoxLayout(self.funciones_widget)

        self.funciones_label = QLabel('Ms Farma', alignment=Qt.AlignCenter)
        self.funciones_layout.addWidget(self.funciones_label)

        self.funciones_widget.setVisible(False)

    def crear_boton(self, texto, callback, height=40):
        """Crea un botón estándar."""
        boton = QPushButton(texto)
        boton.setFixedHeight(height)
        boton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        boton.clicked.connect(callback)
        return boton

    def toggle_sidebar(self):
        """Alterna la visibilidad de los widgets laterales."""
        self.menu_widget.setVisible(not self.menu_widget.isVisible())
        self.funciones_widget.setVisible(not self.funciones_widget.isVisible())

    def mostrar_contador(self):
        """Muestra el último dato leído del Arduino."""
        contador = None
        if self.arduino:
            while self.arduino.in_waiting > 0:
                contador = self.arduino.readline().decode('utf-8').strip()

        texto = contador if contador else 'No hay datos disponibles'
        print(f'Datos recibidos del Arduino: {texto}')
        self.funciones_label.setText(texto)

    def mostrar_matriz(self):
        """Muestra una matriz de ejemplo."""
        matriz = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6],
        ]
        texto_matriz = "\n".join(["\t".join(map(str, fila)) for fila in matriz])
        self.funciones_label.setText(texto_matriz)

    def mostrar_la_mejor_semana(self):
        print('Mostrar la mejor semana')

    def mostrar_la_peor_semana(self):
        print('Mostrar la peor semana')

    def mostrar_promedio_mensual(self):
        print('Mostrar promedio mensual')

    def mostrar_promedio_diario(self):
        print('Mostrar promedio diario')

    def volver_a_principal(self):
        self.hide()
        self.main_window.show()

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
            arduino = serial.Serial('COM5', 9600)
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
