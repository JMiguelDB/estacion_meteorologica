import urllib.request
from tkinter import *
from tkinter.ttk import *
import time
import json
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

root = Tk()
root.title("Estacion meteorologica App")
root.state('zoomed')
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
mainframe = ttk.Frame(root, padding= str(w) + str(h) + "12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

mainframe1 = ttk.Frame(root)

sensor = StringVar() #El sensor en el que haremos la lectura
entradas = StringVar() #El numero de lecturas que haremos para el sensor seleccionado
valores = StringVar() #Los valores impresos con el comando GET
api = IntVar() #Selecciona si se utiliza la api nuestra o la de alberto y juan

def get_valores():
    if api.get() == 1:
        if entradas.get() == 'all':
            url = "https://api.thingspeak.com/channels/283234/feeds.json"
        else:
            url = "https://api.thingspeak.com/channels/283234/feeds.json?results=" + entradas.get()
    else:
        if entradas.get() == 'all':
            url = "https://api.thingspeak.com/channels/283217/feeds.json?api_key=APMYAASGZ249UAR9"
        else:
            url = "https://api.thingspeak.com/channels/283217/feeds.json?api_key=APMYAASGZ249UAR9&results=" + entradas.get()
    val = urllib.request.urlopen(url).read()
    val_json = json.loads(val.decode('utf-8'))
    #print(val_json)
    del val_json['channel']['longitude']
    del val_json['channel']['latitude']
    del val_json['channel']['updated_at']
    del val_json['channel']['last_entry_id']
    del val_json['channel']['id']
    del val_json['channel']['name']
    del val_json['channel']['created_at']

    tv = Treeview()
    headers =list(val_json['channel'])
    val = []
    for j in range(len(headers)):
        val.append(val_json['channel'][headers[j]])
    headers.append('created_at')
    val = tuple(val)
    tv['columns'] = val
    tv.heading("#0", text='created_at', anchor='w')
    tv.column("#0", anchor="w")
    for j in val:     
        tv.heading(j, text=j, anchor='w')
        tv.column(j, anchor='center', width=100)
    #print(tv['columns'])
    #print(val)
    tv.grid(column=1, row=1, sticky = (N,S,W,E))
    body = val_json['feeds']
    for i in body:
        val = []
        for j in headers:
            try:
                val.append(i[j])
            except:
                val.append(None)
        #print(val[0:-1])
        tv.insert('', 'end', text=val[-1], values=tuple(val[0:-1]))
    for child in tv.get_children():
          # For some odd reason the "set" method actually returns the values
          # if you're not actually setting something
          print(tv.set(child))
        

ttk.Label(mainframe, text="Lectura de valores de sensores:").grid(column=1, row=1, sticky=W)

c = Checkbutton(mainframe, text="API Fitngrow", variable=api)
c.grid(column=1, row=2, sticky=(W, E))

ttk.Label(mainframe, text="Nº lecturas").grid(column=1, row=3, sticky=W)
feet_entry = ttk.Entry(mainframe, width=7, textvariable=entradas)
feet_entry.grid(column=2, row=3, sticky=(W, E))

ttk.Button(mainframe, text="Refresh", command=get_valores).grid(column=1, row=4, sticky=W)

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

canvas = FigureCanvasTkAgg(f, root)
canvas.show()
canvas.get_tk_widget().grid(column=15, row=1, sticky=W)

toolbar = NavigationToolbar2TkAgg(canvas, mainframe1)
toolbar.update()
canvas._tkcanvas.grid(column=15, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', get_valores)
root.mainloop()