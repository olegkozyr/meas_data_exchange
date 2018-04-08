# Задати "бекенд" gui для matplotlib
import matplotlib
matplotlib.use('TkAgg')

# Бібліотека для математичних розрахунків
import numpy as np

# Канва та графіка та тулбар для роботи з графіком
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
                                              NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler

from matplotlib.figure import Figure

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = FigureCanvasTkAgg(Figure(figsize=(5, 4), \
                                               dpi=100), \
                                        master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, \
                                         fill=tk.BOTH, \
                                         expand=tk.YES)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, 
                                               self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, 
                                   fill=tk.BOTH, 
                                   expand=tk.YES)
        self.canvas.mpl_connect('key_press_event', 
                                self.on_key_event)
        self.ax = self.canvas.figure.add_subplot(111)
        tk.Button(master=self, 
                  text='Quit', 
                  command=self._quit).pack(side=tk.BOTTOM)
        self._update_canvas()

    def _update_canvas(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        self.ax.plot(t, s)

    def on_key_event(self, event):
        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas, self.toolbar)

    def _quit(self):
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
 
if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Осцилограф") 
    app = Application(master=root)
    app.mainloop()