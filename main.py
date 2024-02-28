import sqlite3
import PySimpleGUI as sg

# conncet = sqlite3.connect('tracker.db')
# c = conncet.cursor()
# c.execute("""CREATE TABLE exercises (
#         exercise text,
#         weight integer
#     )""")

def submit(values):
    # connect to database
    conncet = sqlite3.connect('tracker.db')

    # create cursork
    c = conncet.cursor()

    c.execute(f"SELECT * FROM exercises WHERE exercise = ?", (values['inp'],))    
    data = c.fetchone()
    if data > 0:
        pass
    else:
    #insert into table
        c.execute("INSERT INTO exercises VALUES (:exercise, :weight)",
                {
                    'exercise': values['inp'],#drop down menu,
                    'weight': values['weightinp']#input field 
                }
                )
        conncet.commit()


    # close connection
    conncet.close()
    window['inp'].update('')


def callData(values):
    # connect to database
    conncet = sqlite3.connect('tracker.db')

    # create cursork
    c = conncet.cursor()
    
    c.execute(f"SELECT *, oid FROM exercises WHERE exercise = ?", (values['inp'],))    
    data = c.fetchall()
    print(data)





sg.theme('DarkAmber')

names = ['test1', 'test2', 'test3', 'test4', 'test5']

l2=sg.Text("test on page 2")
tab1= [     [sg.Text('Exercise'), sg.Combo(names, key="inp", enable_events=True, default_value='')],
            [sg.Text('Total Weight'), sg.InputText(do_not_clear=False, key='weightinp')],]
tab2= [     [sg.Button('Test')]]

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
        submit(values)
    elif event == "Clear":
        print("clearing page")
        window['inp'].update('')
    elif event == 'Test':
        callData(values)
window.close()
