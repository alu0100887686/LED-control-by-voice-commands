import pyaudio
import wave
import os, sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
from datetime import datetime

#n_recording = 1

path = os.path.dirname(__file__)
training_set_path = path + '/../../data/training_set'
validation_set_path = path + '/../../data/validation_set'
dictionary_path = path + '/../../data/dictionary.csv'
folder_destination = -1

while(folder_destination != 0 and folder_destination != 1):
    print("Folder files output (0 -> training set, 1 -> validation_set):")
    folder_destination = int(input())
print("Enter File Prefix: ")
filename = input()
print("Enter Recording Class: ")
type = input()

csv = ""
#os.mkdir("wav")

while(True):
    if(folder_destination == 0):
        file = training_set_path + "/" + filename + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".wav"
    else:
        file = validation_set_path + "/" + filename + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".wav"
    csv += filename + str(n_recording) + ".wav" + ";" + str(type) + "\n"
    n_recording += 1

    print("Recording * " + file)

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



    wf = wave.open(file, 'w')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


    aux = 'a'
    while aux != "" and aux != 'q':
        print("Continue[Enter], Quit[Q]: ")
        aux = input()
    if aux == 'q':
        break;

f=open(dictionary_path, "a+")
f.write(csv)
f.close()
