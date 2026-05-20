import tkinter as tk

def szoveg_valtoztatas():
    alma.set("Meow")


root = tk.Tk()

root.title('Almaaa')

label = tk.Label(root, text="Szia, Tkinter!")
label.pack()
alma = tk.StringVar('Almaaa')

gomb = tk.Button(root, text="Mehet", command=koszonj)
gomb.pack()

root.mainloop()