from keyboard import Keyboard
from plugboard import Plugboard
from rotor import Rotor
from reflector import Reflector
from enigma import Enigma
import tkinter as tk
from tkinter import ttk

#We initialize the machine settings

#The wirings and notches
wire1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
notch1 = "Q"
wire2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
notch2 = "E"
wire3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
notch3 = "V"
wire4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
notch4 = "J"
wire5 = "VZBRGITYUPSDNHLXAWMJQOFECK"
notch5 = "Z"

#The rotors
I = Rotor(wire1, notch1)
II = Rotor(wire2, notch2)
III = Rotor(wire3, notch3)
IV = Rotor(wire4, notch4)
V = Rotor(wire5, notch5)

#The reflectors
A = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")

#The keyboard and plugboard
KB = Keyboard()
plugboardList = ["AB", "CD", "EF", "GH", "IJ"]
PB = Plugboard(plugboardList)

#The machine and its initial settings
ENIGMA = Enigma(B, I, II, III, PB, KB)
rotorConfig="CAT"
ENIGMA.setRotor(rotorConfig)

while wire1[0] != rotorConfig[0]:
    wire1 = wire1[1:] + wire1[0]

while wire2[0] != rotorConfig[1]:
    wire2 = wire2[1:] + wire2[0]

while wire3[0] != rotorConfig[2]:
    wire3 = wire3[1:] + wire3[0]

ENIGMA.setRings((1,1,1))

#We create a screen with its properties
screen = tk.Tk()
screen.title('Enigma Machine emulator')
screen.geometry('800x590')
screen.maxsize(width=850, height=590)
screen.minsize(width=850, height=590)
screen.configure(bg='burlywood4')

#Functions related to the keyboard
currentText=" "
path= " "
pathLabel = ttk.Label(screen, text="Encription path: N/A", background="burlywood4", foreground="#EEEEAD")
pathLabel.grid(row=11, column=0, columnspan=10, pady=20)

def press(key):
    global currentText
    currentText = currentText + str(key)
    initialText.set(currentText)

    if key == ' ':
        return

    global wire1, notch1, wire2, notch2, wire3
    if wire2[0] == notch2:
        wire3 = wire3[1:] + wire3[0]
        updateLabel(3)
        wire2 = wire2[1:] + wire2[0]
        updateLabel(2)
        wire1 = wire1[1:] + wire1[0]
        updateLabel(1)
    elif wire1[0] == notch1:
        wire2 = wire2[1:] + wire2[0]
        updateLabel(2)
        wire1 = wire1[1:] + wire1[0]
        updateLabel(1)
    else:
        wire1 = wire1[1:] + wire1[0]
        updateLabel(1)

    global path

    funcResult = ENIGMA.encipher(key, path)

    path = funcResult[1]

    pathLabel.config(text="Encryption path" + path)

def nextRotor(nrRotor):
    global wire1, wire2, wire3
    if nrRotor == 1:
        wire1 = wire1[1:] + wire1[0]
        updateLabel(1)
    elif nrRotor == 2:
        wire2 = wire2[1:] + wire2[0]
        updateLabel(2)
    else:
        wire3 = wire3[1:] + wire3[0]
        updateLabel(3)

def prevRotor(nrRotor):
    global wire1, wire2, wire3, I, II, III
    if nrRotor == 1:
        wire1 = wire1[25] + wire1[:25]
        updateLabel(1)
    elif nrRotor == 2:
        wire2 = wire2[25] + wire2[:25]
        updateLabel(2)
    else:
        wire3 = wire3[25] + wire3[:25]
        updateLabel(3)

def clear():
    global currentText, path
    currentText = " "
    initialText.set(currentText)
    encipheredText.set(currentText)

    path = ""
    pathLabel.config(text="Encryption path: N/A")

def enter():
    global path
    message = initialText.get()
    enciphered = ""
    for letter in message:
        funcResult = ENIGMA.encipher(letter, path)
        enciphered = enciphered + funcResult[0]
    encipheredText.set(enciphered)

    path = ""
    pathLabel.config(text="Encryption path: N/A")

def backspace():
    message = initialText.get()
    newMessage = message[:-1]
    initialText.set(newMessage)

