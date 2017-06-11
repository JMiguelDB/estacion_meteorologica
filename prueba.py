import urllib.request
import time
import json
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk



LARGE_FONT= ("Verdana", 12)

def get_valores():
    print(api.get())
    print(entradas.get())
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
    tv.pack()
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

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Sea of BTC client")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, TablePage, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        entradas = StringVar() #El numero de lecturas que haremos para el sensor seleccionado
        api = IntVar() #Selecciona si se utiliza la api nuestra o la de alberto y juan
        
        label = tk.Label(self, text="Lectura de valores de sensores:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        ttk.Label(self, text="Lectura de valores de sensores:").pack()

        ttk.Checkbutton(self, text="API Fitngrow", variable=api).pack()
        
        ttk.Label(self, text="Nº lecturas").pack()
        
        ttk.Entry(self, width=7, textvariable=entradas).pack()

        print('Valores',entradas,api)
        #ttk.Button(self, text="Refresh", command=get_valores).pack()
        
        #ttk.Button(self, text="Refresh", command=get_valores).pack()

        button = ttk.Button(self, text="Table",
                            command=lambda: controller.show_frame(TablePage))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()


class TablePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        print(controller)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        
        get_valores()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(TablePage))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        

app = SeaofBTCapp()
app.bind('<Return>', get_valores)
app.mainloop()