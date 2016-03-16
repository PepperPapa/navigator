# !usr/bin/python3.4

from tkinter import *
from tkinter import filedialog

class Nav():
    def __init__(self, root):
        toolsFm = Frame(root, bg="#dddddd", height=30)
        toolsFm.pack(side="top", fill="x")

        pane = PanedWindow(root, orient=VERTICAL)
        pane.add(self.makeOutputText(pane))
        pane.add(self.makeInputText(pane))
        pane.pack(side="top", expand=YES, fill=BOTH)

        statusFm = Frame(root, bg="#dddddd", height=30)
        statusFm.pack(side="bottom", fill="x")

    def makeInputText(self, root):
        inputFm = Frame(root)
        self.inputText = Text(inputFm, height=10, relief=GROOVE)
        inputScrollbar = Scrollbar(inputFm, orient=VERTICAL)
        self.inputText.pack(side="left", fill=BOTH, expand=YES)
        inputScrollbar.pack(side="left", fill=Y)
        self.inputText.config(yscrollcommand=inputScrollbar.set)
        inputScrollbar.config(command=self.inputText.yview)
        return inputFm

    def makeOutputText(self, root):
        outputFm = Frame(root)
        self.outputText = Text(outputFm, height=20, relief=FLAT)
        outputScrollbar = Scrollbar(outputFm, orient=VERTICAL)
        self.outputText.pack(side="left", fill=BOTH, expand=YES)
        outputScrollbar.pack(side="left", fill=Y)
        self.outputText.config(yscrollcommand=outputScrollbar.set)
        outputScrollbar.config(command=self.outputText.yview)
        return outputFm

root = Tk()
root.title("navigator")
Nav(root)
mainloop()
