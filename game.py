import tkinter as tk
from PIL import ImageTk, Image
import csv
import random

def szoveg_valtoztatas():
    if alma.get() == 'Meow':
        alma.set('Vau')
    else:
        alma.set('Meow')

root = tk.Tk()
root.title('Ultra mega epic game - HARDCORE EDITION')

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
        szakaszok = [(-2000, 1200), (1400, 5000)]
    return szakaszok

TALAJ_SZAKASZOK = palya_betoltes("akadaly.csv")

# Talajdarabok kirajzolása
for start, end in TALAJ_SZAKASZOK:
    canvas.create_rectangle(start, TALAJ_Y, end, 1000, fill="green", outline="", tags="palya")

# Sok felhő generálása a háttérbe, hogy ne legyen üres az ég menet közben
for i in range(0, 50000, 1500):
    cx = i + random.randint(0, 500)
    cy = random.randint(50, 200)
    canvas.create_oval(cx, cy, cx+120, cy+50, fill="white", outline="", tags="palya")
    canvas.create_oval(cx+40, cy-20, cx+140, cy+40, fill="white", outline="", tags="palya")

try:
    img_open = Image.open("images.jpg")
    img_resized = img_open.resize((46, 59), Image.Resampling.LANCZOS)
    karakter_kep = ImageTk.PhotoImage(img_resized)
    karakter = canvas.create_image(400, 300, image=karakter_kep, anchor="center")
except FileNotFoundError:
    karakter = canvas.create_rectangle(377, 270, 423, 330, fill="red")

ellenseg_kepek = []
ellensegek = []

# --- ELLENSÉGEK AUTOMATIKUS GENERÁLÁSA (65 darab a teljes pályán) ---
ellenseg_tipusok = ["tüske", "bogár", "medúza"]
fajlnevek = {"tüske": "one.jpg", "bogár": "ketto.jpg", "medúza": "three.jpg"}

# Generálunk ellenségeket 1500 és 48000 pixel között
for i in range(65):
    start_x = random.randint(1500, 48000)
    tipus = random.choice(ellenseg_tipusok)
    fajlnev = fajlnevek[tipus]
    
    # Repülő vagy földi magasság beállítása
    if tipus == "medúza":
        start_y = TALAJ_Y - random.randint(100, 180)  # Különböző magasságokban repülnek
    else:
        start_y = TALAJ_Y - 20 if tipus == "tüske" else TALAJ_Y - 25

    try:
        img_open = Image.open(fajlnev)
        w, h = img_open.size
        w = int(w * (40 / h))
        h = 40
        img_resized = img_open.resize((w, h), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_resized)
        ellenseg_kepek.append(img_tk)
        ellenseg_id = canvas.create_image(start_x, start_y, image=img_tk, anchor="center", tags="palya")
    except FileNotFoundError:
        if tipus == "tüske":
            ellenseg_id = canvas.create_polygon(start_x-20, start_y+20, start_x, start_y-20, start_x+20, start_y+20, fill="purple", outline="black", tags="palya")
        elif tipus == "bogár":
            ellenseg_id = canvas.create_oval(start_x-25, start_y-15, start_x+25, start_y+25, fill="saddlebrown", outline="black", tags="palya")
        else:
            ellenseg_id = canvas.create_oval(start_x-20, start_y-20, start_x+20, start_y+20, fill="lightblue", outline="darkblue", tags="palya")

    # Gyorsabb, agresszívabb alapértelmezett sebességek a nehezítésért
    ellensegek.append({
        'id': ellenseg_id,
        'x_start': start_x,
        'tavolsag': random.randint(150, 350),
        'sebesség': random.choice([-5, -4, -3, 3, 4, 5]),
        'relativ_x': 0
    })

# --- UI ELEMEK ---
game_over_text = canvas.create_text(400, 250, text="", font=("Arial", 30, "bold"), fill="red")
tavolsag_text = canvas.create_text(700, 30, text="Távolság: 0m", font=("Arial", 14, "bold"), fill="black")

sebesseg = 11  # Kicsit gyorsabb mozgás a hatalmas pályához
fuggoleges_sebesseg = 0
GRAVITACIO = 0.8
UGRAS_ERO = -15
levegoben_van = True 
jatek_fut = True

gombok_allapota = {'a': False, 'd': False}

def gomb_le(event):
    if event.keysym in gombok_allapota:
        gombok_allapota[event.keysym] = True

def gomb_fel(event):
    if event.keysym in gombok_allapota:
        gombok_allapota[event.keysym] = False

def jump(event):
    global fuggoleges_sebesseg, levegoben_van
    if not levegoben_van and jatek_fut:
        fuggoleges_sebesseg = UGRAS_ERO
        levegoben_van = True

