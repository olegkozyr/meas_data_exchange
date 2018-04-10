# Задати "бекенд" gui для matplotlib
import matplotlib
matplotlib.use('TkAgg')

# Бібліотека для математичних розрахунків
import numpy as np

# Канва та графіка та тулбар для роботи з графіком
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(side=tk.TOP, \
                  fill=tk.BOTH, \
                  expand=tk.YES)
        self._create_widgets()

    def _create_widgets(self):
        self._canvas = FigureCanvasTkAgg(Figure(figsize=(5, 4), \
                                                dpi=100), \
                                         master=self)
        self._canvas.get_tk_widget().pack(side=tk.TOP, \
                                         fill=tk.BOTH, \
                                         expand=tk.YES)
        self._ax = self._canvas.figure.add_subplot(111)
        self._ax.set_xlabel('t, c')
        tk.Label(self, text='Вибірка, с').pack(side=tk.LEFT)
        self.sample = tk.Entry(self, width=5)
        self.sample.pack(side=tk.LEFT)
        self.sample.insert(0, '1')
        tk.Label(self, text='Оновлення, мс').pack(side=tk.LEFT)
        self.fps = tk.Entry(self, width=5)
        self.fps.pack(side=tk.LEFT)
        self.fps.insert(0, '500')
        tk.Button(master=self, 
                  text='Старт', 
                  command=self._start).pack(side=tk.LEFT)
        tk.Button(master=self, 
                  text='Вихід', 
                  command=self._quit).pack(side=tk.LEFT)
        self._timer = None
        self.sampleLen = 0
        self.isStarted = False        

    def _update_canvas(self):
        self._ax.clear()
        t = np.linspace(0, self.sampleLen, 1001)
        # Shift the sinusoid as a function of time.
        self._ax.plot(t, np.sin(2*np.pi*t) + np.random.randn(t.shape[0])/3) 
        self._ax.figure.canvas.draw()

    def _start(self):
        if self.isStarted:
            self._timer.stop()
            self.isStarted = False
        else:
            self.sampleLen = eval(self.sample.get())
            self._timer = self._canvas.new_timer(
                              eval(self.fps.get()), \
                              [(self._update_canvas, (), {})])
            self._timer.start()
            self.isStarted = True

    def _quit(self):       
        self.quit()     # stops mainloop
        self.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Осцилограф") 
    app = Application(master=root)
    app.mainloop()