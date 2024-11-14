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

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 10)
        main_layout.setSpacing(10)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        self.horizontalSlider = QSlider(Qt.Horizontal)
        self.horizontalSlider.setRange(0,255)
        self.horizontalSlider.setValue(255)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider.valueChanged.connect(self.regular_brillo)
        
        self.pushButton_4 = QPushButton('Encender Sistema')
        self.pushButton_4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pushButton_4.setFixedHeight(50)
        self.pushButton_4.clicked.connect(self.enviar_senal_b)

        self.pushButton_5 = QPushButton('Apagar Sistema')
        self.pushButton_5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pushButton_5.setFixedHeight(50)
        self.pushButton_5.clicked.connect(self.enviar_senal_a)

        button_layout.addWidget(self.pushButton_4)
        button_layout.addWidget(self.pushButton_5)

        main_layout.addWidget(self.horizontalSlider)
        main_layout.addLayout(button_layout)

        self.boton_volver = QPushButton('Volver a Principal')
        self.boton_volver.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.boton_volver.setFixedHeight(50)
        self.boton_volver.clicked.connect(self.volver_a_principal)

        main_layout.addWidget(self.boton_volver)

        self.setLayout(main_layout)
        
        self.timer = QTimer(self)
        #self.timer.timeout.connect(self.leer_datos_arduino)
        self.timer.start(1000) 

        
    def leer_datos_arduino(self):
        if self.arduino.in_waiting > 0:
            datos = self.arduino.readline().decode('utf-8').strip()
            print(f'Datos recibidos del Arduino {datos}')

            if datos == 'Sistema encendido':
                self.sistema_encendido = True
                self.toggle = True
            elif datos == 'Sistema apagado':
                self.sistema_encendido = False
                self.toggle = False

    def enviar_senal_a(self):
        self.arduino.write(b'A')
        self.toggle = False
        
    def enviar_senal_b(self):
        self.arduino.write(b'B')
        self.toggle = True
    
    def regular_brillo(self):
        brillo = self.horizontalSlider.value()
        self.arduino.write(f'{brillo}'.encode)
        print(brillo)
        
    def volver_a_principal(self):
        self.hide()
        self.main_window.show()

class EstadisticasWindow(QWidget):
    def __init__(self, arduino, main_window):
        super().__init__()
        self.setWindowTitle('Estadísticas')
        self.arduino = arduino
        self.main_window = main_window
        self.toggle = 0

        main_layout = QVBoxLayout(self)
        
        self.menu_button = QPushButton('Menú')
        self.menu_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.menu_button.setFixedHeight(40)
        self.menu_button.clicked.connect(self.toggle_sidebar)
        
        self.volver_button = QPushButton('Volver')
        self.volver_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.volver_button.setFixedHeight(40)
        self.volver_button.clicked.connect(self.volver_a_principal)

        main_layout.addWidget(self.menu_button)
        
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(self.spacer)

        self.horizontal_layout = QHBoxLayout()

        self.menu_widget = QWidget()
        self.menu_widget.setFixedWidth(200)
        self.menu_layout = QVBoxLayout(self.menu_widget)

        self.contador_button = QPushButton('Contador')
        self.contador_button.clicked.connect(self.mostrar_contador)
        
        self.matriz_button = QPushButton('Matriz')
        self.matriz_button.clicked.connect(self.mostrar_matriz)
        
        self.la_mejor_semana_button = QPushButton('La Mejor Semana')
        self.la_mejor_semana_button.clicked.connect(self.mostrar_la_mejor_semana)
        
        self.la_peor_semana_button = QPushButton('La Peor Semana')
        self.la_peor_semana_button.clicked.connect(self.mostrar_la_peor_semana)
        
        self.promedio_mensual_button = QPushButton('Promedio Mensual')
        self.promedio_mensual_button.clicked.connect(self.mostrar_promedio_mensual)
        
        self.promedio_diario_button = QPushButton('Promedio Diario')
        self.promedio_diario_button.clicked.connect(self.mostrar_promedio_diario)

        # Definir una altura fija y expandir para ocupar el ancho completo
        for button in [self.contador_button, self.matriz_button, self.la_mejor_semana_button, 
                       self.la_peor_semana_button, self.promedio_mensual_button, self.promedio_diario_button]:
            button.setFixedHeight(50)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            self.menu_layout.addWidget(button)

        self.menu_widget.setVisible(False)
        
        self.horizontal_layout.addWidget(self.menu_widget)
        
        self.funciones_widget = QWidget()
        self.funciones_widget.setFixedWidth(200)
        self.funciones_layout = QVBoxLayout(self.funciones_widget)
        
        self.funciones_label = QLabel('Contenido Adicional')
        self.funciones_layout.addWidget(self.funciones_label)
        
        self.horizontal_layout.addWidget(self.funciones_widget)
        
        main_layout.addLayout(self.horizontal_layout)

        
        self.funciones_widget.setVisible(False)
        
        main_layout.addWidget(self.volver_button)

    def toggle_sidebar(self):
        current_visible = self.menu_widget.isVisible()
        self.menu_widget.setVisible(not current_visible)
        current_visible2 = self.funciones_widget.isVisible()
        self.funciones_widget.setVisible(not current_visible2)
        layout = self.layout()
        self.toggle = 1
        if self.toggle == 1:
            layout.removeItem(self.spacer)
        elif self.toggle == 2:
            layout.removeItem(self.volver_button)
            layout.addItem(self.spacer)
            layout.addItem(self.volver_button)
            self.toggle = 0

    def mostrar_contador(self):
        ultima_linea = None
        while self.arduino.in_waiting > 0:
          ultima_linea = self.arduino.readline().decode('utf-8').strip()
          contador = ultima_linea

        if ultima_linea:
            print(f'Datos recibidos del Arduino {ultima_linea}')
            self.funciones_label.setText(ultima_linea)
        else:
            print(f'Datos recibidos del Arduino {contador}')
            self.funciones_label.setText(contador)

    def mostrar_matriz(self):
        print('Mostrar matriz')

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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        layout_botones = QVBoxLayout()

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_botones.addItem(spacer)

        self.pushButton_2 = QPushButton('Estadisticas')
        self.pushButton_2.setFixedHeight(75)
        self.pushButton_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pushButton_2.clicked.connect(self.informacion)
        
        self.pushButton_3 = QPushButton('Inicio')
        self.pushButton_3.setFixedHeight(75)
        self.pushButton_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pushButton_3.clicked.connect(self.inicio)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.pushButton_2)
        button_layout.addWidget(self.pushButton_3)

        layout_botones.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout_botones)
        self.setCentralWidget(central_widget)

        try:
            self.arduino = serial.Serial('COM5', 9600)      #Establece el puerto del Arduino
            print('Conexión establecida con el Arduino.')
        except serial.SerialException as e:
            print(f'No se pudo conectar al Arduino {e}')
            self.arduino = None

        self.funciones_window = FuncionesWindow(self.arduino, self)
        self.estadisticas_window = EstadisticasWindow(self.arduino, self)

    @Slot()
    def inicio(self):
        self.funciones_window.showMaximized()
        self.hide()

    def informacion(self):
        self.estadisticas_window.showMaximized()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
