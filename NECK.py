import Graph_test

def initial(frets,tuning):
    Graph_test.make_graph(frets,len(tuning))
    notes = []
    for i in range(len(tuning)):
        notes.append([])
    f = 0
    for i in range(len(notes)):
        for x in range(f, frets+f):
            notes[i].append(x + tuning[i])
    return notes


if __name__ == '__main__':
    tuning = [65,70,75,80,85]
    frets = 12
    notes = initial(frets,tuning)
    for line in notes:
        print(line)