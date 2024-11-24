import sys
from PySide2.QtWidgets import QApplication
from window1 import MainWindow  # Importamos la ventana principal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = MainWindow()  # Creamos la ventana principal
    ventana_principal.showMaximized()  # Mostramos la ventana principal
    sys.exit(app.exec_())  # Ejecutamos el bucle principal
