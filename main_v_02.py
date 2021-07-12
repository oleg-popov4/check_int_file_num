import sys
from PyQt5 import QtWidgets
from frontend import StartWindow
from backend import Backend

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')  # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    window = StartWindow()
    backend = Backend(window)  # Verbindung vom frontend und backend
    window.show()
    # window.setStyleSheet('background-color: #3D3D3D;')
    # window.test()
    # window.setStyleSheet('background-color: #ffffff;')
    # window.show()
    sys.exit(app.exec_())