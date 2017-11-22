import pyaudio
import wave
import os, sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3

n_recording = 1

print("Enter File Prefix: ")
filename = input()
print("Enter Recording Class: ")
type = input()

csv = ""
os.mkdir("wav")

while(True):

    file = "wav/" + filename + str(n_recording) + ".wav"
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

f=open("TrainingFiles.csv", "a+")
f.write(csv)
f.close()

