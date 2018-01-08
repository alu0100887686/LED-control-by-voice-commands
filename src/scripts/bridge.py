#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import serial, sys, re, binascii
import serial.tools.list_ports
from scipy.io.wavfile import read
import nn
import pyaudio
import wave
from array import array
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "input.wav"

def getSerialPort():
    r = ""
    if sys.platform.startswith('linux2'): # Linux serial port
        r = re.compile("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith('win32'): # Windows serial port
        r = re.compile("COM[A-Za-z0-9]*")
    elif sys.platform.startswith('darwin'): # Mac Osx serial port
        r = re.compile("/dev/cu.usbmodem[A-Za-z0-9]*")
    list = serial.tools.list_ports.comports()
    enable = []
    usable = []
    for i in list:
        enable.append(i.device)
    for i in filter(r.match, enable):
        usable.append(i)
    return usable[0]

print (getSerialPort())
arduino = serial.Serial(getSerialPort(), 9600)

model = nn.import_model()

while(True):
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

    samprate, wavdata = read(WAVE_OUTPUT_FILENAME)
    chunks = np.array_split(wavdata, CHUNK)
    dbs = 20*np.log10(np.amax(chunks))
    #maxdb = dbs
    print(dbs)
    if dbs > 80:
        option = str(nn.predict(model, WAVE_OUTPUT_FILENAME))
        arduino.write(option.encode())

"""
option = "1"
while(option != "0" ):
    option = str(input('Enter your input: '))
    arduino.write(option.encode())
"""

arduino.close()
