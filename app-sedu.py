# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

import urllib.request
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Estacion meteorologica App")
#root.attributes('-fullscreen', True)
root.state('zoomed')
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
mainframe = ttk.Frame(root, padding= str(w) + str(h) + "12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

sensor = StringVar() #El sensor en el que haremos la lectura
entradas = StringVar() #El numero de lecturas que haremos para el sensor seleccionado
valores = StringVar() #Los valores impresos con el comando GET

def get_valores():
    url = "https://api.thingspeak.com/channels/283217/fields/" + sensor.get() + ".json?api_key=APMYAASGZ249UAR9&results=" + entradas.get()
    val = urllib.request.urlopen(url).read()
    valores.set(val)

feet_entry = ttk.Entry(mainframe, width=7, textvariable=entradas)
feet_entry.grid(column=1, row=1, sticky=(W, E))
"""
feet_entry = ttk.Entry(mainframe, width=7, textvariable=sensor)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=valores).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Refresh", command=get_valores).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="Sensor").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Resultados").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="valores").grid(column=3, row=2, sticky=W)
"""
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', get_valores)
root.mainloop()
