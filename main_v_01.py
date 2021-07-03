from PyQt5 import QtWidgets, QtGui  # , QtCore
import sys
from PyQt5.QtWidgets import QFileDialog
import Gui_file
import re
import os


class Backend:  # (QtCore.QThread):
    # Signale
    # s1 = QtCore.pyqtSignal(object)

    @staticmethod
    def save_string_to_file(file_name, string):
        """
        Funktion ergänzt ein File namens file_name mit string Zeichen.
        """
        write_method = 'at' if os.path.isfile(file_name) else 'tw'
        speichere_text = string if (write_method == 'tw') else '\n' + string
        with open(file_name, write_method, encoding='utf-8') as file:
            file.write(speichere_text)
        # end with

    # end save_string_to_file

    def __init__(self, window, parent=None):
        # QtCore.QThread.__init__(self, parent)
        # Zeiger auf dem Gui-fenster
        self.main_window = window
        self.main_gui = self.main_window.ui_fenster
        self.directory = ''  # Untersuchtes verzeichnis
        self.choice = ''  # Auswahl vom Benutzer ( Dateien, Files, Dateien und Files )
        self.all_date = []  # Hier werden alle Dateien und Files aus dem verzeichnis (directory) gespeichert
        self.all_files = []  # Hier werden alle Files aus dem verzeichnis (directory) gespeichert
        self.all_folder = []  # Hier werden alle Dateien aus dem verzeichnis (directory) gespeichert
        self.verify_list = []  # Diese ( modifizierbare ) liste wird überprüft
        self.max_str_len = 0  # Maximale anzahl str in Dateien und Files namen
        self.search_sym = ''  # Text vom line_symbol wird hier gespeichert
        self.bsp_sym = ''  # Wird bei line_verify und line_example angezeigt
        self.text_result = ''  # Wird bei text_results angezeigt. Verwendung: undo-funktion
        self.pattern = re.compile('([0-9]+.{1}[0-9]+)|([0-9]+)')

    # end __init__

    # ----------------------------------Funktionen------------------
    # ---------------------------------------------------------------

    def reset_variable(self):
        self.choice = self.main_gui.Box_choice.currentText()
        self.all_date = []  # Hier werden alle Dateien und Files aus dem verzeichnis (directory) gespeichert
        self.all_files = []  # Hier werden alle Files aus dem verzeichnis (directory) gespeichert
        self.all_folder = []  # Hier werden alle Dateien aus dem verzeichnis (directory) gespeichert
        self.verify_list = []  # Diese ( modifizierbare ) liste wird überprüft
        self.search_sym = ''  # Text vom line_symbol wird hier gespeichert
        self.bsp_sym = ''  # Wird bei line_verify und line_example angezeigt

    # end initialize_variable

    def info(self):
        print('directory', self.directory)
        print('choice', self.choice)
        print('all_date', self.all_date)
        print('all_files', self.all_files)
        print('all_folder', self.all_folder)
        print('verify_list', self.verify_list)
        print('max_str_len', self.max_str_len)
        print('search_sym', self.search_sym)
        print('bsp_sym', self.bsp_sym)
        print('text_result', self.text_result)
        print('pattern', self.pattern)

    # end info

    def update_qline_gui(self):
        """
        update line_verify mit bsp_sym, line_symbol mit search_sym, line_example mit search_sym
        """
        # self.main_gui.line_directory.setText(self.directory)
        self.main_gui.line_verify.setText(self.bsp_sym)
        self.main_gui.line_symbol.setText(self.search_sym)
        self.main_gui.line_example.setText(self.search_sym)

    # end update_gui

    # -------------------------clicked functions--------------------------------
    # --------------------------------------------------------------------------

    def set_box_choice(self):
        """
        1 - Aktualisiert Variable choice
        2 - Falls gültiges verzeichnis ist gegeben, aktualisiere Beispiel
        """
        # self.choice = self.main_gui.Box_choice.currentText() # wird auch bei self.set_calculate_example() abgefragt
        if (os.path.isdir(self.directory)):
            self.set_calculate_example()
        print('set_box_choice')
        self.info()

    # end set_box_choice

    def find_data(self):
        """
        Suche und speichere Dateien, Files, Dateien und Files
        Vorsicht variablen all_date, all_files, all_folder werden aktualisiert
        """
        self.all_date = os.listdir(path=self.directory) if (os.path.isdir(self.directory)) else []
        all_files = []
        all_folder = []
        for data in self.all_date:
            temp_dir = os.path.join(self.directory, data)
            self.max_str_len = max(self.max_str_len, len(data))
            if (os.path.isfile(temp_dir)): all_files.append(data)
            if (os.path.isdir(temp_dir)): all_folder.append(data)
        # end for
        self.all_files = all_files
        self.all_folder = all_folder

    # end find_data

    def set_data(self):
        """
        Setze variable verify_list
        """
        if (self.choice == 'Dateien'):
            self.verify_list = self.all_files
            self.bsp_sym = 'Keine Dateien gefunden' if self.all_files == [] else self.all_files[0]
        elif (self.choice == 'Ordner'):
            self.verify_list = self.all_folder
            self.bsp_sym = 'Keine Ordner gefunden' if self.all_folder == [] else self.all_folder[0]
        elif (self.choice == 'Beides'):
            self.verify_list = self.all_date
            self.bsp_sym = 'Verzeichniss ist leer' if self.all_date == [] else self.all_date[0]
        # end if

    # end set_data

    def set_calculate_example(self):
        """
        Richtiges verzeichnis muss gegeben werden
        1 - Berechne Beispiel
        2 - update line_verify, line_example
        3 - lösche line_symbol
        """
        # 1 - Berechne Beispiel
        self.choice = self.main_gui.Box_choice.currentText()
        # verzeichnis hat sich geändert? brauche abfrage
        if True:
            self.find_data()
        # end if
        self.set_data()
        # 2 - update line_verify, line_example, 3 - lösche line_symbol
        self.search_sym = ''
        self.update_qline_gui()

    # end set_example

    def set_directory(self, dir: str):
        """
        set_directory(self, dir=None)
        Diese Funktion hat zwei arbeitsweisen
        1. Abfragen verzeichnis vom Benutzer
        2. Eingetippte (dir) verzeichnis vom Benutzer abspeichern
        """
        verzeichnis = QFileDialog.getExistingDirectory() if (dir == '') else dir
        if (os.path.isdir(verzeichnis)):
            # Gültiges verzeichnis ist gegeben
            # 1 - abspeichern verzeichnis, Dateien, Files, Dateien und Files in variablen,
            # 2 - Berechne Beispiel
            self.directory = verzeichnis
            self.main_gui.line_directory.setText(str(verzeichnis))  # Fur Punkt 1
            self.set_calculate_example()
        else:
            self.reset_variable()
            self.bsp_sym = 'Kein gultiges verzeichniss ausgewahlt'
            self.update_qline_gui()
        # end if

    # end set_directory

    def clicked_button_anwenden(self):
        """
        Gegeben: verzeichnis muss richtig eingegeben werden
        1 - verify_list muss Symbol (line_symbol) erhalten
        2 - anpasse verify_list an neuen symbol
        3 - bei änderung von box_choice muss neu berechnet werden
        """
        # ToDo teste ob gebraucht wird: self.set_data()
        # Gegeben: verzeichnis muss richtig eingegeben werden
        if (os.path.isdir(self.directory)):
            self.search_sym = self.main_gui.line_symbol.text()
            neu_list = []
            if (self.search_sym != ''):
                for el in self.verify_list:
                    if (self.search_sym in el):
                        neu_list.append(el)
                # end for
                self.verify_list = neu_list
            else:
                neu_list = self.verify_list
            # end if
            self.bsp_sym = neu_list[0] if len(neu_list) > 0 else ''
            if (len(self.verify_list) != 0):
                self.main_gui.line_verify.setText(self.bsp_sym)
                self.main_gui.line_example.setText(self.bsp_sym)
            else:
                self.main_gui.line_verify.setText('Keine Datei gefunden')

    # end clicked_button_anwenden

    def cut_example(self):
        """
        Anpassung vom line_example an int werte
        1 - Text kann in line_example.text()
        2 - oder mit int Zahlen (links_int, rechts_int) angegeben werden
        """
        # 1 - Text kann in line_example.text() angegeben werden
        example = ''
        if (self.bsp_sym != ''):
            # uberprufe int werte und exapmle
            links_int = self.main_gui.links_int.value()
            rechts_int = self.main_gui.rechts_int.value()
            example = self.main_gui.line_example.text()
            if (example == ''):  # Anwende int werte
                if (rechts_int == 0):
                    example = self.bsp_sym[links_int:]
                else:
                    example = self.bsp_sym[links_int:-rechts_int]
            else:
                match = re.search(example, self.bsp_sym)
                if (match != None and len(match.span()) == 2):
                    neu_links = match.span()[0]
                    neu_recht = match.span()[1]
                    self.main_gui.links_int.setValue(neu_links)
                    self.main_gui.rechts_int.setValue(len(self.bsp_sym) - neu_recht)
                    example = self.bsp_sym[neu_links:neu_recht]
                else:
                    example = 'Muster nicht gefunden'
            # end if
            self.main_gui.line_example.setText(example)

    # end cut_example

    def change_int_value(self):
        """
        Anpassung vom line_example an int werte
        1 - Text kann in line_example.text()
        2 - oder mit int Zahlen (links_int, rechts_int) angegeben werden
        """
        # 2 - oder mit int Zahlen (links_int, rechts_int) angegeben werden
        example_text = self.bsp_sym # ui.line_example.text()
        links_int = self.main_gui.links_int.value()
        rechts_int = self.main_gui.rechts_int.value()
        neu_text = example_text[links_int:-rechts_int] if rechts_int != 0 else example_text[links_int:]
        self.main_gui.line_example.setText(neu_text)

    # end change_int_value

    def start_computing(self):
        ausgabe = lambda test: ui.text_results.append(str(test))
        ausgabe_text = ''
        # uberprufe ob programm Starten kann
        if (VERZEICHNISS == ''): ausgabe_text = ausgabe_text + str('Kein Verzeichniss ausgewahlt?') + '\n'
        if (len(VERIFY_LIST) == 0):
            ausgabe_text = ausgabe_text + str('Nichts zu tun? VERIFY_LIST ist leer') + '\n'
        else:
            # print('Wir betrachten folgende Liste')
            # print_list_spalten(VERIFY_LIST,1)#100 ist di grenze
            # Jetzt werden alle Daten mit nummern ausgewertet
            min_num = 1000
            max_num = 0
            zahlen_list_int = []
            zahlen_list_rest = []
            list_ohne_num = []
            links_int = ui.links_int.value()
            rechts_int = ui.rechts_int.value()
            for el in VERIFY_LIST:
                text = el[links_int:-rechts_int] if rechts_int != 0 else el[links_int:]
                match = PATTERN.search(text)
                if (match != None):
                    # Uberprufe nach int oder float
                    try:
                        zahl = int(match[0])
                        min_num = min(min_num, zahl)
                        max_num = max(max_num, zahl)
                        zahlen_list_int.append(zahl)
                    except ValueError:
                        zahlen_list_rest.append(el)
                else:
                    list_ohne_num.append(el)
            # end for
            # fehlende Nummer
            fehlende_num = [zahl for zahl in range(min_num, max_num + 1) if zahl not in zahlen_list_int]
            ausgabe_text = ausgabe_text + str(VERZEICHNISS) + '\n'
            # ausgabe('VERIFY_LIST hat ' + str(len(VERIFY_LIST)) + ' Elemente' )
            if (len(zahlen_list_rest) != 0):
                ausgabe_text = ausgabe_text + str(
                    'Es gibt ' + str(len(zahlen_list_rest)) + ' Elemente die nicht ganzahlig sind\n')
                ausgabe_text = ausgabe_text + str(zahlen_list_rest) + '\n'
            if (len(list_ohne_num) != 0):
                ausgabe_text = ausgabe_text + str('Es gibt ' + str(len(list_ohne_num)) + ' Elemente ohne nummer\n')
                ausgabe_text = ausgabe_text + str(list_ohne_num) + '\n'
            ausgabe_text = ausgabe_text + str('Maximum int ist {0}, minimale int ist {1}\n'.format(max_num, min_num))
            ausgabe_text = ausgabe_text + str('Insgesamt gibt es {0} int Daten\n'.format(len(zahlen_list_int)))
            if (len(fehlende_num) != 0):
                ausgabe_text = ausgabe_text + str('Es fehlen folgende int Nummer\n')
                ausgabe_str = ''
                for el in fehlende_num:
                    ausgabe_str = ausgabe_str + str(el) + ', '
                    # ausgabe(el)
                # dn for
                ausgabe_text = ausgabe_text + str(ausgabe_str[:-2]) + '\n'
                # print_list_spalten(fehlende_num)
        # end if
        ausgabe(ausgabe_text)

    # end start_computing

    def clear_text_results(self):
        self.text_result = self.main_gui.text_results.toPlainText()
        self.main_gui.text_results.clear()

    # end clear_text_results

    def undo_text_results(self):
        aktuelle_text = self.main_gui.text_results.toPlainText()
        if (aktuelle_text == ''):
            self.main_gui.text_results.setText(self.text_result)
        else:
            self.main_gui.text_results.undo()
        # end if

    # end undo_text_results

    def save_to_file(self):
        text = self.main_gui.text_results.toPlainText()
        if (text != ''):
            file_name = QFileDialog.getSaveFileName()
            file_name = file_name[0]
            file_name = file_name if os.path.isfile(file_name) else file_name + '.txt'
            self.save_string_to_file(file_name, text)

    # end save_to_file

    # -------------------------clicked functions end----------------------------
    # --------------------------------------------------------------------------

