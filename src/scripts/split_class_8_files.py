from pydub import AudioSegment
from datetime import datetime
import os, sys, time

path = os.path.abspath('')
training_set_path = path + '/../../data/training_set'
validation_set_path = path + '/../../data/validation_set'
training_set_class_8_path = path + '/../../data/class_8_files/training_set'
validation_set_class_8_path = path + '/../../data/class_8_files/validation_set'
training_dictionary_path = training_set_path + '/training_dictionary.csv'
validation_dictionary_path = validation_set_path + '/validation_dictionary.csv'

folder_destination = -1
csv_path = ''
audio_files = []
folder_input = ''
csv = ''

def split_audio_and_export(seconds, file_path, file_output_path):
    audio = AudioSegment.from_file(file_path)
    period = seconds * 1000 # Pydub works with milliseconds
    duration = len(audio)
    csv = ''
    slices = int(duration / period) # Get the number of slices (avoid slices duration less than period)
    for i in range(0, slices):
        part = audio[(i * period):((i + 1) * period)] # Get a slice
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        part.export(file_output_path + "/undefined" + date + ".wav", format="wav")
        csv += "undefined" + date + ".wav" + ";" + str(8) + "\n"
        time.sleep(1)
    return csv


while(folder_destination != 0 and folder_destination != 1):
    print("Folder files output (0 -> training set, 1 -> validation_set):")
    folder_destination = int(input())

if(folder_destination == 0):
    audio_files = [f for f in os.listdir(training_set_class_8_path) if f.endswith('.wav')]
    csv_path = training_dictionary_path
    folder_destination = training_set_path
    folder_input = training_set_class_8_path
else:
    audio_files = [f for f in os.listdir(validation_set_class_8_path) if f.endswith('.wav')]
    csv_path = validation_dictionary_path
    folder_destination = validation_set_path
    folder_input = validation_set_class_8_path

for i in audio_files:
    csv += split_audio_and_export(3, folder_input + "/" + i, folder_destination)

f=open(csv_path, "a+")
f.write(csv)
f.close()
