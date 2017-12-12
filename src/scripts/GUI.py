import batch
import pyaudio
import wave
import nn as nn
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "input.wav"
DATA_OUTPUT_FILENAME = "output.txt"
DEFAULT_JSON_FILE = '../../data/model/model.json'
DEFAULT_H5_FILE = '../../data/model/weights.h5'


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recognition")
        self.tabControl = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Validation')
        self.tabControl.add(self.tab2, text='Training')

        self.lf_output = LabelFrame(self.tab1, text="Output")
        self.ent_output = Entry(self.lf_output)
        self.btn_record = Button(self.tab1, text="Record...", command=self.record)

        self.lf_train = LabelFrame(self.tab2, text="From Model and Weights")
        self.ent_JSON = Entry(self.lf_train)
        self.btn_JSON = Button(self.lf_train, text="Model...", command=lambda: self.set_text(askopenfilename(),
                                                                                             self.ent_JSON))

        self.ent_weights = Entry(self.lf_train)
        self.btn_weights = Button(self.lf_train, text="Weights...", command=lambda: self.set_text(askopenfilename(),
                                                                                                  self.ent_weights))

        self.btn_train = Button(self.lf_train, text="Train", command=self.train)

        self.model = nn.import_model(DEFAULT_JSON_FILE, DEFAULT_H5_FILE)
        self.prediction = -1

        self.set_text(DEFAULT_JSON_FILE, self.ent_JSON)
        self.set_text(DEFAULT_H5_FILE, self.ent_weights)

    def pack(self):
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible

        self.lf_output.pack()
        self.btn_record.pack()
        self.ent_output.pack()

        self.lf_train.pack()
        self.ent_JSON.grid(row=0, column=0)
        self.btn_JSON.grid(row=0, column=1)

        self.ent_weights.grid(row=1, column=0)
        self.btn_weights.grid(row=1, column=1)

        self.btn_train.grid(row=2, columnspan=2)

    def osx_fix(self):
        # a fix for running on OSX - to center the tab title text vertically
        if self.root.tk.call('tk', 'windowingsystem') == 'aqua':  # only for OSX
            s = ttk.Style()
            # Note: the name is specially for the text in the widgets
            s.configure('TNotebook.Tab', padding=(12, 8, 12, 0))

    def run(self):
        self.osx_fix()
        self.root.mainloop()

    def predict(self):
        self.prediction = nn.predict(self.model, WAVE_OUTPUT_FILENAME)
        self.set_text(self.prediction, self.ent_output)

    def train(self):
        self.model = nn.import_model(self.ent_JSON.get(), self.ent_weights.get())

    def record(self):
        print('Recording...')
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()
        print('Finished Recording')
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        self.predict()

    def set_text(self, text, entry):
        entry.delete(0, END)
        entry.insert(0, text)
        return


win = Tk()
gui = GUI(win)
gui.pack()
gui.run()