# end class Backend


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_fenster = Gui_file.Ui_Form()
        self.ui_fenster.setupUi(self)
        self.backend = Backend(self)  # Verbindung vom frontend und backend
        self.set_box_choice()  # Definiere: Was wollen Sie untersuchen
        self.set_gui_interaction()
        self.set_reaction_to_user()  # Reaktionen auf Benutzer aktivität

    def set_box_choice(self) -> None:
        # Was wollen Sie untersuchen? Box_choice
        self.ui_fenster.Box_choice.addItem('Dateien')
        self.ui_fenster.Box_choice.addItem('Ordner')
        self.ui_fenster.Box_choice.addItem('Beides')
        # self.ui_fenster.Box_choice.setStyleSheet('''
        # border: 2px solid #A4004D;
        # color: rgb(255, 255, 255);
        # selection-background-color: #b80000;
        # ''')
        # selection-color: rgb(255, 88, 0); Farbe beim Textauswahl
        # color: rgb(255, 255, 255); Farbe des Textes
        # selection-background-color: rgb(255, 255, 255); Balken beim auswahl des Textes
        # selection-color: rgb(85, 170, 255); Makierung des Schriftes beim auswahl

    # end set_box_choice

    def set_all_button_text(self):
        pass

    # end set_all_button_text

    def set_gui_interaction(self):
        # Ein Beispiel der Datei, die verifiziert wird (line_verify) soll nicht bearbeitet werden
        self.ui_fenster.line_verify.setReadOnly(True)
        # Alle Ergebnisse werden hier und im Terminal angezeigt, text_results
        # self.ui_fenster.text_results.setReadOnly(True)
        # self.ui_fenster.text_results.setWordWrapMode(QtGui.QTextOption.NoWrap)

    # end set_gui_interaction

    def set_reaction_to_user(self):
        # Box_chois
        self.ui_fenster.Box_choice.currentTextChanged.connect(self.backend.set_box_choice)
        # Button_directory
        self.ui_fenster.Button_directory.clicked.connect(lambda: self.backend.set_directory(dir=''))
        # Verzeichnis eintippen in line_directory
        self.ui_fenster.line_directory.textEdited.connect \
            (lambda: self.backend.set_directory(dir=self.ui_fenster.line_directory.text()))
        # Button_symbol .zip Anwenden
        self.ui_fenster.Button_symbol.clicked.connect(self.backend.clicked_button_anwenden)
        # Button_cut Abschneiden
        self.ui_fenster.Button_cut.clicked.connect(self.backend.cut_example)
        # links_int rechts_int Ziffer eingabe
        self.ui_fenster.links_int.valueChanged.connect(self.backend.change_int_value)
        self.ui_fenster.rechts_int.valueChanged.connect(self.backend.change_int_value)
        # Button Start, Clear, Undo, Save to file
        self.ui_fenster.Button_start.clicked.connect(self.backend.start_computing)
        self.ui_fenster.Button_clear.clicked.connect(self.backend.clear_text_results)
        self.ui_fenster.Button_undo.clicked.connect(self.backend.undo_text_results)
        self.ui_fenster.Button_save_to_file.clicked.connect(self.backend.save_to_file)
    # end set_button_functions


# end class Window


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')  # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    window = Window()
    window.show()
    # window.setStyleSheet('background-color: #ffffff;')
    # window.show()
    sys.exit(app.exec_())
