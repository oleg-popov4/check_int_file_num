import os
import sys
import re
import sys
import FileUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QFileDialog, QApplication)
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY,PLAIN_COLUMNS,MARKDOWN,ORGMODE

#test = [el for el in range(6) if el > 2 ]
#--------------Globale Variablen-----------
VERZEICHNISS = '' #string
CHOIS = '' #string
ALL_DATA = [] #list
ALL_FILES = [] #list
ALL_FOLDER = [] #list
VERIFY_LIST = []
MAX_STR_LEN = 0 # int
SEARCH_SYM = ''
BSP_SYM = ''
PATTERN = re.compile('([0-9]+.{1}[0-9]+)|([0-9]+)')
#--------------Globale Variablen-----------

def save_string_to_file(file_name,string):
    write_method = 'at' if os.path.isfile(file_name) else 'tw'
    speichere_text = string if (write_method == 'tw') else '\n' + string
    with open(file_name, write_method, encoding='utf-8') as file:
        file.write(speichere_text)
    #end with
#end save_string_to_file

def print_list_spalten(liste: list,spalten=1,vorg_ignore_num_str = 0):
    leerres_elem = ' '
    table = PrettyTable(header=False)
    table.set_style(ORGMODE) #1)DEFAULT 2)PLAIN_COLUMNS  3)MARKDOWN  4)ORGMODE
    print_list = liste[:]
    while ( len(print_list) % spalten != 0 ):
        print_list.append(leerres_elem)
    #end while
    table_temp =[]
    for id,elem in enumerate(print_list):
        if ( elem == leerres_elem ):
            table_temp.extend([leerres_elem,elem])
        else:
            table_temp.extend([str(id)+')',elem])
        #end if
        if ( (id+1)%spalten == 0 ):
            table.add_row(table_temp)
            table_temp = []
    #end for
    print(table)
#end print_list_spalten

def inizialisiere_ui(ui):
    #Was wollen Sie untersuchen? Box_chois
    #ui.Box_chois.setStyleSheet("QComboBox {color: white}")
    ui.Box_chois.addItem('Dateien')
    ui.Box_chois.addItem('Ordner')
    ui.Box_chois.addItem('Beides')
    

    #Wählen Sie ein Ordner aus, line_directory
    #ui.line_directory.setReadOnly(True)
    ui.line_directory.textEdited.connect(lambda: clicked_Button_directory(ui,path = ui.line_directory.text() ))

    #Ein Beispiel der Datei, die verifiziert wird, line_verify
    ui.line_verify.setReadOnly(True)

    #Alle Ergebnisse werden hier und im Terminal angezeigt, text_results
    ui.text_results.setReadOnly(True)
    #ui.text_results.setWordWrapMode(QtGui.QTextOption.NoWrap)
    return ui
#end inizialisiere_ui

def find_set_data():
    global ALL_DATA, ALL_FILES, ALL_FOLDER, VERZEICHNISS, MAX_STR_LEN
    ALL_DATA = os.listdir(path = VERZEICHNISS)
    all_files = []
    all_folder = []
    for data in ALL_DATA:
        path = os.path.join(VERZEICHNISS,data)
        MAX_STR_LEN = max(MAX_STR_LEN,len(data))
        if ( os.path.isfile(path) ): all_files.append(data)
        if ( os.path.isdir(path) ): all_folder.append(data)
    ALL_FILES = all_files
    ALL_FOLDER = all_folder
#end find_set_data

def set_beispiel(ui):
    global VERZEICHNISS, CHOIS, ALL_FILES, ALL_FOLDER, ALL_DATA, VERIFY_LIST, BSP_SYM
    CHOIS = ui.Box_chois.currentText()
    if ( CHOIS == 'Dateien'):
        VERIFY_LIST = ALL_FILES
        if (ALL_FILES == []):
            ui.line_verify.setText('Keine Dateien gefunden')
        else:
            BSP_SYM = ALL_FILES[0]
            ui.line_verify.setText(BSP_SYM)
    elif ( CHOIS == 'Ordner'):
        VERIFY_LIST = ALL_FOLDER
        if (ALL_FOLDER == []):
            ui.line_verify.setText('Keine Ordner gefunden')
        else:
            BSP_SYM = ALL_FOLDER[0]
            ui.line_verify.setText(BSP_SYM)
    elif ( CHOIS == 'Beides'):
        VERIFY_LIST = ALL_DATA
        if (ALL_DATA == []):
            ui.line_verify.setText('Verzeichniss ist leer')
        else:
            BSP_SYM = ALL_DATA[0]
            ui.line_verify.setText(BSP_SYM)
    #end if

