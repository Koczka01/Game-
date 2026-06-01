import tkinter as tk
from PIL import ImageTk, Image
import csv

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

canvas = tk.Canvas(root, width=800, height=600, bg="skyblue")
canvas.pack()

TALAJ_Y = 500
kamera_x = 0

TALAJ_SZAKASZOK = []

def palya_betoltes(fajlnev):
    szakaszok = []
    try:
        with open(fajlnev, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for sor in reader:
                start = int(sor['start'])
                end = int(sor['end'])
                szakaszok.append((start, end))
    except FileNotFoundError:
        print(f"A {fajlnev} nem található, alapértelmezett pálya betöltése...")
        szakaszok = [(-2000, 600), (750, 1200), (1400, 5000)]
    return szakaszok

TALAJ_SZAKASZOK = palya_betoltes("akadaly.csv")

# Talajdarabok kirajzolása
for start, end in TALAJ_SZAKASZOK:
    canvas.create_rectangle(start, TALAJ_Y, end, 1000, fill="green", outline="", tags="palya")

# Felhők dekorációnak
canvas.create_oval(200, 100, 300, 150, fill="white", outline="", tags="palya")
canvas.create_oval(700, 120, 850, 170, fill="white", outline="", tags="palya")

# Karakter betöltése
try:
    img_open = Image.open("images.jpg")
    img_resized = img_open.resize((46, 59), Image.Resampling.LANCZOS)
    karakter_kep = ImageTk.PhotoImage(img_resized)
    karakter = canvas.create_image(400, 300, image=karakter_kep, anchor="center")
except FileNotFoundError:
    karakter = canvas.create_rectangle(377, 270, 423, 330, fill="red")

# --- ÚJ ELLENSÉGEK BETÖLTÉSE ÉS HOZZÁADÁSA ---

ellenseg_kepek = []
ellensegek = []

# Ellenségek tulajdonságai: (fájlnév, kezdeti_x, kezdeti_y, típus)
# típus: 0=földi, 1=repülő
ellenseg_adatok = [
    ("one.jpg", 1000, TALAJ_Y - 20, 0),  # Kicsi földi akadály
    ("ketto.jpg", 2200, TALAJ_Y - 50, 0), # Nagyobb földi akadály
    ("three.jpg", 1800, TALAJ_Y - 150, 1) # Repülő akadály
]

try:
    for fajlnev, start_x, start_y, tipus in ellenseg_adatok:
        img_open = Image.open(fajlnev)
        # Resizing (adjust size as needed for each enemy)
        w, h = img_open.size
        # Simple resize to a consistent height for testing
        w = int(w * (40 / h))
        h = 40
        img_resized = img_open.resize((w, h), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_resized)
        ellenseg_kepek.append(img_tk) # Keep reference to prevent garbage collection

        # create enemy on canvas, moving with the level
        ellenseg = canvas.create_image(start_x, start_y, image=img_tk, anchor="center", tags="palya")
        ellensegek.append({'id': ellenseg, 'x_start': start_x, 'tipus': tipus})
except FileNotFoundError:
    print("Egy vagy több ellenség kép nem található. Piros négyzetekkel helyettesítve.")
    for fajlnev, start_x, start_y, tipus in ellenseg_adatok:
        w, h = 40, 40
        ellenseg = canvas.create_rectangle(start_x-20, start_y-20, start_x+20, start_y+20, fill="red", tags="palya")
        ellensegek.append({'id': ellenseg, 'x_start': start_x, 'tipus': tipus})


# --- JÁTÉKMENET BEÁLLÍTÁSOK ---

sebesseg = 10
fuggoleges_sebesseg = 0
GRAVITACIO = 0.8
UGRAS_ERO = -15
levegoben_van = True 

gombok_allapota = {'a': False, 'd': False}

def gomb_le(event):
    if event.keysym in gombok_allapota:
        gombok_allapota[event.keysym] = True

def gomb_fel(event):
    if event.keysym in gombok_allapota:
        gombok_allapota[event.keysym] = False

def jump(event):
    global fuggoleges_sebesseg, levegoben_van
    if not levegoben_van:
        fuggoleges_sebesseg = UGRAS_ERO
        levegoben_van = True

def jatekhurok():
    global fuggoleges_sebesseg, levegoben_van, kamera_x

    if gombok_allapota['a']:
        canvas.move("palya", sebesseg, 0)
        kamera_x -= sebesseg
    if gombok_allapota['d']:
        canvas.move("palya", -sebesseg, 0)
        kamera_x += sebesseg

    karakter_vilag_x = 400 + kamera_x

    talajon_all = False
    for start, end in TALAJ_SZAKASZOK:
        if start <= karakter_vilag_x <= end:
            talajon_all = True
            break

    if not talajon_all and fuggoleges_sebesseg >= 0:
        levegoben_van = True

    if levegoben_van:
        fuggoleges_sebesseg += GRAVITACIO
        canvas.move(karakter, 0, fuggoleges_sebesseg)
        
        pos = canvas.coords(karakter)
        aktualis_y = pos[1]
        
        if talajon_all and aktualis_y + 25 >= TALAJ_Y:
            canvas.move(karakter, 0, TALAJ_Y - (aktualis_y + 25))
            fuggoleges_sebesseg = 0
            levegoben_van = False
            
        if aktualis_y > 650:
            canvas.moveto(karakter, 377, 200)
            fuggoleges_sebesseg = 0
            levegoben_van = True
            canvas.move("palya", kamera_x, 0)
            kamera_x = 0

    root.after(16, jatekhurok)
    
root.bind("<KeyPress>", gomb_le)
root.bind("<KeyRelease>", gomb_fel)
root.bind("<space>", jump)

jatekhurok()
root.mainloop()