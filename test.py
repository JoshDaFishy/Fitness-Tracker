# import PySimpleGUI as sg
# import math
# import matplotlib
# # All the stuff inside your window.
# layout = [  [sg.Text('Some text on Row 1')],
#             [sg.Text('Enter something on Row 2'), sg.InputText()],
#             [sg.Button('Ok'), sg.Button('Cancel')] ]

# # Create the Window
# window = sg.Window('Window Title', layout)

# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
#         break
    # print('You entered ', values[0])

# window.close()str

# layout = [[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(-15,-15), graph_top_right=(105,105), background_color='white', key='graph', tooltip='This is a cool graph!')],]    

# window = sg.Window('Graph of Sine Function', layout, grab_anywhere=True, finalize=True)  
# graph = window['graph']

# # Draw axis    
# graph.DrawLine((0,0), (100,0))    
# graph.DrawLine((0,0), (0,100))    

# for x in range(0, 101, 20):    
#     graph.DrawLine((x,-3), (x,3))    
#     if x != 0:    
#         graph.DrawText( x, (x,-10), color='green')    

# for y in range(0, 101, 20):    
#     graph.DrawLine((-3,y), (3,y))    
#     if y != 0:    
#         graph.DrawText( y, (-10,y), color='blue')    

# # Draw Graph    
# for x in range(0,100):    
#     y = math.sin(x/20)*50    
#     graph.DrawCircle((x,y), 1, line_color='red', fill_color='red')    

# event, values = window.read()  

# import PySimpleGUI as sg
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np
# import math

# y_axis = [20, 25, 40, 50]
# x_axis = [1, 2, 3, 4]


# def create_plot(x_axis, y_axis):
#     new_list = range(math.floor(min(x_axis)), math.ceil(max(x_axis))+1)
#     plt.xticks(new_list)

#     plt.plot(x_axis, y_axis, color='black', marker='o')
#     plt.title('Benchpress over time', fontsize=14)
#     plt.xlabel('Chronological entries', fontsize=14)
#     plt.ylabel('Weight moved', fontsize=14)
#     plt.grid(True)
#     return plt.gcf()

# layout = [[sg.Text('Line plot')],
#             [sg.Canvas(size=(1000, 1000), key='-CANVAS-')],
#             [sg.Exit()]
# ]

# def draw_figure(canvas, figrue):
#     figure_canvas_agg = FigureCanvasTkAgg(figrue, canvas)
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
#     return figure_canvas_agg

# window = sg.Window("Graph", layout, finalize=True, element_justification='centre')

# draw_figure(window['-CANVAS-'].TKCanvas, create_plot(x_axis, y_axis))

# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Exit':
#         break

# window.close()

# # matplotlib.use('TkAgg')
# # fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
# # t = np.arange(10, 30, .01)
# # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

# # def draw_figure(canvas, figure):
# #     tkcanvas = FigureCanvasTkAgg(figure, canvas)
# #     tkcanvas.draw()
# #     tkcanvas.get_tk_widget().pack(side='top', fill='both', expand=1)

# #     return tkcanvas
# # layout = [[sg.Text('Plot test')],
# #     [sg.Canvas(key='-CANVAS-')],
# #     [sg.Button('Ok')]]
# # window = sg.Window('Matplotlib In PySimpleGUI', layout, size=(715, 500), finalize=True, element_justification='center', font='Helvetica 18')

# # # add the plot to the window
# # tkcanvas = draw_figure(window['-CANVAS-'].TKCanvas, fig)
# # event, values = window.read()
# # window.close()

import math

from matplotlib import use as use_agg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import PySimpleGUI as sg

def pack_figure(graph, figure):
    canvas = FigureCanvasTkAgg(figure, graph.Widget)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack(side='top', fill='both', expand=1)
    return plot_widget

def plot_figure(index, theta):
    fig = plt.figure(index)         # Active an existing figure
    ax = plt.gca()                  # Get the current axes
    x = [degree for degree in range(1080)]
    y = [math.sin((degree+theta)/180*math.pi) for degree in range(1080)]
    ax.cla()                        # Clear the current axes
    ax.set_title(f"Sensor Data {index}")
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_xscale('log')
    ax.grid()
    plt.plot(x, y)                  # Plot y versus x as lines and/or markers
    fig.canvas.draw()               # Rendor figure into canvas

# Use Tkinter Agg
use_agg('TkAgg')

layout = [[sg.Graph((640, 480), (0, 0), (640, 480), key='Graph1'), sg.Graph((640, 480), (0, 0), (640, 480), key='Graph2')]]
window = sg.Window('Matplotlib', layout, finalize=True)


# Initial
graph1 = window['Graph1']
graph2 = window['Graph2']
plt.ioff()                          # Turn the interactive mode off
fig1 = plt.figure(1)                # Create a new figure
ax1 = plt.subplot(111)              # Add a subplot to the current figure.
fig2 = plt.figure(2)                # Create a new figure
ax2 = plt.subplot(999)              # Add a subplot to the current figure.
pack_figure(graph1, fig1)           # Pack figure under graph
pack_figure(graph2, fig2)
theta1 = 0                          # theta for fig1
theta2 = 90                         # theta for fig2
plot_figure(1, theta1)
plot_figure(2, theta2)

while True:

    event, values = window.read(timeout=10)

    if event == sg.WINDOW_CLOSED:
        break
    elif event == sg.TIMEOUT_EVENT:
        theta1 = (theta1 + 40) % 360
        plot_figure(1, theta1)
        theta2 = (theta2 + 40) % 260
        plot_figure(2, theta2)

window.close()