import sqlite3
import PySimpleGUI as sg

# conncet = sqlite3.connect('tracker.db')
# c = conncet.cursor()
# c.execute("""CREATE TABLE exercises (
#         exercise text,
#         weight integer
#     )""")

exerciseAdded = False
actionsDone = 0

def submit(values):
    global exerciseAdded
    global names
    global actionsDone
    # connect to database
    conncet = sqlite3.connect('tracker.db')

    # create cursork
    c = conncet.cursor()

    c.execute(f"SELECT id, exercise FROM exercises WHERE exercise = ?", (values['inp'],))    
    data = c.fetchone()
    if values['weightinp'] == '' or values['inp'] == '':
        sg.popup_ok("You must fill in all fields before submitting", title="Error")
        return
    c.execute("SELECT MAX(rowid) FROM data")
    maxrow = c.fetchone()
    if data != None:
        c.execute("INSERT INTO data VALUES (:id, :weight, :exercise_id)",
                {
                    'id': maxrow[0] + 1,
                    'weight': values['weightinp'],#drop down menu,
                    'exercise_id': data[0]
                }
                )
        conncet.commit() 
        exerciseAdded = False
        actionsDone += 1    
    else:
    #insert into table
        c.execute("SELECT MAX(rowid) FROM exercises")
        maxrow = c.fetchone()
        c.execute("INSERT INTO exercises VALUES (:id, :exercise)",
                {
                    'id': maxrow[0] + 1,
                    'exercise': values['inp'],#drop down menu,
                }
                )
        conncet.commit()
        exerciseAdded = True
        actionsDone += 1
        names.append(values['inp'])
        window['inp'].update(values=names)
        print(names)
        c.execute("SELECT MAX(rowid) FROM data")
        maxrow = c.fetchone()
        c.execute(f"SELECT rowid, exercise FROM exercises WHERE exercise = ?", (values['inp'],))    
        data = c.fetchone()
        c.execute("INSERT INTO data VALUES (:id, :weight, :exercise_id)",
                {
                    'id': maxrow[0] + 1,
                    'weight': values['weightinp'],#drop down menu,
                    'exercise_id': data[0]
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
    
    c.execute(f"SELECT *, rowid FROM exercises WHERE exercise = ?", (values['inp'],))    
    data = c.fetchall()
    print(data)


def undo():
    global exerciseAdded, actionsDone
    if actionsDone == 0:
        sg.popup_ok("No action to undo!", title="Error")
        return
    conncet = sqlite3.connect('tracker.db')
    c = conncet.cursor()
    if exerciseAdded == True:
        print('running')
        c.execute("DELETE FROM exercises WHERE rowid = (SELECT MAX(rowid) FROM exercises)")
        c.execute("DELETE FROM data WHERE rowid = (SELECT MAX(rowid) FROM exercises)")
    else:
        print('also running')
        c.execute("DELETE FROM data WHERE rowid = (SELECT MAX(rowid) FROM exercises)")
    exerciseAdded = False
    actionsDone -= 1
    #searches data table for most recent item and finds the 
    #if the new exercise added is true then remove that
#TODO add an undo button, review data section

sg.theme('DarkAmber')

conncet = sqlite3.connect('tracker.db')
c = conncet.cursor()
c.execute(f"SELECT * FROM exercises")    
data = c.fetchall()
print(data)
names = []
for exercise in data:
    names.append(exercise[0])
print(names)

l2=sg.Text("test on page 2")
tab1= [     [sg.Text('Exercise'), sg.Combo(names, key="inp", enable_events=True, default_value='')],
            [sg.Text('Total Weight'), sg.InputText(do_not_clear=False, key='weightinp')],]
tab2= [     [sg.Button('Test')]]

layout = [
            [sg.TabGroup([
            [sg.Tab('Data Entry', tab1),
            sg.Tab('Review Data', tab2)]])],
            #[psg.OK(), psg.Cancel()]
            [sg.Button('Submit'), sg.Button('Clear'), sg.Button('Undo')] ]

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
    elif event == "Undo":
        print("undoing last action")
        undo()
    elif event == 'Test':
        callData(values)
window.close()
