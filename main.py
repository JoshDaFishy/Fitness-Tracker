import sqlite3
import PySimpleGUI as sg

sg.theme('DarkAmber')

names = ['test1', 'test2', 'test3', 'test4', 'test5']

l2=sg.Text("test on page 2")
tab1= [     [sg.Text('Exercise'), sg.Combo(names, key="inp", enable_events=True, default_value='')],
            [sg.Text('Total Weight'), sg.InputText(do_not_clear=False)],]
tab2=[[l2]]

layout = [
            [sg.TabGroup([
            [sg.Tab('Data Entry', tab1),
            sg.Tab('Review Data', tab2)]])],
            #[psg.OK(), psg.Cancel()]
            [sg.Button('Submit'), sg.Button('Clear')] ]

# tab2=sg.Tab("title2", l2)
# Tg = sg.TabGroup([[tab1, tab2]])

window = sg.Window('Hello Example', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'inp':
        print(values["inp"])
    elif event == "Submit":
        print("submiting data")
        window['inp'].update('')
    elif event == "Clear":
        print("clearing page")
        window['inp'].update('')
window.close()