def updateLabel(nrRotor):
    global wire1, wire2, wire3
    if nrRotor == 1:
        newLabel = wire1[0]
        rotor1.config(text=newLabel)
    elif nrRotor == 2:
        newLabel = wire2[0]
        rotor2.config(text=newLabel)
    elif nrRotor == 3:
        newLabel = wire3[0]
        rotor3.config(text=newLabel)

#Style for buttons
class CustomButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg='gray15', fg='white', activebackground='black', activeforeground='white')

#Rotors
prev1 = CustomButton(screen, text='<', width=6, command=lambda:prevRotor(1))
prev1.grid(row=0, column=0, pady=10, ipadx=6, ipady=3)
rotor1 = tk.Label(screen, text=rotorConfig[0], anchor="center", background="gray15", foreground="white", relief="raised", borderwidth=2, highlightcolor="black")
rotor1.grid(row=0, column=1, pady=10, ipadx=10, ipady=15)
next1 = CustomButton(screen, text='>', width=6, command=lambda:nextRotor(1))
next1.grid(row=0, column=2, pady=10, ipadx=6, ipady=3)

prev2 = CustomButton(screen, text='<', width=6, command=lambda:prevRotor(2))
prev2.grid(row=0, column=3, pady=10, ipadx=6, ipady=3)
rotor2 = tk.Label(screen, text=rotorConfig[1], anchor="center", background="gray15", foreground="white", relief="raised", borderwidth=2, highlightcolor="black")
rotor2.grid(row=0, column=4, pady=10, ipadx=10, ipady=15)
next2 = CustomButton(screen, text='>', width=6, command=lambda:nextRotor(2))
next2.grid(row=0, column=5, pady=10, ipadx=6, ipady=3)

prev3 = CustomButton(screen, text='<', width=6, command=lambda:prevRotor(3))
prev3.grid(row=0, column=6, pady=10, ipadx=6, ipady=3)
rotor3 = tk.Label(screen, text=rotorConfig[2], anchor="center", background="gray15", foreground="white", relief="raised", borderwidth=2, highlightcolor="black")
rotor3.grid(row=0, column=7, pady=10, ipadx=10, ipady=15)
next3 = CustomButton(screen, text='>', width=6, command=lambda:nextRotor(3))
next3.grid(row=0, column=8, pady=10, ipadx=6, ipady=3)

#Plugboard
count = 0
for pair in plugboardList:
    plugboardPair = tk.Label(screen, text=pair[0] + "-" + pair[1], anchor="center", background="gray15", foreground="white", relief="raised", borderwidth=2, highlightcolor="black")
    plugboardPair.grid(row=6, column=count, pady=10, ipadx=10, ipady=10)
    count = count + 1

while count != 9:
    plugboardPair = tk.Label(screen, text="N\A", anchor="center", background="gray15",
                              foreground="white", relief="raised", borderwidth=2, highlightcolor="black")
    plugboardPair.grid(row=6, column=count, pady=10, ipadx=10, ipady=10)
    count = count + 1

#Style for entries
entryStyle = ttk.Style()
entryStyle.configure("Black.TEntry", fieldbackground="black", foreground="white")

#Entry for the initial text
label1 = ttk.Label(screen, text="Initial text:", background="burlywood4", foreground="#EEEEAD")
label1.grid(row=7, column=0, pady=10, sticky='w')
initialText= tk.StringVar()
initialTextEntry = tk.Entry(screen, textvariable=initialText, bg="#CDCD95")
initialTextEntry.grid(row=8, rowspan=1, columnspan=60, ipadx=999, ipady=20)

#Entry for the enciphered text
label2 = ttk.Label(screen, text="Enciphered text:", background="burlywood4", foreground="#EEEEAD")
label2.grid(row=9, column=0, pady=10, sticky='w')
encipheredText= tk.StringVar()
encipheredTextEntry = tk.Entry(screen, textvariable=encipheredText, bg="#CDCD95")
encipheredTextEntry.grid(row=10, rowspan=1, columnspan=60, ipadx=999, ipady=20)


#First row of the keyboard
q = CustomButton(screen, text='Q', width=6, command=lambda:press('Q'))
q.grid(row=1, column=0, pady=2, ipadx=6, ipady=10)

w = CustomButton(screen, text='W', width=6, command=lambda:press('W'))
w.grid(row=1, column=1, pady=2, ipadx=6, ipady=10)

e = CustomButton(screen, text='E', width=6, command=lambda:press('E'))
e.grid(row=1, column=2, pady=2, ipadx=6, ipady=10)

