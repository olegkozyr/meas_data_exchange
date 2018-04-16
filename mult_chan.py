# Задати "бекенд" gui для matplotlib
import matplotlib
matplotlib.use('TkAgg')

# Бібліотека для математичних розрахунків
import numpy as np

# Канва та графіка та тулбар для роботи з графіком
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure

import tkinter as tk

tby = dict(side=tk.TOP, \
           fill=tk.BOTH, \
           expand=tk.YES)

txn = dict(side=tk.TOP, \
           fill=tk.X, \
           expand=tk.NO)

class CanvasFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(tby)

        self._canvas = FigureCanvasTkAgg(Figure(figsize=(5, 4), \
                                                dpi=100), \
                                         master=self)
        self._canvas.get_tk_widget().pack(tby)
        self._ax = self._canvas.figure.add_subplot(111)
        self._ax.set_xlabel('t, c')
        self._ax.grid()

class RunFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(txn)

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
                  command=master._start).pack(side=tk.LEFT) 
        tk.Button(master=self, 
                  text='Вихід', 
                  command=self._quit).pack(side=tk.RIGHT) 

    def _quit(self):       
        self.quit()     
        self.destroy()   

    def get_sample_size(self):
        return eval(self.sample.get())

    def get_fps(self):
        return eval(self.fps.get())

class SaveFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(txn)
        self.fileHandle = None
        self.checkVar = tk.IntVar()
        self.saveCheckbutton = tk.Checkbutton(self, text="Зберегти", variable=self.checkVar) 
        self.saveCheckbutton.pack(side=tk.LEFT)
        self.pathVar = tk.StringVar()
        self.filedialog = tk.filedialog
        tk.Label(self, text='Файл').pack(side=tk.LEFT)
        self.file_path = tk.Entry(self, textvariable=self.pathVar, width=50)
        self.file_path.pack(side=tk.LEFT)
        tk.Button(master=self, 
                  text='Створити', 
                  command=self._save2file).pack(side=tk.LEFT)  

    def _save2file(self):
        self.pathVar.set(self.filedialog.asksaveasfilename(initialdir = "", \
                                           title = "Створити файл", \
                                           filetypes = (("Txt files","*.txt"),("all files","*.*"))))
        if self.pathVar.get(): 
            with open(self.pathVar.get(), 'w') as f:
                pass
#f.write('{:.4f} {:.4f} {}'.format(2.4, 5.666, '\n'))
#f.write('Second Line' +'\n')

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(tby)
        self._timer = None
        self.sampleLen = 0
        self.isStarted = False           
        self._create_widgets()

    def _create_widgets(self):
        self.canvasFrame = CanvasFrame(self)
        self.canvasFrame.pack(tby)
        self.runFrame = RunFrame(self)
        self.runFrame.pack(txn)
        self.saveFrame = SaveFrame(self)
        self.saveFrame.pack(txn)

    def _update_canvas(self):
        self.canvasFrame._ax.clear()
        t = np.linspace(0, self.sampleLen, 1001)
        # Shift the sinusoid as a function of time.
        x1 = np.sin(2*np.pi*t) + np.random.randn(t.shape[0])/10
        x2 = np.cos(2*np.pi*t) + np.random.randn(t.shape[0])/10
        x3 = np.sin(2*np.pi*t) * np.cos(2*np.pi*t) + \
                                 np.random.randn(t.shape[0])/10
        self.canvasFrame._ax.plot(t, x1, label='ch0')
        self.canvasFrame._ax.plot(t, x2, label='ch1') 
        self.canvasFrame._ax.plot(t, x3, label='ch2')  
        self.canvasFrame._ax.legend(loc=1)
        self.canvasFrame._ax.grid()
        self.canvasFrame._ax.figure.canvas.draw()
        self.saveFrame.fileHandle.write('{:.4f} {:.4f} {:.4f} {}'.format(2.4, 5.666, '\n'))
    
    def _start(self):
        if self.isStarted:
            self._timer.stop()
            if self.saveFrame.fileHandle:
                self.saveFrame.fileHandle.close()
                self.saveFrame.fileHandle = None
            self.isStarted = False
        else:
            self.sampleLen = self.runFrame.get_sample_size()
            self._timer = self.canvasFrame._canvas.new_timer(
                              self.runFrame.get_fps(), \
                              [(self._update_canvas, (), {})])
            self._timer.start()
            if self.saveFrame.checkVar.get() and self.saveFrame.pathVar.get():
                self.saveFrame.fileHandle = open(self.saveFrame.pathVar.get(), 'w')
            self.isStarted = True


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Осцилограф") 
    app = Application(master=root)
    app.mainloop()