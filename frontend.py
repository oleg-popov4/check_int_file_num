from PyQt5 import QtWidgets
import Gui_file


class StartWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_fenster = Gui_file.Ui_start_window()
        self.ui_fenster.setupUi(self)
        # Speichere alle Elemente als Liste
        self.label_spin_list = [self.ui_fenster.label_links, self.ui_fenster.label_rechts, self.ui_fenster.rechts_int,
                                self.ui_fenster.links_int]
        self.button_list = [self.ui_fenster.Button_directory, self.ui_fenster.Button_symbol, self.ui_fenster.Button_cut,
                            self.ui_fenster.Button_start, self.ui_fenster.Button_clear, self.ui_fenster.Button_undo,
                            self.ui_fenster.Button_save_to_file]
        self.qlabel_list = [self.ui_fenster.text_for_Box_choice, self.ui_fenster.text_for_line_symbol,
                            self.ui_fenster.text_line_example]
        self.qline_text_list = [self.ui_fenster.line_directory, self.ui_fenster.line_verify,
                                self.ui_fenster.line_symbol,
                                self.ui_fenster.line_example, self.ui_fenster.text_results]

        self.set_box_choice()  # Definiere: Was wollen Sie untersuchen
        self.set_gui_interaction()

    def test(self):
        self.setStyleSheet('background-color: ')
        self.update()

    def set_theme(self, theme):
        # lbl1 = QLabel('Привет! Что нового?', self)
        #         lbl1.setAlignment(Qt.AlignCenter)                      #  (Qt.AlignVCenter)

        def set_style(elem_list: list, style: str) -> None:
            for elem in elem_list:
                elem.setStyleSheet(style)
        #end set_style
        if (theme == 'dark'):
            start_window_theme = 'background-color: #3D3D3D;'
            label_spin_theme = 'background-color: #404040; color: white; border: 2px solid #A4004D;'
            qlabel_theme = 'background-color: #404040; color: white;'
            qline_text_theme = 'selection-background-color: #b80000; color: rgb(255, 255, 255); ' \
                              'border: 2px solid #A4004D;'
            button_theme = 'QPushButton{border: 2px solid #A4004D; background-color: #404040; color: white;}' \
                          'QPushButton:hover{border: 2px solid #A4004D; background-color: #444444; color: white;}'

            # selection-color: rgb(255, 88, 0); Farbe beim Textauswahl
            # color: rgb(255, 255, 255); Farbe des Textes
            # selection-background-color: rgb(255, 255, 255); Balken beim auswahl des Textes
            # selection-color: rgb(85, 170, 255); Makierung des Schriftes beim auswahl
            box_choice_theme = 'border: 2px solid #A4004D; color: rgb(255, 255, 255); ' \
                              'selection-background-color: #b80000; '
        elif (theme == 'white'):
            start_window_theme = 'background-color: ;'
            label_spin_theme = 'background-color: ; color: ; border: ;'
            qlabel_theme = 'background-color: ; color: ;'
            qline_text_theme = 'selection-background-color: ; color: ; border: ;'
            button_theme = 'QPushButton{border: ; background-color: ; color: ;}' \
                           'QPushButton:hover{border: ; background-color: ; color: ;}'
            box_choice_theme = 'border: ; color: ; selection-background-color:  ; selection-color:  ;'
        #end if

        self.setStyleSheet(start_window_theme)
        set_style(self.label_spin_list,label_spin_theme)
        set_style(self.qlabel_list, qlabel_theme)
        set_style(self.qline_text_list, qline_text_theme)
        set_style(self.button_list, button_theme)
        self.ui_fenster.Box_choice.setStyleSheet(box_choice_theme)
        self.update()
        # self.ui_fenster.Box_choice.setStyleSheet('''
        # border: 2px solid #A4004D;
        # color: rgb(255, 255, 255);
        # selection-background-color: #b80000;
        # ''')
        # selection-color: rgb(255, 88, 0); Farbe beim Textauswahl
        # color: rgb(255, 255, 255); Farbe des Textes
        # selection-background-color: rgb(255, 255, 255); Balken beim auswahl des Textes
        # selection-color: rgb(85, 170, 255); Makierung des Schriftes beim auswahl
        # self.ui_fenster.Box_choice

    # end dark_mode

    def set_box_choice(self) -> None:
        # Was wollen Sie untersuchen? Box_choice
        self.ui_fenster.Box_choice.addItem('Dateien')
        self.ui_fenster.Box_choice.addItem('Ordner')
        self.ui_fenster.Box_choice.addItem('Beides')

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
# end class Window
