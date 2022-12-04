import ga
import app
import numpy as np
import PySimpleGUI as sg
import pandas as pd
import os
# Variables
b_counter = 0
slider_it=0
lista_ograniczen_gui =[]
folder = 'Graphs'
png_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.png')]
filenames_only = [f for f in os.listdir(folder) if f.lower().endswith('.png')]
filenum, filename = 0, png_files[0]

# Layouts
layout_selekcji = [
                    [sg.T('Selekcja turniejowa')]
                  ]

layout_populacji = [
                    [sg.T('20')]
                  ]

layout_wyniku = [
                    [sg.T('Minimum globalne:')],
                    [sg.T('', k='W1')],
                    [sg.Text('w punkcie:')],
                    [sg.Text('', k='W2')],
                    [sg.Text('Ograniczenia: ')],
                    [sg.Text('', k='Ograniczenia')],
                  ]

layout_ograniczenia = [
                    [sg.T('', k='OGRPOD')]
                  ]

tab_layout_1 =[[sg.Input(key='ITER')],
               [sg.Button('Wprowadź', key='ITER_B')]]

tab_layout_2 =[[sg.Input(key='P_MUT')],
               [sg.Button('Wprowadź', key='P_MUT_B')]]

tab_layout_3 =[[sg.Input(key='P_CRO')],
               [sg.Button('Wprowadź', key='P_CRO_B')]]
main_tab_layout=[[sg.TabGroup([[sg.Tab('Liczba iteracji', tab_layout_1), sg.Tab('Krzyżowania', tab_layout_2), sg.Tab('Mutacji', tab_layout_3)]])]]
params = [
            [sg.Text('Podaj funkcję f(x[n]):')],
            [sg.Combo(['((1-x[0])**2)+100*(x[1]-x[0]**2)**2', 'sin(x[1])*np.exp((1-cos(x[0]))**2)+cos(x[0])*np.exp((1-sin(x[1]))**2)+(x[0]-x[1])**2', '4*x[0]**2-2.1*x[0]**4+1/3*x[0]**6+x[0]*x[1]-4*x[1]**2+4*x[1]**4','((x[0]-2)**2)+((x[1]-1)**2)'], key='OBJ', size=(65,1))],
            [sg.Button('Wprowadź funkcję', pad=(20, 5), size=(19,1))],
            [sg.Text('Podaj liczbę zmiennych:')],
            [sg.Input(key='-IN-', size=(65,1))],
            [sg.Button('Wprowadź', pad=(20, 5), size=(19,1))],
            [sg.Text('Podaj ograniczenie w postaci g(x[n])<=0:')],
            [sg.Input(key='OGR', size=(65,1))],
            [sg.Radio('Równość', "RADIO", default=True, size=(10,1), key='Row'), sg.Radio('Nierówność', "RADIO", default=False, size=(10,1), key='NRow'), sg.Radio('Nierówność ostra', "RADIO", default=False, size=(10,1), key='ORow')],
            [sg.Button('Wprowadź ograniczenie', pad=(20, 5), size=(19,1))],
            [sg.Frame('Wprowadzone ograniczenia', layout_ograniczenia, size=(270,150), element_justification='l')],
            [sg.Text('Podaj wartości minimalne granic w postaci tablicy:', k='-IN-')],
            [sg.Input(key='-IN-3', size=(65,1))],
            [sg.Button('Wprowadź wartości min', pad=(20, 5), size=(19,1))],
            [sg.Text('Podaj wartości maksymalne granic w postaci tablicy:', k='-IN-')],
            [sg.Input(key='-IN-5', size=(65,1))],
            [sg.Button('Wprowadź wartości max', pad=(20, 5), size=(19,1))],
            # [sg.Frame('Liczba iteracji', layout_slider, size=(180,70), element_justification='c')],
            [sg.Frame('Parametr', main_tab_layout)],
            [sg.Frame('Liczba populacji', layout_populacji, size=(180,50), element_justification='c')],
            [sg.Frame('Rodzaj selekcji', layout_selekcji, size=(180,50), element_justification='c')],
            [sg.Button('Oblicz', size=(20,2), pad=(10, 5))],
        ]


results = [
            [sg.Frame('Wynik', layout_wyniku, size=(546,180), element_justification='l')],
            [sg.Image('Placeholder\placeholder.png', key='PICT')],
            [sg.Button('Poprzednie', size=(8, 2)), sg.Button('Następne', size=(8, 2)),
            sg.Text('Plik 1 of {}'.format(app.paramsy.maxit), size=(15, 1), key='-FILENUM-'),
            sg.Slider(range=(0, 5000), default_value=1, resolution=1, orientation='h',enable_events = True, key='N_PICT', visible=False)],
            [sg.Button('Wyjdź', size=(10,1))]
          ]

layout = [[sg.Column(params, element_justification='l'), sg.VSeparator(), sg.Column(results, element_justification='r')]]
window = sg.Window('Genetic algorithm', layout, resizable=True ) #scaling=.9

