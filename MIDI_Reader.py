import subprocess
from subprocess import STDOUT, PIPE
import time

def run_java (java_file):
    subprocess.check_call(['javac', java_file])
    cmd=['java', java_file]
    subprocess.Popen(cmd, stdout = PIPE, stderr = STDOUT)

errors = [0,0]
def readSong(songName, max, min):
    global errors
    errors =[0,0]

    with open('javaBridge.txt', 'w') as file:
        file.write(songName)
    
    with open('MIDI_Unpacked.txt', 'w') as file:
        file.write('none')

    run_java("MIDI_Reader_Java.java")

    while True:
        with open('MIDI_Unpacked.txt', 'r') as file:
            line = file.readline()
        if len(line)>4:
            break


    with open('MIDI_Unpacked.txt', 'r') as file:
        try:
            channels = []
            song = [0,0]
            line = file.readline()
            while len(line) >= 1:
                if line.startswith('channel'):
                    channels.append(song)
                    song = [[0,0]]
                else:
                    note = list(map(int,line.strip().split(',')))
                    note[0] = int(note[0]/100)
                    if note [-1] <= max and note[-1] >=min:
                        song.append(note)
                    elif note[-1] < min:
                        song[0][0]+=1
                    elif note[-1] > max:
                        song[0][1]+=1
                line = file.readline()
        except:
            if len(song) == 0:
                print('song not read')
    channels.append(song)
    channels = channels[1:]
    return channels

    

if __name__ == '__main__':

    song = readSong('MIDI_files/Sigmas Theme MIDI.mid', 200, 0)
    # song = readSong('MIDI_files/cello-C-chord.mid', 200, 0)
    print(len(song))