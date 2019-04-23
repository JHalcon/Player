from tkinter import *
from pygame import mixer, time
from tkinter import filedialog
import os
import tkinter.messagebox
from mutagen.mp3 import MP3
import threading
root = Tk()
root.title("JS MUSIC PLAYER")
root.geometry("600x500")
mixer.init()

btns = Frame(root)
btns.pack(side=BOTTOM, pady=10)
Ti = Frame(root)
Ti.pack(fill = X)
li = Frame(root, height = 300, width = 200)
li.pack()
ADbtns = Frame(li)
ADbtns.pack(side = BOTTOM, pady = 8)
Dl = Label(root, text="Długość piosenki:", font='Helvetica 13')
Dl.pack(side=BOTTOM)
# nazwa
nazwa = Label(Ti, text="Nazwa utworu:", font='Halvetica 13')
nazwa.pack(fill = X, pady=10)
SEBox = Frame(root)
SEBox.pack(fill = X)

songs = []

def AddS(n):
    n = os.path.basename(filename)
    #print(n)
    index = 0
    ListBox.insert(index, n)
    ListBox.pack()
    songs.insert(index, filename)
    #print(songs)
    index+=1

def UsunP():
    currents = ListBox.curselection()
    #print(currents)
    idx = int(currents[0])
    ListBox.delete(idx)
    songs.pop(idx)

def NextS():
    currents = ListBox.curselection()
    idx = int(currents[0])
    ListBox.select_clear(idx)
    idx = idx+1
    ListBox.activate(idx)
    ListBox.selection_set(idx)
    play()


def PrevS():
    currents = ListBox.curselection()
    idx = int(currents[0])
    ListBox.select_clear(idx)
    idx = idx-1
    ListBox.activate(idx)
    ListBox.selection_set(idx)
    play()


def file():
    global filename
    filename = filedialog.askopenfilename()
    AddS(filename)


ListBox = Listbox(li,bg = "black", fg = "white", width = 50, height = 12)
Adds = Button(ADbtns, text = "Dodaj piosenkę", command = file)
Dels = Button(ADbtns, text = "Usuń piosenkę", command = UsunP)


def czas(t):
    global ifP
    x = 0
    while x <= t and mixer.music.get_busy():
        if ifP:
            continue
        else:
            mins, sec = divmod(t, 60)
            mins = round(mins)
            sec = round(sec)
            TMformat = '{:02d}:{:02d}'.format(mins, sec)
            Dl['text'] = "Długość piosenki: " + os.path.basename(TMformat)
            time.delay(1000)
            t -= 1




def name(song):
    #print("1")
    nazwa['text'] = "Teraz gramy: " + os.path.basename(song)
    format = os.path.splitext(song)
    if (format[1] == '.mp3'):
        audio = MP3(song)
        lng = audio.info.length
       # print(lng)
    else:
        s = mixer.Sound(song)
        lng = s.get_length()

    min, sec = divmod(lng, 60)
    min = round(min)
    sec = round(sec)
    TMformat = '{:02d}:{:02d}'.format(min, sec)
    #print(TMformat)
    Dl['text'] = "Długość piosenki: " + os.path.basename(TMformat)
    thr1 = threading.Thread(target=czas, args=(lng,))
    thr1.start()


def play():
    global ifP
    if ifP:
        mixer.music.unpause()
        ifP = FALSE
    else:
        try:
            stop()
            time.delay(1000)
            currents = ListBox.curselection()
            idx = int(currents[0])
            toplaysong = songs[idx]
            mixer.music.load(toplaysong)
            print(toplaysong)
            mixer.music.play()
            name(toplaysong)
        except:
            tkinter.messagebox.showerror("Bląd odczytu pliku", "Nie wybrano pliku audio do odtwarzania!")



def stop():
    mixer.music.stop()



ifP = FALSE


def pause():
    global ifP
    ifP = TRUE
    mixer.music.pause()


def volumeFN(v):
    volume = int(v) / 100
    mixer.music.set_volume(volume)


def help():
    tkinter.messagebox.showinfo("Instrukcja użytkowania odtwarzacza muzyki: ",
                                "1.W celu dodania nowego pliku audio wybierz opcję dodaj plik z zakladki plik...")

menu = Menu(root)
root.config(menu=menu)
menu2 = Menu(menu, tearoff=0)
menu.add_cascade(label="pliki", menu=menu2)
menu2.add_command(label="dodaj plik", command=file)
menu3 = Menu(menu, tearoff=0)
menu.add_cascade(label="pomoc", menu=menu3)
menu3.add_command(label="instrukcja użytkowania", command=help)

scale = Scale(li, from_=100, to=0, orient=VERTICAL, command=volumeFN, bg="black", fg="gray")
scale.set(50)
ListBox.configure(height = 17)
ListBox.pack(side = RIGHT)

Adds.pack(side = LEFT)
Dels.pack(side = RIGHT)
mixer.music.set_volume(0.5)
scale.pack(side = LEFT, padx = 5)

PSImg = PhotoImage(file="img/ps.png")
PSBtn = Button(btns, image=PSImg, command=PrevS, )
PSBtn.pack(side=LEFT, padx=10)

PImg = PhotoImage(file="img/play-button.png")
PBtn = Button(btns, image=PImg, command=play, )
PBtn.pack(side=LEFT, padx=10)

STImg = PhotoImage(file="img/stop.png")
STBtn = Button(btns, image=STImg, command=stop)
STBtn.pack(side=LEFT)

PAImg = PhotoImage(file="img/pause.png")
PABtn = Button(btns, image=PAImg, command=pause)
PABtn.pack(side=LEFT, padx=10)

NSImg = PhotoImage(file="img/ns.png")
NSBtn = Button(btns, image=NSImg, command=NextS)
NSBtn.pack(side=RIGHT, padx=10)

def Cl():
    print("zamykanie")
    tkinter.messagebox.showwarning("Uwaga","Czy na pewno chcesz zamknąć program?")
    stop()
    root.destroy()



root.protocol("WM_DELETE_WINDOW",Cl)
root.mainloop()
