import sqlite3
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# conncet = sqlite3.connect('tracker.db')
# c = conncet.cursor()
# c.execute("""CREATE TABLE exercises (
#         exercise text,
#         weight integer
#     )""")

exerciseAdded = False
actionsDone = 0


y_axis = [0]
x_axis = [0]


def create_plot(isEmpty, exercise):
    if isEmpty: 
        y_axis = [0]
        x_axis = [0]
        new_list = range(math.floor(min(x_axis)), math.ceil(max(x_axis))+1)
        plt.xticks(new_list)
        plt.plot(x_axis, y_axis, color='black', marker='o')
        plt.title('Benchpress over time', fontsize=14)
        plt.xlabel('Chronological entries', fontsize=14)
        plt.ylabel('Weight moved', fontsize=14)
        plt.grid(True)
        return plt.gcf()
    conncet = sqlite3.connect('tracker.db')

    # create cursork
    c = conncet.cursor()
    c.execute(f"SELECT id FROM exercises WHERE exercise = ?", (exercise,))    
    data = c.fetchone()

    #note: i'm most certainly supposed to be using an inner join rather than 2 separate statements but this is simpler for my brain and lazier
    c.execute(f"SELECT weight FROM data WHERE exercise_id = ?", (data[0],))  
    weightData = c.fetchall()
    increments = []
    #convert the data into lists matplot can understand
    for i in range(1,len(weightData)+1):
        increments.append(i)
    realWeighData = []
    for tuplething in weightData:
        realWeighData.append(tuplething[0])
    new_list = range(math.floor(min(increments)), math.ceil(max(increments))+1)
    plt.xticks(new_list)
    plt.plot(increments, realWeighData, color='black', marker='o')
    plt.title(f'{exercise} progress over time', fontsize=14)
    plt.xlabel('Chronological entries', fontsize=14)
    plt.ylabel('Weight moved', fontsize=14)
    plt.grid(True)
    return plt.gcf()

def draw_figure(canvas, figrue):
    figure_canvas_agg = FigureCanvasTkAgg(figrue, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg



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
    #input validation , maybe should be tooltip
    if values['weightinp'] == '' or values['inp'] == '':
        sg.popup_ok("You must fill in all fields before submitting", title="Error")
        return
    try:
        int(values['weightinp'])
    except ValueError:
        sg.popup_ok("You must enter a valid number", title="Error")
        return
    c.execute("SELECT MAX(rowid) FROM data")
    maxrow = c.fetchone()
    if data != None:
    #adding data to an existing exercise
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
    #adding data to a new exercise
        c.execute("SELECT MAX(rowid) FROM exercises")
        maxrow = c.fetchone()
        if maxrow[0] == None:
        #if no exercise has been created yet
            c.execute("INSERT INTO exercises VALUES (:id, :exercise)",
                    {
                        'id': 1,
                        'exercise': values['inp'],#drop down menu,
                    }
                    )
            conncet.commit()
            exerciseAdded = True
            actionsDone += 1
            names.append(values['inp'])
            window['inp'].update(values=names)
            print(names)
            c.execute("SELECT MAX(id) FROM data")
            maxrow = c.fetchone()
            c.execute(f"SELECT id, exercise FROM exercises WHERE exercise = ?", (values['inp'],))    
            data = c.fetchone()
            c.execute("INSERT INTO data VALUES (:id, :weight, :exercise_id)",
                    {
                        'id': 1,
                        'weight': values['weightinp'],#drop down menu,
                        'exercise_id': data[0]
                    }
                    )
            conncet.commit()   
        else:
        #if one has already been
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
            c.execute("SELECT MAX(id) FROM data")
            maxrow = c.fetchone()
            c.execute(f"SELECT id, exercise FROM exercises WHERE exercise = ?", (values['inp'],))    
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
        c.execute("DELETE FROM exercises WHERE id = (SELECT MAX(id) FROM exercises)")
        c.execute("DELETE FROM data WHERE id = (SELECT MAX(id) FROM exercises)")
        conncet.commit()  
    else:
        print('also running')
        c.execute("DELETE FROM data WHERE id = (SELECT MAX(id) FROM exercises)")
        conncet.commit()   
    exerciseAdded = False
    actionsDone -= 1
    #searches data table for most recent item and finds the 
    #if the new exercise added is true then remove that
#review data section

sg.theme('DarkAmber')

conncet = sqlite3.connect('tracker.db')
c = conncet.cursor()
c.execute(f"SELECT exercise FROM exercises")    
data = c.fetchall()
print(data)
names = []
for exercise in data:
    names.append(exercise[0])
print(names)

l2=sg.Text("test on page 2")
tab1= [     [sg.Text('Exercise'), sg.Combo(names, key="inp", enable_events=True, default_value='', expand_x=True)],
            [sg.Text('Total Weight'), sg.InputText(do_not_clear=False, key='weightinp')],]
frameContents = [[sg.Canvas(size=(600, 600), key='-CANVAS-')], [sg.Text('placeholder')]]
tab2= [     [sg.Frame('graphHolder',frameContents)],
            [sg.Combo(names, key='graphChoice', enable_events=True, default_value='', expand_x=True, readonly=True)]]

layout = [
            [sg.TabGroup([
            [sg.Tab('Data Entry', tab1),
            sg.Tab('Review Data', tab2)]])],
            #[psg.OK(), psg.Cancel()]
            [sg.Button('Submit'), sg.Button('Clear'), sg.Button('Undo')] ]

# tab2=sg.Tab("title2", l2)
# Tg = sg.TabGroup([[tab1, tab2]])



window = sg.Window('Hello Example', layout, finalize=True)

draw_figure(window['-CANVAS-'].TKCanvas, create_plot(True,''))

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
    elif event == 'graphChoice':
        # draw_figure(window['-CANVAS-'].TKCanvas, create_plot(False, values['graphChoice']))
        #TODO finish this part - the dynamic graph will be the last bit basically. I just need the extend layout to work
        window['-CANVAS-'].TKCanvas.destroy()
        newitem = [[sg.Text('testing')]]
        window.extend_layout(window['graphHolder', newitem])
        # window.extend_layout(window['graphHolder'], draw_figure(window['-CANVAS-'].TKCanvas, create_plot(False, values['graphChoice'])))
        # window['-CANVAS-'].TKCanvas.update(draw_figure(window['-CANVAS-'].TKCanvas, create_plot(False, values['graphChoice'])))
window.close()

#TODO check that if you only enter a number it actually gets caught by the error handler before submitting, same with undo button