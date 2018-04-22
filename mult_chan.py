# Задати "бекенд" gui для matplotlib
import matplotlib
matplotlib.use('TkAgg')

# Бібліотека для математичних розрахунків
import numpy as np

from time import localtime, strftime

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
        tk.Label(self, text='dt, c').pack(side=tk.LEFT)
        self.dt = tk.Entry(self, width=5)
        self.dt.pack(side=tk.LEFT)
        self.dt.insert(0, '0.01')
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
                  command=master.start).pack(side=tk.LEFT) 
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

    def get_dt(self):
        return eval(self.dt.get())

class SaveOpenFrame(tk.Frame):
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
                  command=self._file_save).pack(side=tk.LEFT)  
        tk.Button(master=self, 
                  text='Відкрити', 
                  command=self._file_open).pack(side=tk.RIGHT)  

    def _file_save(self):
        self.pathVar.set(self.filedialog.asksaveasfilename(initialdir = "", \
                                           title = "Створити файл", \
                                           filetypes = (("Txt files","*.txt"),("all files","*.*"))))

    def _file_open(self):
        path = self.filedialog.askopenfilename(initialdir = "", \
                                           title = "Відкрити файл", \
                                           filetypes = (("Txt files","*.txt"),("all files","*.*")))

        chanNames = []
        dt = 0.0
        with open(path, 'r') as f:
            f.readline().split()
            dt = eval(f.readline()[3:])
            chanNames = f.readline().split()
        data = np.genfromtxt(path, skip_header=3)
        self.master.update_canvas([np.arange(0, data.shape[0]*dt, dt), data[:, 0], data[:, 1], data[:, 2]], chanNames)

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(tby)
        self._timer = None
        self.sampleLen = 0
        self.dt = 0
        self.isStarted = False    
        self.channels = ['ch0', 'ch1', 'ch2']
        self._create_widgets()

    def _create_widgets(self):
        self.canvasFrame = CanvasFrame(self)
        self.canvasFrame.pack(tby)
        self.runFrame = RunFrame(self)
        self.runFrame.pack(txn)
        self.saveFrame = SaveOpenFrame(self)
        self.saveFrame.pack(txn)

    def _genarator(self):
        t = np.arange(0, self.sampleLen, self.dt)
        ch0 = np.sin(2*np.pi*t) + np.random.randn(t.shape[0])/10
        ch1 = np.cos(2*np.pi*t) + np.random.randn(t.shape[0])/10
        ch2 = np.sin(2*np.pi*t) * np.cos(2*np.pi*t) + \
                                  np.random.randn(t.shape[0])/10 
        #return np.transpose(np.vstack((t, ch0, ch1, ch2)))
        return [t, ch0, ch1, ch2]

    def update_canvas(self, data, chanNames):
        '''
           Update figure plots
        '''
        self.canvasFrame._ax.clear()
        self.canvasFrame._ax.plot(data[0], data[1], label=chanNames[0])
        self.canvasFrame._ax.plot(data[0], data[2], label=chanNames[1])
        self.canvasFrame._ax.plot(data[0], data[3], label=chanNames[2])
        self.canvasFrame._ax.legend(loc=1)
        self.canvasFrame._ax.grid()
        self.canvasFrame._ax.figure.canvas.draw()

    def _save2file(self, data):
        '''
           Save data to file
        '''
        for x0, x1, x2 in zip(data[1], data[2], data[3]):
            self.saveFrame.fileHandle.write('{:.4f} {:.4f} {:.4f}{}'.format(x0, x1, x2, '\n'))
            self.saveFrame.fileHandle.flush()

    def _plot(self):
        data = self._genarator()
        self.update_canvas(data, self.channels)

    def _plot_save(self):
        data = self._genarator()
        self.update_canvas(data, self.channels)
        self._save2file(data)

    def start(self):
        if self.isStarted:
            self._timer.stop()
            if self.saveFrame.fileHandle:
                self.saveFrame.fileHandle.close()
                self.saveFrame.fileHandle = None
            self.isStarted = False
        else:
            self.sampleLen = self.runFrame.get_sample_size() 
            self.dt = self.runFrame.get_dt()
            if self.saveFrame.checkVar.get() and self.saveFrame.pathVar.get():
                self.saveFrame.fileHandle = open(self.saveFrame.pathVar.get(), 'w')                               
                self.saveFrame.fileHandle.write('{}{}'.format(\
                    strftime("%a, %d %b %Y %H:%M:%S +0300", localtime()), '\n'))
                self.saveFrame.fileHandle.write('dt={}{}'.format(self.dt, '\n'))
                self.saveFrame.fileHandle.write('{} {} {}{}'.format('ch0', 'ch1', 'ch2', '\n'))
                self.saveFrame.fileHandle.flush()                
                self._timer = self.canvasFrame._canvas.new_timer(
                                  self.runFrame.get_fps(), \
                                  [(self._plot_save, (), {})])
            else:
                self._timer = self.canvasFrame._canvas.new_timer(
                                  self.runFrame.get_fps(), \
                                  [(self._plot, (), {})])
            self._timer.start()
            self.isStarted = True

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Осцилограф") 
    app = Application(master=root)
    app.mainloop()