#end set_beispiel

def clicked_Button_directory(ui, path = None):
    global VERZEICHNISS, CHOIS, ALL_FILES, ALL_FOLDER, ALL_DATA, BSP_SYM, SEARCH_SYM, VERIFY_LIST
    verzeichniss = QFileDialog.getExistingDirectory() if ( path == None ) else path
    if ( os.path.isdir(verzeichniss) ):
        VERZEICHNISS = verzeichniss
        ui.line_directory.setText(str(verzeichniss))
        #CHOIS = ui.Box_chois.currentText()
        find_set_data()
        #todo setze beliebige Datei als bespiel, line_verify
        set_beispiel(ui)
        clear_placeholder(ui)
    else:
        ui.line_verify.setText('Kein gultiges verzeichniss ausgewahlt')
        VERZEICHNISS = ''
        ALL_FILES = []
        ALL_FOLDER = []
        ALL_DATA = []
        BSP_SYM = ''
        SEARCH_SYM = ''
        VERIFY_LIST = []
    #end if
#end clicked_Button_directory

def clicked_Button_anwenden(ui):
    global VERZEICHNISS, CHOIS, ALL_FILES, ALL_FOLDER, ALL_DATA, VERIFY_LIST, SEARCH_SYM, BSP_SYM
    set_beispiel(ui)
    SEARCH_SYM = ui.line_symbol.text()
    neu_list = []
    if (SEARCH_SYM != ''):
        for el in VERIFY_LIST:
            if ( SEARCH_SYM in el ): neu_list.append(el)
        #end for
        VERIFY_LIST = neu_list
    else:
        neu_list = VERIFY_LIST
    #end if
    BSP_SYM = neu_list[0] if len(neu_list) > 0 else ''
    if ( len(VERIFY_LIST) != 0 ):
        ui.line_verify.setText(BSP_SYM)
        ui.line_example.setText(BSP_SYM)
    else:
        ui.line_verify.setText('Keine Datei gefunden')
#end clicked_Button_anwenden

def clicked_Button_cut(ui):
    global VERZEICHNISS, CHOIS, ALL_DATA, ALL_FILES, ALL_FOLDER, VERIFY_LIST, MAX_STR_LEN, SEARCH_SYM, BSP_SYM
    example = ''
    if ( BSP_SYM != ''):
        #uberprufe int werte und exapmle
        links_int = ui.links_int.value()
        rechts_int = ui.rechts_int.value()
        example = ui.line_example.text()
        if ( example == '' ): #Anwende int werte
            if (rechts_int == 0):
                example = BSP_SYM[links_int:]
            else:
                example = BSP_SYM[links_int:-rechts_int]
        else:
            match = re.search(example,BSP_SYM)
            if ( match != None and len(match.span() ) == 2 ):
                neu_links = match.span()[0]
                neu_recht = match.span()[1]
                ui.links_int.setValue(neu_links)
                ui.rechts_int.setValue(len(BSP_SYM) - neu_recht)
                example = BSP_SYM[neu_links:neu_recht]
            else:
                example = 'Muster nicht gefunden'
        #end if
        ui.line_example.setText(example)
#end clicked_Button_cut

def value_int_changed(ui):
    global VERZEICHNISS, CHOIS, ALL_DATA, ALL_FILES, ALL_FOLDER, VERIFY_LIST, MAX_STR_LEN, SEARCH_SYM, BSP_SYM
    example_text = BSP_SYM # ui.line_example.text()
    links_int = ui.links_int.value()
    rechts_int = ui.rechts_int.value()
    neu_text = example_text[links_int:-rechts_int] if rechts_int !=0 else example_text[links_int:]
    ui.line_example.setText(neu_text)
#end value_int_changed(ui)

def clear_placeholder(ui):
    ui.line_symbol.clear()
    ui.line_example.clear()
    ui.links_int.setValue(0)
    ui.rechts_int.setValue(0)
#end clear_placeholder

def set_box_chois(ui):
    global VERZEICHNISS, CHOIS, ALL_DATA, ALL_FILES, ALL_FOLDER, VERIFY_LIST, MAX_STR_LEN, SEARCH_SYM, BSP_SYM
    #text_in_line_directory = ui.line_directory.text()
    set_beispiel(ui)
    clear_placeholder(ui)
    if ( VERZEICHNISS == ''):
        ui.line_verify.setText('')
#end set_box_chois