r = CustomButton(screen, text='R', width=6, command=lambda:press('R'))
r.grid(row=1, column=3, pady=2, ipadx=6, ipady=10)

t = CustomButton(screen, text='T', width=6, command=lambda:press('T'))
t.grid(row=1, column=4, pady=2, ipadx=6, ipady=10)

z = CustomButton(screen, text='Z', width=6, command=lambda:press('Z'))
z.grid(row=1, column=5, pady=2, ipadx=6, ipady=10)

u = CustomButton(screen, text='U', width=6, command=lambda:press('U'))
u.grid(row=1, column=6, pady=2, ipadx=6, ipady=10)

i = CustomButton(screen, text='I', width=6, command=lambda:press('I'))
i.grid(row=1, column=7, pady=2, ipadx=6, ipady=10)

o = CustomButton(screen, text='O', width=6, command=lambda:press('O'))
o.grid(row=1, column=8, pady=2, ipadx=6, ipady=10)

#Second row of the keyboard

a = CustomButton(screen, text='A', width=6, command=lambda:press('A'))
a.grid(row=2, column=0, pady=2, ipadx=6, ipady=10)

s = CustomButton(screen, text='S', width=6, command=lambda:press('S'))
s.grid(row=2, column=1, pady=2, ipadx=6, ipady=10)

d = CustomButton(screen, text='D', width=6, command=lambda:press('D'))
d.grid(row=2, column=2, pady=2, ipadx=6, ipady=10)

f = CustomButton(screen, text='F', width=6, command=lambda:press('F'))
f.grid(row=2, column=3, pady=2, ipadx=6, ipady=10)

g = CustomButton(screen, text='G', width=6, command=lambda:press('G'))
g.grid(row=2, column=4, pady=2, ipadx=6, ipady=10)

h = CustomButton(screen, text='H', width=6, command=lambda:press('H'))
h.grid(row=2, column=5, pady=2, ipadx=6, ipady=10)

j = CustomButton(screen, text='J', width=6, command=lambda:press('J'))
j.grid(row=2, column=6, pady=2, ipadx=6, ipady=10)

k = CustomButton(screen, text='K', width=6, command=lambda:press('K'))
k.grid(row=2, column=7, pady=2, ipadx=6, ipady=10)

clear = CustomButton(screen, text='Clear', width=6, command=clear)
clear.grid(row=2, column=8, ipadx=6, ipady=10)

#Third row of the keyboard

p = CustomButton(screen, text='P', width=6, command=lambda:press('P'))
p.grid(row=3, column=0, pady=2, ipadx=6, ipady=10)

y = CustomButton(screen, text='Y', width=6, command=lambda:press('Y'))
y.grid(row=3, column=1, pady=2, ipadx=6, ipady=10)

x = CustomButton(screen, text='X', width=6, command=lambda:press('X'))
x.grid(row=3, column=2, pady=2, ipadx=6, ipady=10)

c = CustomButton(screen, text='C', width=6, command=lambda:press('C'))
c.grid(row=3, column=3, pady=2, ipadx=6, ipady=10)

v = CustomButton(screen, text='V', width=6, command=lambda:press('V'))
v.grid(row=3, column=4, pady=2, ipadx=6, ipady=10)

b = CustomButton(screen, text='B', width=6, command=lambda:press('B'))
b.grid(row=3, column=5, pady=2, ipadx=6, ipady=10)

n = CustomButton(screen, text='N', width=6, command=lambda:press('N'))
n.grid(row=3, column=6, pady=2, ipadx=6, ipady=10)

m = CustomButton(screen, text='M', width=6, command=lambda:press('M'))
m.grid(row=3, column=7, pady=2, ipadx=6, ipady=10)

l = CustomButton(screen, text='L', width=6, command=lambda:press('L'))
l.grid(row=3, column=8, pady=2, ipadx=6, ipady=10)

#Encipher
encipher = CustomButton(screen, text='Encipher', command=enter)
encipher.grid(row=4, column=0, padx=10, pady=10)

#Spacebar
spacebar = CustomButton(screen, text='Spacebar', width=18, command=lambda:press(' '))
spacebar.grid(row=4, column=2, columnspan=5, pady=4, ipadx=150, ipady=10)

#Backspace
backspace = CustomButton(screen, text='Backspace', command=backspace)
backspace.grid(row=4, column=8, padx=3, pady=10)

screen.mainloop()