def ujrainditas():
    global kamera_x, fuggoleges_sebesseg, levegoben_van, jatek_fut
    canvas.itemconfig(game_over_text, text="")
    canvas.moveto(karakter, 377, 200)
    fuggoleges_sebesseg = 0
    levegoben_van = True
    canvas.move("palya", kamera_x, 0)
    kamera_x = 0
    for e in ellensegek:
        canvas.move(e['id'], -e['relativ_x'], 0)
        e['relativ_x'] = 0
        e['sebesség'] = random.choice([-5, -4, 4, 5])
    jatek_fut = True
    jatekhurok()

def jatekhurok():
    global fuggoleges_sebesseg, levegoben_van, kamera_x, jatek_fut

    if not jatek_fut:
        return

    karakter_sugar = 23
    pos_karakter = canvas.coords(karakter)
    
    if pos_karakter:
        aktualis_y = pos_karakter[1]
        karakter_alj = aktualis_y + 25
    else:
        karakter_alj = 325

    dx = 0
    if gombok_allapota['a']:
        dx = -sebesseg
    if gombok_allapota['d']:
        dx = sebesseg

    if dx != 0:
        aktualis_vilag_x = 400 + kamera_x
        tervezett_kamera_x = kamera_x + dx
        tervezett_vilag_x = 400 + tervezett_kamera_x
        
        mehet_oldalra = True
        
        if karakter_alj > TALAJ_Y:
            for start, end in TALAJ_SZAKASZOK:
                if dx < 0 and (aktualis_vilag_x >= end + karakter_sugar) and (tervezett_vilag_x < end + karakter_sugar):
                    mehet_oldalra = False
                    break
                if dx > 0 and (aktualis_vilag_x <= start - karakter_sugar) and (tervezett_vilag_x > start - karakter_sugar):
                    mehet_oldalra = False
                    break
        
        if mehet_oldalra:
            canvas.move("palya", -dx, 0)
            kamera_x = tervezett_kamera_x

    # Élő távolságkijelzés frissítése
    tav_meter = max(0, int(kamera_x / 10))
    canvas.itemconfig(tavolsag_text, text=f"Távolság: {tav_meter}m")

    # Ellenségek intenzívebb, kiszámíthatatlan mozgása
    for e in ellensegek:
        canvas.move(e['id'], e['sebesség'], 0)
        e['relativ_x'] += e['sebesség']
        # 2% esély a hirtelen irány/sebességváltásra képkockánként
        if abs(e['relativ_x']) >= e['tavolsag'] or random.random() < 0.02:
            uj_seb = random.choice([-6, -5, -4, 4, 5, 6])
            if e['relativ_x'] >= e['tavolsag']:
                e['sebesség'] = -abs(uj_seb)
            elif e['relativ_x'] <= -e['tavolsag']:
                e['sebesség'] = abs(uj_seb)
            else:
                e['sebesség'] = uj_seb

    # Ellenség ütközésvizsgálat
    kar_box = canvas.bbox(karakter)
    if kar_box:
        for e in ellensegek:
            e_box = canvas.bbox(e['id'])
            if e_box:
                if (kar_box[0] < e_box[2] and kar_box[2] > e_box[0] and
                    kar_box[1] < e_box[3] and kar_box[3] > e_box[1]):
                    jatek_fut = False
                    canvas.itemconfig(game_over_text, text="GAME OVER")
                    root.after(1500, ujrainditas)
                    return

    # Talajvizsgálat
    karakter_vilag_x = 400 + kamera_x
    talajon_all = False
    for start, end in TALAJ_SZAKASZOK:
        if start <= karakter_vilag_x <= end:
            talajon_all = True
            break

    if not talajon_all and fuggoleges_sebesseg >= 0:
        levegoben_van = True

    # Gravitáció és esés
    if levegoben_van:
        fuggoleges_sebesseg += GRAVITACIO
        canvas.move(karakter, 0, fuggoleges_sebesseg)
        
        pos = canvas.coords(karakter)
        if pos:
            aktualis_y = pos[1]
            karakter_alj = aktualis_y + 25
            
            if talajon_all and karakter_alj >= TALAJ_Y and (karakter_alj - fuggoleges_sebesseg <= TALAJ_Y + 5):
                canvas.move(karakter, 0, TALAJ_Y - karakter_alj)
                fuggoleges_sebesseg = 0
                levegoben_van = False
                
            if aktualis_y > 650:
                jatek_fut = False
                canvas.itemconfig(game_over_text, text="GAME OVER")
                root.after(1500, ujrainditas)
                return

    # Győzelem ellenőrzése a pálya végén (50 000 pixelnél)
    if karakter_vilag_x >= 49500:
        jatek_fut = False
        canvas.itemconfig(game_over_text, text="VICTORY! BERÚGTAD A PÁLYÁT!", fill="gold")
        return

    root.after(16, jatekhurok)
    
root.bind("<KeyPress>", gomb_le)
root.bind("<KeyRelease>", gomb_fel)
root.bind("<space>", jump)

jatekhurok()
root.mainloop()