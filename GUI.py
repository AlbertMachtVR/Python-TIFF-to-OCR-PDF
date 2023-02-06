import tkinter as tk
import tkinter.filedialog
from tkinter import filedialog




def generate_pdf():
    # Hier sollte der Code ausgeführt werden, um das PDF zu generieren
    file = filedialog.askopenfilename()
    # Hier sollte der Code stehen, der die PDF-Datei verarbeitet
    popup = tk.Toplevel()
    popup.geometry("200x100")
    label = tk.Label(popup, text="PDF erfolgreich generiert!")
    label.pack()
    button = tk.Button(popup, text="Schließen", command=popup.destroy)
    button.pack()

root = tk.Tk()
root.geometry("500x500")


label = tk.Label(root, text="OCR your PDF")
label.pack()

entry = tk.Entry(root, text="Ziehe deine PDF-Datei hierhin")
entry.pack()

button = tk.Button(root, text="Generate", command=generate_pdf)
button.pack()

root.mainloop()
