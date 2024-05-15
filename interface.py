import NECK
import MIDI_Reader
import TAB_Maker


import customtkinter as ctk
from customtkinter import filedialog

class Setting():
    def __init__(self) -> None:
        while True:
            try:
                with open("settings.txt", 'r') as f:
                    self.tuning = list(map(int, f.readline().strip("Tuning:[]\n").split(",")))
                    self.frets = int(f.readline().strip("Frets:[]"))
                    break
            except:
                with open("settings.txt", 'w') as f:
                    lines = ["Tuning:64,69,74,79,83\n","Frets:20\n","Strings:6"]
                    f.writelines(lines)
        self.numMode = True

    def writeToFile(self):
        with open("settings.txt", 'w') as f:
                lines = [str(self.tuning)+'\n',str(self.frets)+'\n']
                f.writelines(lines)
        print("saved")

settings = Setting()

    





import tkinter as tk
from tkinter import ttk
  
 
LARGEFONT =("Verdana", 35)
LABELTEXT = ("Arial", 18)
BUTTONLABEL = ("arial", 10)
VALUEFONT = ("Arial", 18)
ARROWFONT = ('Arial', 18)
PLUSMINUSFONT = ('Arial', 20)
INFOTEXT = ('Arial',10)
TUNINGBUTTONW = 10
STRINGUPDOWNW = 10
FRETBUTTONW = 10

notesOutOfRange = [0,0]


class tkinterApp(ctk.CTk):

    def __init__(self, *args, **kwargs): 
        ctk.CTk.__init__(self, *args, **kwargs)

        self.title = 'MIDI to TAB'

        container = ctk.CTkFrame(self)
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {}  
  
        for F in (StartPage, settingsPage, ChannelsPage):
  
            frame = F(container, self)
  
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        self.geometry("800x500")
        self.show_frame(StartPage)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
# first window frame startpage
  
class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller): 
        ctk.CTkFrame.__init__(self, parent)

        label = ctk.CTkLabel(self, text="MIDI To TAB Converter", font=("Comic",40))
        label.pack(padx=10, pady= 50)

        def make_Tab():
            controller.show_frame(ChannelsPage)

        TabBtn = ctk.CTkButton(self, text="Make Tab", font=BUTTONLABEL, command=make_Tab)
        TabBtn.pack(padx=10, pady=2)

        settingsPageBtn = ctk.CTkButton(self, text="Settings Page", font=BUTTONLABEL, command=lambda : controller.show_frame(settingsPage))
        settingsPageBtn.pack(padx=10, pady=2)

        QuitBtn = ctk.CTkButton(self, text="Quit", font=BUTTONLABEL, command=quit)
        QuitBtn.pack(padx=10, pady=2) 
  
  
