import tkinter as tk
from PIL import ImageTk, Image

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

img = ImageTk.PhotoImage(Image.open("images.jpg"))
panel = tk.Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

root.mainloop()