import sqlite3
import PySimpleGUI

layout = [ [PySimpleGUI.Text('Hello, world!')] ]
window = PySimpleGUI.Window('Hello Example', layout)
while True:
    event, values = window.read()
    if event == PySimpleGUI.WIN_CLOSED:
        break
window.close()
