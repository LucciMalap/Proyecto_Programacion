import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel
from PySide2.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear la matriz 3x3
        matriz = [
            [4, 9, 2],
            [1, 0, 0],
            [3, 5, 7]
        ]

        # Convertir la matriz a un formato de texto para mostrar en QLabel
        matriz_texto = "\n".join(["\t".join(map(str, fila)) for fila in matriz])

        # Crear un QLabel para mostrar la matriz
        self.label = QLabel(matriz_texto, self)

        # Establecer el tamaño de la ventana
        self.setWindowTitle("Matriz 3x3")
        self.setGeometry(100, 100, 300, 200)

        # Ajustar el tamaño del QLabel al contenido
        self.label.setAlignment(Qt.AlignCenter)

        # Configurar el QLabel en el centro de la ventana
        self.setCentralWidget(self.label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