# Second window frame settingsPage
class settingsPage(ctk.CTkFrame): 
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Settings Page", font = LARGEFONT)
        label.pack(pady=10)

        tuningText  = ctk.CTkLabel(self, text="Change Tuning", font=LABELTEXT)
        tuningText.pack()



        def stringUpL():
            if len(settings.tuning) < 8:
                settings.tuning = [settings.tuning[0]-5] + settings.tuning
                tuningFrameReset()
        
        def stringDownL():
            if len(settings.tuning) > 1:
                settings.tuning = settings.tuning[1:]
                tuningFrameReset()
        
        def stringUpR():
            if len(settings.tuning) < 8:
                settings.tuning += [settings.tuning[-1]+5]
                tuningFrameReset()

        def stringDownR():
            if len(settings.tuning) > 1:
                settings.tuning = settings.tuning[:-1]
                tuningFrameReset()

        StringsFrame = ctk.CTkFrame(self)


        stringNumFrameL = ctk.CTkFrame(StringsFrame)
        stringUpBtnL = ctk.CTkButton(stringNumFrameL, width=STRINGUPDOWNW, text="+", font=PLUSMINUSFONT, command=stringUpL)
        stringUpBtnL.grid(row=0,column = 0)

        stringDownBtnL = ctk.CTkButton(stringNumFrameL, width=STRINGUPDOWNW, text="-", font=PLUSMINUSFONT, command=stringDownL)
        stringDownBtnL.grid(row=1,column = 0)

        stringNumFrameL.grid(row=0, column=0)

        stringNumFrameR = ctk.CTkFrame(StringsFrame)
        stringUpBtnR = ctk.CTkButton(stringNumFrameR, width=STRINGUPDOWNW, text="+", font=PLUSMINUSFONT, command=stringUpR)
        stringUpBtnR.grid(row=0,column = 0)

        stringDownBtn = ctk.CTkButton(stringNumFrameR, width=STRINGUPDOWNW, text="-", font=PLUSMINUSFONT, command=stringDownR)
        stringDownBtn.grid(row=1,column = 0)

        stringNumFrameR.grid(row=0,column=2)

        tuningFrame = ctk.CTkFrame(StringsFrame)


        
        upButtons = []
        vals = []
        downButtons = []

        def tuningFrameReset():
            upButtons.clear()
            downButtons.clear()
            vals.clear()
            for element in tuningFrame.winfo_children():
                element.destroy()
            addTuningButtons(0, settings.tuning)

        def addToTuning(i):
            settings.tuning[i] += 1
            vals[i].configure(text=str(settings.tuning[i]))
            tuningFrameReset()

        def subToTuning(i):
            settings.tuning[i] -= 1
            vals[i].configure(text=str(settings.tuning[i]))
            tuningFrameReset()
        

        def addTuningButtons(i, val):
            if i == len(val):
                return True
            else:
                if settings.numMode:
                    textLabel = val[i]
                else:
                    textLabel = noteToName(val[i])
                upButtons.append(ctk.CTkButton(tuningFrame, width=TUNINGBUTTONW, text='▲', font=ARROWFONT, command=lambda : addToTuning(i)))
                upButtons[-1].grid(row=0, column=i)

                vals.append(ctk.CTkLabel(tuningFrame, text=str(textLabel), font=VALUEFONT))
                vals[-1].grid(row=1, column=i)

                downButtons.append(ctk.CTkButton(tuningFrame, width=TUNINGBUTTONW, text='▼', font=ARROWFONT, command=lambda : subToTuning(i)))
                downButtons[-1].grid(row=2, column=i)
                addTuningButtons(i+1,val)
            
        addTuningButtons(0, settings.tuning)
        tuningFrame.grid(row=0, column=1)

        StringsFrame.pack()

        def toggleNoteName():
            settings.numMode = not settings.numMode
            tuningFrameReset()

                

        toggleNum = ctk.CTkButton(self, text='Toggle Note Name', command= toggleNoteName)
        toggleNum.pack(pady=5)


        fretLabel = ctk.CTkLabel(self, text="Change Number of Frets", font=LABELTEXT)
        fretLabel.pack(pady=10)

        fretFrame = ctk.CTkFrame(self)


        def subToFret():
            settings.frets-=1
            fretNum.config(text=str(settings.frets))
        
        def addToFret():
            settings.frets +=1
            fretNum.config(text=str(settings.frets))


        decreaceBtn = ctk.CTkButton(fretFrame, width=FRETBUTTONW, text="◄", font=ARROWFONT, command=subToFret)
        decreaceBtn.grid(row=0, column = 0)

        fretNum = ctk.CTkLabel(fretFrame, text=str(settings.frets), font=VALUEFONT)
        fretNum.grid(row=0,column=2)

        increaceBtn = ctk.CTkButton(fretFrame, width=FRETBUTTONW, text="►", font=ARROWFONT, command=addToFret)
        increaceBtn.grid(row=0,column=3)

        fretFrame.pack(pady=10)
        

        saveBtn = ctk.CTkButton(self, text ="Save",command = settings.writeToFile)
        saveBtn.pack()

        homeBtn = ctk.CTkButton(self, text ="Home",command = lambda : controller.show_frame(StartPage))
        homeBtn.pack(pady = 10)


        infoText = ctk.CTkLabel(self, text='Standard Guitar Tuning = [64,69,74,79,83,88]\nStandard Bass Tuning = [52,57,62,67]', font=INFOTEXT, anchor='se')
        infoText.pack()

