import mido
import time

def SortingAlgo(song):
    song = sorted(song)
    for i in range(len(song)):
        if i <= len(song)-1 and song[i] == song[i-1]:
            song.remove(song[i])
    return song


def readSong(songName, max):
    cv1 = mido.MidiFile(songName)
    song = []
    stopCheck = 0
    messagesRead = []
    for msg in cv1.tracks[1]:
        if msg.type not in messagesRead:
            messagesRead.append(msg.type)
        if msg.type == 'note_on' and msg.note <= max:
            song.append([msg.time,msg.note])
        else:
            stopCheck+= 1
    if len(song) != stopCheck:
        print(f"Song Reader Invalid\n{len(song)-stopCheck} notes not ended out of {len(song)} messages\nReturning test case song\nMessages Read were:{messagesRead}")
        song = testSong()
    return SortingAlgo(song)

def testSong():
    song = []
    for y in list(range(3*5))[::5]:
        for i in range(0,5):
            for x in [64,71,76]:
                song.append([i+y,i+x+y])
    return song*100

def PySort(song):
    return sorted(song)

def readAll(songL):
    final = []
    for i in songL:
        final.append(i)
    return final

def MergeSort(song):
    #Solution found on Geeks for Geeks
    def merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
    
        # create temp arrays
        L = [0] * (n1)
        R = [0] * (n2)
    
        # Copy data to temp arrays L[] and R[]
        for i in range(0, n1):
            L[i] = arr[l + i]
    
        for j in range(0, n2):
            R[j] = arr[m + 1 + j]
    
        # Merge the temp arrays back into arr[l..r]
        i = 0     # Initial index of first subarray
        j = 0     # Initial index of second subarray
        k = l     # Initial index of merged subarray
    
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
    
        # Copy the remaining elements of L[], if there
        # are any
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
    
        # Copy the remaining elements of R[], if there
        # are any
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
    
    # l is for left index and r is right index of the
    # sub-array of arr to be sorted
    
 
    def mergeSort(arr, l, r):
        if l < r:
 
            # Same as (l+r)//2, but avoids overflow for
            # large l and h
            m = l+(r-l)//2
    
            # Sort first and second halves
            mergeSort(arr, l, m)
            mergeSort(arr, m+1, r)
            merge(arr, l, m, r)
    mergeSort(song, 0, len(song)-1)
    return song
    
    


def BubbleSort(song):
    n = len(song)
    for i in range(n):
        sorted = True
        for j in range(0, n-i-1):
            if song[j] > song[j+1]:
                song[j], song[j+1] = song[j+1], song[j]
                sorted = False
        if sorted == True:
            return song
    return song

def InsertionSort(song):
    n = len(song)
    if n <= 1:
        return

    for i in range(1, n):
        key = song[i]
        j = i - 1

        while j >= 0 and key < song[j]:
            song[j + 1] = song[j]
            j -= 1

        song[j + 1] = key
    return song


MINIMUM= 32
 
def find_minrun(n): 
 
    r = 0
    while n >= MINIMUM: 
        r |= n & 1
        n >>= 1
    return n + r 
 
def insertion_sort(array, left, right): 
    for i in range(left+1,right+1):
        element = array[i]
        j = i-1
        while element<array[j] and j>=left :
            array[j+1] = array[j]
            j -= 1
        array[j+1] = element
    return array
             
def merge(array, l, m, r): 
 
    array_length1= m - l + 1
    array_length2 = r - m 
    left = []
    right = []
    for i in range(0, array_length1): 
        left.append(array[l + i]) 
    for i in range(0, array_length2): 
        right.append(array[m + 1 + i]) 
 
    i=0
    j=0
    k=l
  
    while j < array_length2 and  i < array_length1: 
        if left[i] <= right[j]: 
            array[k] = left[i] 
            i += 1
 
        else: 
            array[k] = right[j] 
            j += 1
 
        k += 1
 
    while i < array_length1: 
        array[k] = left[i] 
        k += 1
        i += 1
 
    while j < array_length2: 
        array[k] = right[j] 
        k += 1
        j += 1
 
def tim_sort(array): 
    n = len(array) 
    minrun = find_minrun(n) 
 
    for start in range(0, n, minrun): 
        end = min(start + minrun - 1, n - 1) 
        insertion_sort(array, start, end) 
  
    size = minrun 
    while size < n: 
 
        for left in range(0, n, 2 * size): 
 
            mid = min(n - 1, left + size - 1) 
            right = min((left + 2 * size - 1), (n - 1)) 
            merge(array, left, mid, right) 
 
        size = 2 * size 
 
 
 
   

def SortingAlgoTest(song):
    allAlgos = [readAll,PySort,MergeSort,BubbleSort,InsertionSort, tim_sort]
    trueSorted = sorted(song)
    for algorithm in allAlgos:
        start = time.perf_counter_ns()
        testSorted = algorithm(song)
        if testSorted == trueSorted:
            success = True
        else:
            success = False
        end = time.perf_counter_ns()
        timeToComplete = end-start
        print(f'time = {timeToComplete}, {algorithm},sorted = {success}')

import random
if __name__ == "__main__":
    songName =  "MIDI_files/Sigmas Theme MIDI.mid"
    max = 100
    song = readSong(songName,max)
    # random.shuffle(song)
    for note in song:
        print(note)
    SortingAlgoTest(song)
