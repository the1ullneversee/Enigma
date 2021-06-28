from os import name
import tkinter as tk
from tkinter import ttk
from tkinter.constants import FLAT, RAISED, SUNKEN
#init the window we will use to pin the widgets


borderEffects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE
}

alphabet = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]

btn_selected = "yellow"
btn_unselected = "grey"

class RotorGUI():
    def __init__(self,rButton,rsInput, spInput, inFunction, decFunction, type):
        self.rButton = rButton
        self.rsInput = rsInput
        self.spInput = spInput
        self.inFunction = inFunction
        self.decFunction = decFunction
        self.type = type

class GUI():
    keysToLamps = {}
    supportedReflectors = ["A","B","C"]
    supportedRotors = [ "I","II", "III", "IV", "V","VI","VII","VIII", "Beta", "Gamma"]
    selectedReflector = supportedReflectors[0]
    selectedRotors = []
    ringSettings = [0,0,0]
    startingPositions = ["A","A","A"]
    rotors = 3

    rotor1 = tk.Button()
    rotor2 = tk.Button()
    rotor3 = tk.Button()
    rotor4 = tk.Button()

    def choice(self,rotor,newRotor):
        pop.destroy()
        rg = self.selectedRotors[rotor]
        rg.rButton.config(text=newRotor)
        """
        f = tk.Frame(self.window, name="foo")
        b1 = tk.Button(f, name="b1")
        tk.Button.config("refChoice",text=ref)
        """
        tk.win.destroy()

    def click_fun(self,rotor):
        global pop
        pop = tk.Toplevel(self.window)
        pop.title("Confirmation")
        pop.geometry("300x150")
        pop.config(bg="white")
        # Create a Label Text
        label = tk.Label(pop, text="Choose new Rotor",
        font=('Aerial', 12))
        label.pack(pady=20)
        # Add a Frame
        frame = tk.Frame(pop, bg="gray71")
        frame.pack(pady=10)
        # Add Button for making selection
        for rotorSupp in self.supportedRotors:
            button1 = tk.Button(frame, text=rotorSupp, command=lambda: self.choice(rotor,rotorSupp), bg="blue", fg="white")
            button1.grid(row=0, column=1)
        #button2 = tk.Button(frame, text="No", command=lambda: choice("no"), bg="blue", fg="white")
        #button2.grid(row=0, column=2)
    
    def ChangeReflector(self,reflector):
        global pop
        pop = tk.Toplevel(self.window)
        pop.title("Confirmation")
        pop.geometry("300x150")
        pop.config(bg="white")
        # Create a Label Text
        label = tk.Label(pop, text="Would You like to Proceed?",
        font=('Aerial', 12))
        label.pack(pady=20)
        # Add a Frame
        frame = tk.Frame(pop, bg="gray71")
        frame.pack(pady=10)
        # Add Button for making selection
        for ref in self.supportedReflectors:
            button1 = tk.Button(frame, text=ref, command=lambda: self.choice(ref), bg="blue", fg="white")
            button1.grid(row=0, column=0+1)

    def DrawRotors(self, targetFrame):
        targetFrame.columnconfigure([0,1,2,3], minsize=50)
        
        frame = tk.Frame(master=targetFrame,
                                relief=FLAT,
                                background="green",
                                borderwidth=1)
        frame.grid(row=0,column=0,padx=5,pady=5)
        button = tk.Button(master=frame,text="Add")
        button.pack(padx=1,pady=1)
        """
        frame = tk.Frame(master=targetFrame,
                                relief=FLAT,
                                background="green",
                                borderwidth=1)
        frame.grid(row=0,column=1,padx=5,pady=5)
        """
        rotorLabel = tk.Button(master=frame,name="refChoice", text=self.selectedReflector,command=lambda: self.ChangeReflector(self.selectedReflector))
        rotorLabel.pack(padx=0,pady=5)
        btnPlus = tk.Button(master=frame,text="+")
        btnPlus.pack(padx=1,pady=1)
        label = tk.Label(master=frame,text=alphabet[0])
        label.pack(padx=1,pady=1)
        btnMinus = tk.Button(master=frame,text="-")
        btnMinus.pack(padx=1,pady=1)
        x = 0
        for i in range(2,5):
            frame = tk.Frame(master=targetFrame,
                                relief=FLAT,
                                background="white",
                                borderwidth=1)
            frame.grid(row=0,column=i,padx=5,pady=5)
            rotorName = self.supportedRotors[x]
            rotorLabel = tk.Button(master=frame, text=rotorName, command=lambda: self.click_fun(rotorName))
            rotorLabel.pack(padx=0,pady=5)
            btnPlus = tk.Button(master=frame,text="+")
            btnPlus.pack(padx=1,pady=1)
            label = tk.Label(master=frame,text=self.startingPositions[x])
            label.pack(padx=1,pady=1)
            btnMinus = tk.Button(master=frame,text="-")
            btnMinus.pack(padx=1,pady=1)
            rsFrame = tk.Frame(master=frame)
            rsL = tk.Label(master=rsFrame, text="Ring Setting: ")
            rsL.pack(padx=5)
            rs = tk.Entry(master=rsFrame)
            rs.insert(0, self.ringSettings[x])
            rs.pack(padx=1,pady=1)
            rsFrame.pack()
            rg = RotorGUI(rotorLabel,label,rs,None,None,"rotor")
            self.selectedRotors.append(rg)
            x += 1

    def HighlightLamp(self, value):
        print(value)
        existing = self.inputLabel["text"]
        self.inputLabel.configure(text=existing + value + " ")
        widget = self.keysToLamps[value]
        widget[0].config(bg=btn_selected)
        button = tk.Button(widget[0])
        button.after(500,lambda: self.ResetLamp(value))
        print(widget)

    def DrawLamps(self, targetFrame):
        i = 0
        row = 0
        col = 0
        max = 9

        for i in range(0,26):
            if row == 1:
                max = 8
            else:
                max = 9
            if col >= max:
                row += 1
                col = 0
            frame = tk.Frame(master=targetFrame,
                            relief=SUNKEN,
                            background="black",
                            borderwidth=1)
            
            frame.grid(row=row,column=col,padx=1,pady=1)
            label = tk.Label(master=frame, text=alphabet[i],bg="grey")
            label.pack(padx=5,pady=5)
            self.keysToLamps[alphabet[i]] = (label,)
            i += 1
            col += 1
    
    def ResetLamp(self, value):
        print(value)
        widget = self.keysToLamps[value]
        widget[0].config(bg=btn_unselected)
        print(widget)
    
    def DrawKeys(self,targetFrame):
        i = 0
        row = 0
        col = 0
        max = 9

        for i in range(0,26):
            if row == 1:
                max = 8
            else:
                max = 9
            if col >= max:
                row += 1
                col = 0
            frame = tk.Frame(master=targetFrame,
                            relief=RAISED,
                            borderwidth=1)
            
            frame.grid(row=row,column=col,padx=1,pady=1)
            btn = tk.Button(master=frame, text=alphabet[i],command = lambda value=alphabet[i]:self.HighlightLamp(value))
            #btn.bind(f"<Button-1>", handle_click)
            btn.pack(padx=5,pady=5)
            tup = self.keysToLamps[alphabet[i]]
            self.keysToLamps[alphabet[i]] = (tup[0],btn)
            i += 1
            col += 1

    def __init__(self):
        self.window = tk.Tk("Enigma Simulator")
        rotorSelectionFrame = tk.Frame(master=self.window, height=100)
        self.DrawRotors(rotorSelectionFrame)
        frameLamps = tk.Frame(master=self.window)
        self.DrawLamps(frameLamps)
        frameInputs = tk.Frame(master=self.window,relief=borderEffects["sunken"],borderwidth=5)

        self.inputLabel = tk.Label(master=frameInputs, text="")
        self.inputLabel.pack()

        frameKeys = tk.Frame(master=self.window,relief=borderEffects["sunken"],borderwidth=5)
        self.DrawKeys(frameKeys)

        
        frameDecrypted = tk.Frame(master=self.window,relief=borderEffects["sunken"],borderwidth=5,bg="white",height=100)
        self.decryptedLabel = tk.Label(master=frameDecrypted,text="")

        rotorSelectionFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        frameLamps.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        frameInputs.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        frameKeys.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        frameDecrypted.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.window.mainloop()







