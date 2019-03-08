#!/usr/bin/env python

from sys import stdin
from time import time
from random import shuffle, choice
from csv import writer,QUOTE_MINIMAL
import tkinter
from winsound import PlaySound, SND_ASYNC
from tkinter.messagebox import askokcancel
from tkinter.constants import PAGES, UNITS, NORMAL, RAISED, SUNKEN, HORIZONTAL, RIGHT, BOTH, LEFT, BOTTOM, TOP, NW, HIDDEN, X, Y, ALL, CENTER,END
from EXDAT import *



class MainFrame(tkinter.Frame):
    def __init__(self, master, *scripts, **opts):
        
        tkinter.Frame.__init__(self, master, **opts)
        master.title("Han Shot First")

        self.scripts = list(scripts)
        self.opts = {}

        self.display_var = tkinter.StringVar("")
        width = master.winfo_screenwidth()
        self.display = tkinter.Message(self, justify = LEFT, textvar = self.display_var, bg = "light grey", font = (FontName, FontSize1), width = 0.8*width)
        self.display.pack(fill=BOTH, expand=1, padx = 10, pady = 15)


        self.next_button = tkinter.Button(master, text="", font=(FontName, FontSize1), fg = "black", disabledforeground= "red", command = self.Next_Session)
        self.next_button.pack(side = BOTTOM, expand = 0, padx = 5, pady = 10)

        self.remaining = 0

        self.Next_Session()

    def Next_Session(self):
        if self.scripts:
            self.scripts[0].next(self,**self.opts)

    def Next_Script(self, **opts):
        self.opts.update(opts)
        self.scripts.pop(0)

    def set_text(self, text, justify = None, font = None):
        if justify:
            self.display["justify"] = justify
        if font:
            self.display["font"] = font
        self.display_var.set(text)

    def play(self, audio):
        PlaySound(audio, SND_ASYNC)

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining < 0:
            self.Next_Session()
        else:
            self.next_button.configure(text="%03d" % self.remaining, state = tkinter.DISABLED)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)


class Text(object):
    
    def __init__(self, text, align=LEFT, font = (FontName, FontSize1), fg = "black"):
        self.text = text
        self.align = align
        self.font = font
        
    
    def next(self, frame, **opts):
        frame.set_text(self.text, self.align, self.font)
        frame.next_button.configure(text="Next", state = tkinter.NORMAL, fg = "black")
        frame.play(None)
        frame.Next_Script()

class ReadingSpeed(object):
    
    def __init__(self, filename):
        
        self.text = open(filename).read()
        self.time1 = 0
        self.time2 = 0

        self.next = self.SpeedMeasure

    def SpeedMeasure(self,frame, **opts):
        frame.set_text(self.text, LEFT, ExpFont)
        frame.next_button.configure(text="Done", state = tkinter.NORMAL, fg = "red")
        self.time1 = time()
        self.next = self.SpeedStore

    def SpeedStore(self, frame, **opts):
        self.time2 = time()
        global RT
        RT = self.time2 - self.time1
        frame.set_text("""You took %d seconds to read this passage.\nClick "Next" to continue...""" % RT, CENTER, (FontName, FontSize1))
        frame.next_button.configure(text="Next", state = tkinter.NORMAL, fg = "black")
        frame.Next_Script()
        self.next = lambda s,**o:None

class ReadingComp(object):
    """ Main reading comprehension test.
    """
    def __init__(self, textname, audioname):
        
        in_file = open(textname).read()
        self.text = in_file.split('=')[0]
        self.audio = audioname

    def next(self, frame, **opts):
        frame.set_text(self.text, LEFT, ExpFont)
        frame.play(self.audio)
        frame.countdown(ReadingTime)
        frame.Next_Script()


class ReadingQues1(object):
    """ Main reading comprehension test.
    """
    def __init__(self, textname):
        
        in_file = open(textname).read()
        self.text = in_file.split('=')[1]

    def next(self, frame, **opts):
        frame.set_text(self.text, LEFT, (FontName, FontSize2))
        frame.play(None)
        frame.countdown(ResponseTime)
        frame.Next_Script()

class ReadingQues2(object):
    """ Main reading comprehension test.
    """
    def __init__(self, textname):
        
        in_file = open(textname).read()
        self.text = in_file.split('=')[2]

    def next(self, frame, **opts):
        frame.set_text(self.text, LEFT, (FontName, FontSize2))
        frame.play(None)
        frame.countdown(ResponseTime)
        frame.Next_Script()

class GoodbyeScript(object):
    """ The end.
    """

    def next(self, frame, **opts):
        frame.next_button.pack_forget()
        tkinter.Button(root, text = "Click This to Quit the Program", fg ='red', font = (FontName, FontSize1), command = AskIfQuit).pack(side = BOTTOM, expand = 0, padx = 5, pady = 10)                
        frame.set_text("This is the end of the test. The researcher will be available for any question you have.\nThank you very much for participating! Goodbye!")
        
# Quit the test at any time by calling this function.
def AskIfQuit():
    if askokcancel("Quit", "Do you wish to quit the test?"):
        PlaySound(None,SND_ASYNC)
        root.destroy()

def request_subject_id():
    """Prompt the user to enter a subject ID and check if the input conforms with the required format.  If not ask again.
    """
    print("Please enter a subject id: ")
    sid = stdin.readline()[:-1]
    return sid


#request_subject_id()

ID = request_subject_id()
shuffle(RCList)
shuffle(AList)
ExpFont = choice(Groups)



with open('IDSummary.csv', 'a') as IDSummary:
    grouping = writer(IDSummary,delimiter=',')
    grouping.writerow([ID] + [ExpFont[0]] + [RCList[0][0]] + [AList[0][0]])
    grouping.writerow([ID] + [ExpFont[0]] + [RCList[1][0]] + [AList[1][0]])
    grouping.writerow([ID] + [ExpFont[0]] + [RCList[2][0]] + [AList[2][0]])

IDSummary.close()


# Root window created
root = tkinter.Tk()
root.attributes('-fullscreen', True)
# Make it cover the entire screen:
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
root.protocol("WM_DELETE_WINDOW", AskIfQuit)

Experiment = MainFrame(
    root, 
    Text(WelcomeText),
    Text(Ins_0),
    Text(Ins_1_0),
    ReadingSpeed(RSF),
    Text(Ins_1_1),
    Text(Ins_2_0),
    Text(Ins_2_1),
    Text(Ins_2_2),
    ReadingComp(RCList[0][1], AList[0][1]), 
    Text(Ins_3),
    ReadingQues1(RCList[0][1]), 
    ReadingQues2(RCList[0][1]),
    Text(Ins_2_2),
    ReadingComp(RCList[1][1], AList[1][1]),
    Text(Ins_3),
    ReadingQues1(RCList[1][1]),
    ReadingQues2(RCList[1][1]),
    Text(Ins_2_2),
    ReadingComp(RCList[2][1], AList[2][1]), 
    Text(Ins_3),
    ReadingQues1(RCList[2][1]),
    ReadingQues2(RCList[2][1]),
    GoodbyeScript())
Experiment.pack(fill = BOTH, expand = 1)
root.mainloop()


with open('ReadingSpeed.csv', 'a') as RS:
    speed = writer(RS,delimiter=',')
    speed.writerow([ID] + [RT])

RS.close()
