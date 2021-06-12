import os
import re
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY,PLAIN_COLUMNS,MARKDOWN,ORGMODE

def print_list_zeilen(liste: list,spalten=1):
    leerres_elem = ' '
    table = PrettyTable(header=False)
    table.set_style(ORGMODE) #1)DEFAULT 2)PLAIN_COLUMNS  3)MARKDOWN  4)ORGMODE
    print_list = liste[:]
    #temp_num = list(range(len(liste)))
    temp_num = [ str(iter)+')' for iter in range(len(liste)) ]
    while ( len(print_list) % spalten != 0 ):
        print_list.append(leerres_elem)
        temp_num.append(leerres_elem)
    #end while
    anzahl_elem = len(print_list) // spalten
    for iter in range(spalten):
        first_num = iter*anzahl_elem
        second_num = (iter+1)*anzahl_elem
        header_num = '№ {0}-{1}'.format(first_num,second_num)
        #header_name = 'Field № {0}-{1}'.format(first_num,second_num)
        header_name = 'Field {0}'.format(iter+1)
        #Erzeuge Spalten
        table.add_column(header_num,temp_num[first_num:second_num])
        table.add_column(header_name,print_list[first_num:second_num])
    print(table)
#end print_list_zeilen

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

def konvert_str_2_num(eingabe: str):
    #Eingabe string, ausgabe int, float, oder ValueError
    output = None
    try:
        output = int(eingabe)
    except ValueError:
        output = float(eingabe)
    return output
#end konvert_str_2_num

def main(path='',vorg_maske='',vorg_dat_end=[],vorg_ignore_num_str=0):
    # E:\Video WD\Temp\X Manga\Manhva\Параллельный_рай_Parallel_Paradise
    such_maske = ''
    ignor_str_num = vorg_ignore_num_str
    eingabe_1 = input('Verzeichniss eingeben: ') if path =='' else path
    if (os.path.isdir(eingabe_1)):
        inhalt = os.listdir(eingabe_1)

        #1 Найти файлы 
        #2 Найти окончание файлов если есть
        #3 Сгрупировать фалы с одинаковым окончанием
        #4 Какие файлы проверять с числами

        datei_endung = set()
        dateien_list = [] #alle gefundenen Dokumente
        dat_no_end = []
        pattern = re.compile('[0-9]+')
        #Suche alle Daten(files) mit Nummer
        for elem in inhalt:
            path = os.path.join(eingabe_1,elem)
            match = pattern.search(elem)
            if (match != None and os.path.isfile(path)):
                temp_num = elem.rfind('.')
                dateien_list.append(elem)
                if (temp_num != -1 ):
                    temp_end = elem[temp_num:]
                    datei_endung.add(temp_end)
                else:
                    dat_no_end.append(elem)
                #end if
            #end if
        #end for
    else:
        print('Einegegebene verzeichniss',eingabe_1,'exestirt nicht oder nicht richtig erkant')
        print('Versuchen Sie bitte erneurt')
        main()
    #end if
    #print_list_spalten(dateien_list,2)
    print('Folgende Dateiendungen gefunden:', datei_endung)
    print('Folgende Dateien gefunden')
    print_list_zeilen(dateien_list,2)
    #Wurden such parametern uebergeben? Falls Nein, bevutzer abfragen
    if ( vorg_maske == '' and vorg_dat_end == [] ):
        benutzer_zufrieden = False
        while ( not(benutzer_zufrieden) ):
            #Suchpatern muss am anfang der datei sein und bei allen dateien gleich sein
            eingabe_2 = input('Geben Sie einen Suchpatern an: ')
            eingabe_4 = input('Anzahl Anfangsbuchstaben die ignoriert werden eingeben (default ist 0) oder ENTER: ')
            try:
                eingabe_4 = eingabe_4.replace(' ','')
                ignor_str_num = int(eingabe_4) if eingabe_4 != '' else vorg_ignore_num_str
            except ValueError:
                ignor_str_num = vorg_ignore_num_str
            if (eingabe_2 != ''):
                eingabe_3 = input('Folgende Suchpatern: ' + eingabe_2 + '\nuntersuchen und '
                                   + str(ignor_str_num) + ' anfangsbuchstaben ignorieren, Y/N? ')
                benutzer_zufrieden = True if eingabe_3=='Y' else False
                such_maske = eingabe_2
        #end while
    else:
        such_maske = vorg_maske
    #end if
    #Jetzt werden alle Daten mit nummern ausgewertet
    pattern = re.compile('([0-9]+.{1}[0-9]+)|([0-9]+)')
    min_num = 1000
    max_num = 0
    zahlen_list_int =[]
    zahlen_list_float =[]
    if ( such_maske != '' ):
        for elem in dateien_list:
            if (such_maske in elem):
                string = elem[ignor_str_num:]
                match = pattern.search(string)
                if (match != None):
                    #Uberprufe nach int oder float
                    try:
                        zahl = int(match[0])
                        min_num = min(min_num,zahl)
                        max_num = max(max_num,zahl)
                        zahlen_list_int.append(zahl)
                    except ValueError:
                        zahl = float(match[0].replace(',', ''))
                        zahlen_list_float.append(zahl)
                #end if
            #end if
        #end for
    #end if
    
    #fehlende Nummer
    fehlende_num = [zahl for zahl in range(min_num,max_num+1) if zahl not in zahlen_list_int]
    print('Maximum int ist {0}, minimale int ist {1}'.format(max_num,min_num))
    print('Insgesamt gibt es {0} int Daten'.format(len(zahlen_list_int)))
    if (len(fehlende_num) !=0 ): 
        print('Es fehlen folgende int Nummer')
        print_list_spalten(fehlende_num)
    if ( len(zahlen_list_float)!=0 ):
        print('Ausserden gibt es {0} float Nummer'.format(len(zahlen_list_float)))
        #print_list_spalten(zahlen_list_float)
#end main

if __name__ == '__main__':
    gehe_in = r"E:\Manga\neu\Wedding_Ring_Story___История_с_обручальным_кольцом___Kekkon_Yubiwa_Monogatari"
    maske = "№"
    main(path=gehe_in,vorg_ignore_num_str=0,vorg_maske=maske)#vorg_maske='Параллельный_рай_Parallel_Paradise_Глава_№')
    #test()
#Прикоснись_чтобы_открыть__Touch_to_unlock fehlen 59,60
#Параллельный_рай_Parallel_Paradise 20
#Рассвет_Йоны 192,193
#Король_Ада___King_of_hell 178, 179, 180, 181
#Месть_Масамуне-куна!___Masamune's_Revenge 35, 46
#Инуяша___InuYasha 488-518





    