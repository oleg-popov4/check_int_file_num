from PyQt5 import QtWidgets
import sys

import Gui_file


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_fenster = Gui_file.Ui_Form()
        self.ui_fenster.setupUi(self)
        self.set_box_choice()

    def set_box_choice(self) -> None:
        # Was wollen Sie untersuchen? Box_choice
        self.ui_fenster.Box_choice.addItem('Dateien')
        self.ui_fenster.Box_choice.addItem('Ordner')
        self.ui_fenster.Box_choice.addItem('Beides')
        self.ui_fenster.Box_choice.setStyleSheet('''
        border: 2px solid #A4004D; 
        color: rgb(255, 255, 255);
        selection-background-color: #b80000;
        ''')
        # selection-color: rgb(255, 88, 0); Farbe beim Textauswahl
        # color: rgb(255, 255, 255); Farbe des Textes
        # selection-background-color: rgb(255, 255, 255); Balken beim auswahl des Textes
        # selection-color: rgb(85, 170, 255); Makierung des Schriftes beim auswahl

    # end set_box_choice

    def clear_line_directory(self):
        pass
    # end clear_line_directory


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')  # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    window = Window()
    window.show()
    sys.exit(app.exec_())
