import MIDI_Reader
import NECK
import Graph_test
import itertools


notesExcluded = 0
def MakeTAB(song, neck):
    if len(song) == 0:
        return None
    global notesExcluded
    notesExcluded = 0
    tab = []
    potentialPlace = []
    currentTime = song[0][0]
    timedNotes = []
    for note in song:
        notePlace = []
        for string in range(len(neck)):
            try:
                fret = neck[string].index(note[1])
                notePlace.append([string, fret, note[0]]) #Each item in temp has string, fret, and time
            except:
                pass
        if note[0] == currentTime:
            timedNotes.append(notePlace)
        else:
            potentialPlace.append(timedNotes)
            currentTime = note[0]
            timedNotes = [notePlace]
    potentialPlace.append(timedNotes)
    #Make a list of lists of all the places a note can be played

    cart = list(itertools.product(*potentialPlace[0]))
    bestCombo, bestWeight = findBestCombo(cart, tab)
    if bestCombo == ['NA']:
        bestCombo = [[i,'/',note[0]] for i in range(len(neck))]
    tab.append(bestCombo)
    
    if bestWeight >=99999:
        print("ComboNotPossible")

    for timeFrame in potentialPlace[1:]:
        cart= list(itertools.product(*timeFrame))
        locked = tab[-1]
        bestCombo, bestWeight = findBestCombo(cart,locked)
        if bestCombo == ['NA']:
            bestCombo = [[i,'/',note[0]] for i in range(len(neck))]
        if bestWeight >=99999:
            print("ComboNotPossible")
        tab.append(bestCombo)
    if notesExcluded !=0:
        print(f'{notesExcluded} notes were removed due to impossible combinations')
    return tab

def findBestCombo(cart,locked):
    global notesExcluded
    bestWeight = 99999
    bestCombo = ['NA']
    for places in cart:
        places = list(places)
        visited = []
        collision = False
        for note in places:
            if note[0] in visited:
                collision = True
            visited.append(note[0])
        if not collision:
            fullFrame = places+locked
            n = len(fullFrame)
            pairs = []
            for i in range(n):
                for x in range(n):
                    pairs.append([fullFrame[i][:2], fullFrame[x][:2]])
            weight = 0
            for combo in pairs:
                weight+= Graph_test.findWeight(str(combo[0]),str(combo[1]))
            if weight <= bestWeight:
                bestWeight = weight
                bestCombo = places
        else:
            weight = 9999
    if bestCombo == ['NA']:
        cartR = list(map(lambda x: x[1:], cart))
        notesExcluded+=1
        bestCombo, bestWeight = findBestCombo(cartR, locked)
    return bestCombo, bestWeight

#Test case
if __name__ == '__main__':
    songName = 'Sigmas Theme MIDI.mid' 
    neck = NECK.initial(12, [64,69,74,79,83])
    max = neck[-1][-1]
    song = MIDI_Reader.readSong('MIDI_files/TestSong.mid', max, neck[0][0])[0]
    Graph_test.make_graph(12, 6)
    fullTAB = MakeTAB(song, neck)
    print(fullTAB)
    # import TAB_Format
    # TAB_Format.format(fullTAB, 'chord.mid')











    
# def format(tab):

#     timeTAB = []
#     try:
#         for i in range(len(tab)):
#             timeTAB.append([song[i][0],tab[i]])
#     except:
#         pass



#     strings = [[],[],[],[],[],[]]
#     time = 0
#     tempAdded = []
#     for current in timeTAB:
#         if current[0] == time:
#             strings[current[1][0]].append([current[1][1]])
#             if current[1][0] in tempAdded:
#                 print(current,'+',tempAdded)
#             tempAdded.append(current[1][0])
#         else:
#             for x in range(len(strings)):
#                 if x not in tempAdded:
#                     strings[x].append('-')
#             time+=1
#             tempAdded = []

#     for i in range(len(strings)):
#         if len(strings[i]) != len(strings[i-1]):
#             print("leng of strings don't match")

#     with open('TAB output.txt','w') as file:
#         for line in strings:
#             file.write(str(line)+'\n')