# Main loop
while True:
    event, values = window.read()
    if event == 'Wyjdź' or event == sg.WIN_CLOSED:
        break
    elif event == 'Wprowadź funkcję':
        app.funkcja_obj = values.get('OBJ')
    elif event == 'Wprowadź ograniczenie':
        b_counter = b_counter+1
        lista_ograniczen_gui.append(values.get('OGR'))
        window['OGRPOD'].Update(window['OGRPOD'].get()+values.get('OGR')+"\n")
        window['OGR'].Update('')
        if (b_counter == 1):
            app.funkcjaDlaApp.ci1 = lista_ograniczen_gui[0]
            if (values['Row'] == True):
                app.problem.cons_flag[0] = 'Row'
            elif (values['NRow'] == True):
                app.problem.cons_flag[0] = 'NRow'
            elif (values['ORow'] == True):
                app.problem.cons_flag[0] = 'ORow'
        if (b_counter == 2):
            app.funkcjaDlaApp.ci2 = lista_ograniczen_gui[1]
            if (values['Row'] == True):
                app.problem.cons_flag[1] = 'Row'
            elif (values['NRow'] == True):
                app.problem.cons_flag[1] = 'NRow'
            elif (values['ORow'] == True):
                app.problem.cons_flag[1] = 'ORow'
        if (b_counter == 3):
            app.funkcjaDlaApp.ci3 = lista_ograniczen_gui[2]
            if (values['Row'] == True):
                app.problem.cons_flag[2] = 'Row'
            elif (values['NRow'] == True):
                app.problem.cons_flag[2] = 'NRow'
            elif (values['ORow'] == True):
                app.problem.cons_flag[2] = 'ORow'
        if (b_counter == 4):
            app.funkcjaDlaApp.ci4 = lista_ograniczen_gui[3]
            if (values['Row'] == True):
                app.problem.cons_flag[3] = 'Row'
            elif (values['NRow'] == True):
                app.problem.cons_flag[3] = 'NRow'
            elif (values['ORow'] == True):
                app.problem.cons_flag[3] = 'ORow'
        if (b_counter == 5):
            app.funkcjaDlaApp.ci5 = lista_ograniczen_gui[4]
            if (values['Row'] == True):
                app.problem.cons_flag[4] = 'Row'
            elif (values['NRow'] == True):
                app.problem.cons_flag[4] = 'NRow'
            elif (values['ORow'] == True):
                app.problem.cons_flag[4] = 'ORow'
    elif event == 'Wprowadź':
        app.problem.nvar = int(values.get('-IN-'))
        window['OGRPOD'].Update('')
    elif event == 'Wprowadź wartości min':
        app.problem.varmin = pd.eval(values.get('-IN-3'))
    elif event == 'Wprowadź wartości max':
        app.problem.varmax = pd.eval(values.get('-IN-5'))
    elif event == 'ITER_B':
        app.paramsy.maxit = int(values.get('ITER'))
    elif event == 'P_MUT_B':
        app.paramsy.mu = float(values.get('P_MUT'))
    elif event == 'P_CRO_B':
        app.paramsy.crosspro = float(values.get('P_CRO'))
    elif event == 'Oblicz':
        window['PICT'].update(filename='Placeholder\k.png')
        window.refresh()
        app.paramsy.maxit = int(values.get('ITER'))
        pict_slider_max = int(values.get('ITER'))
        window['N_PICT'].update(range=(1, pict_slider_max))
        app.problem.button_counter = b_counter
        out = ga.run(app.problem, app.paramsy)
        g_minimum = out.bestsol.cost
        window['W1'].update(value=g_minimum)
        g_minimum_position = out.bestsol.position
        window['W2'].update(value=g_minimum_position)
        cons =[]
        for i in range (b_counter):
            cons.append(out.bestsol.constraints[i])
        window['Ograniczenia'].update(value=cons)
        lista_ograniczen_gui = []
        b_counter = 0
        window['PICT'].update(filename=filename)
    # Image browsing
    elif event in ('Następne') and filenum < len(png_files) - 1:
        filenum += 1
        filename = os.path.join(folder, filenames_only[filenum])
        window['N_PICT'].update(value=filenum)
        window['PICT'].update(filename=filename)
    elif event in ('Poprzednie') and filenum > 0:
        filenum -= 1
        filename = os.path.join(folder, filenames_only[filenum])
        window['N_PICT'].update(value=filenum)
        window['PICT'].update(filename=filename)
    elif event == 'Exit':
        break
    elif event == 'N_PICT':
        filenum = int(values['N_PICT'])  # int(values.get('N_PICT'))
        filename = os.path.join(folder, filenames_only[filenum])
        window['PICT'].update(filename=filename)
    # update page display
    window['-FILENUM-'].update('Plik {} z {}'.format(filenum + 1, len(png_files)))

window.close()
