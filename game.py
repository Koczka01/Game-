import tkinter as tk
from PIL import ImageTk, Image
import time

def szoveg_valtoztatas():
    if alma.get() == 'Meow':
        alma.set('Vau')
    else:
        alma.set('Meow')

root = tk.Tk()

root.title('Ultra mega epic game')

alma = tk.StringVar(root, 'Vau')
label = tk.Label(root, textvariable=alma)
label.pack()

gomb = tk.Button(root, textvariable=alma, command=szoveg_valtoztatas)
gomb.pack()

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

TALAJ_Y = 500
canvas.create_rectangle(0, TALAJ_Y, 800, 600, fill="green", outline="")

img_open = Image.open("images.jpg")
img_resized = img_open.resize((46, 59), Image.Resampling.LANCZOS)
karakter_kep = ImageTk.PhotoImage(img_resized)

karakter = canvas.create_image(400, 300, image=karakter_kep, anchor="center")

sebesseg = 10

fuggoleges_sebesseg = 0
GRAVITACIO = 0.8
UGRAS_ERO = -15
levegoben_van = False

def fel(event):
    canvas.move(karakter, 0, -sebesseg)

def le(event):
    canvas.move(karakter, 0, sebesseg)

def balra(event):
    canvas.move(karakter, -sebesseg, 0)

def jobbra(event):
    canvas.move(karakter, sebesseg, 0)

def jump(event):
    global fuggoleges_sebesseg, levegoben_van
    if not levegoben_van:
        fuggoleges_sebesseg = UGRAS_ERO
        levegoben_van = True

def jatekhurok():
    global fuggoleges_sebesseg, levegoben_van

    if levegoben_van:
        fuggoleges_sebesseg += GRAVITACIO
        
        canvas.move(karakter, 0, fuggoleges_sebesseg)
        
        pos = canvas.coords(karakter)
        aktualis_y = pos[1]
        
        if aktualis_y + 25 >= TALAJ_Y:
            canvas.move(karakter, 0, TALAJ_Y - (aktualis_y + 25))
            fuggoleges_sebesseg = 0
            levegoben_van = False

    root.after(16, jatekhurok)

root.bind("<w>", fel)
root.bind("<s>", le)
root.bind("<a>", balra)
root.bind("<d>", jobbra)
root.bind("<space>", jump)

jatekhurok()
root.mainloop()