def programm_start(ui):
    global VERZEICHNISS, CHOIS, ALL_DATA, ALL_FILES, ALL_FOLDER, VERIFY_LIST, MAX_STR_LEN, SEARCH_SYM, BSP_SYM,PATTERN
    ausgabe = lambda test: ui.text_results.append( str(test) )
    #uberprufe ob programm Starten kann
    if ( VERZEICHNISS == '' ): ausgabe('Kein Verzeichniss ausgewahlt?')
    if ( len(VERIFY_LIST) == 0 ): 
        ausgabe('Nichts zu tun? VERIFY_LIST ist leer')
    else:
        #print('Wir betrachten folgende Liste')
        #print_list_spalten(VERIFY_LIST,1)#100 ist di grenze
        #Jetzt werden alle Daten mit nummern ausgewertet
        min_num = 1000
        max_num = 0
        zahlen_list_int = []
        zahlen_list_rest = []
        list_ohne_num = []
        links_int = ui.links_int.value()
        rechts_int = ui.rechts_int.value()
        for el in VERIFY_LIST:
            text = el[links_int:-rechts_int] if rechts_int !=0 else el[links_int:]
            match = PATTERN.search(text)
            if (match != None):
                #Uberprufe nach int oder float
                try:
                    zahl = int(match[0])
                    min_num = min(min_num,zahl)
                    max_num = max(max_num,zahl)
                    zahlen_list_int.append(zahl)
                except ValueError:
                    zahlen_list_rest.append(el)
            else:
                list_ohne_num.append(el)
        #end for
        #fehlende Nummer
        fehlende_num = [zahl for zahl in range(min_num,max_num+1) if zahl not in zahlen_list_int]
        ausgabe(VERZEICHNISS)
        #ausgabe('VERIFY_LIST hat ' + str(len(VERIFY_LIST)) + ' Elemente' )
        if (len(zahlen_list_rest) != 0):
            ausgabe('Es gibt ' + str(len(zahlen_list_rest)) + ' Elemente die nicht ganzahlig sind')
            ausgabe(zahlen_list_rest)
        if ( len(list_ohne_num) !=0 ):
            ausgabe('Es gibt ' + str(len(list_ohne_num)) + ' Elemente ohne nummer')
            ausgabe(list_ohne_num)
        ausgabe('Maximum int ist {0}, minimale int ist {1}'.format(max_num,min_num))
        ausgabe('Insgesamt gibt es {0} int Daten'.format(len(zahlen_list_int)))
        if (len(fehlende_num) !=0 ): 
            ausgabe('Es fehlen folgende int Nummer')
            ausgabe_str = ''
            for el in fehlende_num:
                ausgabe_str = ausgabe_str + str(el) + ', '
                #ausgabe(el)
            #dn for
            ausgabe(ausgabe_str[:-2])
            #print_list_spalten(fehlende_num)
    #end if
#end programm_start
    
def save_to_file(ui):
    text = ui.text_results.toPlainText()
    if ( text != '' ):
        file_name = QFileDialog.getSaveFileName()
        file_name = file_name[0]
        file_name = file_name if os.path.isfile(file_name) else file_name + '.txt'
        save_string_to_file(file_name,text)
#end save_to_file

def inizialisiere_button(ui):
    #Box_chois
    #ui.Box_chois.textActivated.connect(lambda: print('textActivated',ui.Box_chois.currentText()) )
    ui.Box_chois.currentTextChanged.connect(lambda: set_box_chois(ui) )
    #Button_directory
    ui.Button_directory.clicked.connect(lambda: clicked_Button_directory(ui) )
    #Button_symbol .zip Anwenden
    ui.Button_symbol.clicked.connect(lambda: clicked_Button_anwenden(ui) )
    #Button_cut Abschneiden
    ui.Button_cut.clicked.connect(lambda: clicked_Button_cut(ui) )
    #links_int rechts_int Ziffer eingabe
    ui.links_int.valueChanged.connect( lambda:  value_int_changed(ui) )
    ui.rechts_int.valueChanged.connect( lambda:  value_int_changed(ui) )
    #buttonBox_start Start Abort
    ui.button_start.clicked.connect(lambda: programm_start(ui))
    ui.Button_save_to_file.clicked.connect(lambda: save_to_file(ui))
#End inizialisiere_button

app = QtWidgets.QApplication(sys.argv)
windou = QtWidgets.QWidget()
ui = FileUi.Ui_Form()
ui.setupUi(windou)
inizialisiere_ui(ui)
inizialisiere_button(ui)
windou.show()
app.exec_()