class ChannelsPage(ctk.CTkFrame):
    def __init__(self, parent, controller): 
        ctk.CTkFrame.__init__(self, parent)

        def reset():
            for element in channelFrame.winfo_children():
                element.destroy
            controller.show_frame(StartPage)


        self.channels = []

        channelFrame = ctk.CTkFrame(self)
        placeholder = ctk.CTkLabel(channelFrame, text="No song loaded yet", font=INFOTEXT)
        placeholder.grid(row=0,column= 0)

        label = ctk.CTkLabel(self, text="Load song", font=LARGEFONT)
        label.pack(padx=10, pady= 50)

        def chooseChannel(ind):
            global notesOutOfRange
            notesOutOfRange = self.channels[ind].pop(0)
            tab = TAB_Maker.MakeTAB(self.channels[ind], self.neck)
            format(tab, self.filename)
            reset()

        def addChannelButtons(columnNum, i, channels):
            if i == 0:
                label = ctk.CTkLabel(channelFrame, text=f"Select channel:\n", font=LARGEFONT)
                span= len(channels)//4
                if span != 0:
                    label.grid(row=0, column=0,columnspan =span)
                else:
                    label.grid(row=0, column=0)
            if i == len(channels):
                return True
            else:
                rowN = i%4
                btn = ctk.CTkButton(channelFrame, text=f'Channel {i+1}', font=('Arial', 10), command=lambda:chooseChannel(i-1))
                btn.grid(row=rowN+1, column=columnNum)
                i+=1
                if i%4 == 0:
                    columnNum += 1
            addChannelButtons(columnNum, i, self.channels)

        def chooseFile():
            self.filename = filedialog.askopenfilename(
                                                title='select file', 
                                                filetypes=(("MIDI files","*.mid*"), ("all files","*.*")))
            
            self.neck = NECK.initial(settings.frets, settings.tuning)
            max = self.neck[-1][-1]
            min = self.neck[0][0]
            self.channels = MIDI_Reader.readSong(self.filename, max, min)
            for element in channelFrame.winfo_children():
                element.destroy()
            addChannelButtons(0,0,self.channels)

            
        if len(self.channels) > 0:
            addChannelButtons(0, 0,self.channels)

        btn = ctk.CTkButton(self, text="Click to Load New Song", font=BUTTONLABEL, command=chooseFile)
        btn.pack()

        channelFrame.pack(pady = 10)

        homeBtn = ctk.CTkButton(self, text ="Home",font=BUTTONLABEL, command = lambda : controller.show_frame(StartPage))
        homeBtn.pack(pady = 2)

        QuitBtn = ctk.CTkButton(self, text="Quit", font=BUTTONLABEL, command=quit)
        QuitBtn.pack(padx=10, pady=2) 
  

def noteToName(num):
        noteNames = ["C ","C#","D ", "D#", "E ", "F ", "F#", "G ", "G#","A ","A#","B "]
        return noteNames[int(num)%12]


def format(timeTAB, filename):
    
    formattedTab = []

    def addChunk():

        strings = []

        for i in settings.tuning:
            strings.append(noteToName(i)+'|---')

        formattedTab.append(strings)

    addChunk()
    
    if timeTAB != None:
        
        time = timeTAB[0][0][-1]
        for notes in timeTAB:
            if notes[0][-1] != time:
                gapFill = '-'
                if notes[0][-1]-time <10:
                    gapFill*= notes[0][-1]-time
                else:
                    gapFill*=10
                for line in range(len(formattedTab[-1])):
                    formattedTab[-1][line]+=gapFill
                time = notes[0][-1]
            visited = []
            for place in notes:
                visited.append(place[0])
                strFret = str(place[1])
                if len(strFret) == 1:
                    strFret+='-'
                formattedTab[-1][place[0]]+= strFret
            for line in range(len(formattedTab[-1])):
                formattedTab[-1][line]+='-'
                if not line in visited:
                    formattedTab[-1][line]+='--'
            if len(formattedTab[-1][0]) >= 100:
                addChunk()
    else:
        formattedTab[-1][len(settings.tuning)//2]+=" TAB not possible due to no valid notes"
        
    filename = filename.removesuffix('.mid')
    ind =  filename.rfind('/')
    TabFileName = 'OutputTABs/'+filename[ind+1:]+'_TAB.txt'
    print("\n\nSaved to OutputTABs/",TabFileName,'\n\n')

    global notesOutOfRange
    TABerror = TAB_Maker.notesExcluded


    with open(TabFileName,'w') as file:
        if notesOutOfRange[1]>0:
            file.write(f'{notesOutOfRange[1]} notes were above range\n')
        if notesOutOfRange[0]>0:
            file.write(f'{notesOutOfRange[0]} notes were below range\n')
        if TABerror > 0:
            file.write(f'{TABerror} notes were excluded due to impossible combinations\n')

        for string in formattedTab:
            for line in string[::-1]:
                file.write(str(line)+'\n')

            file.write('\n\n')

        
  
# Driver Code
app = tkinterApp()
app.mainloop()
