import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import os
import time
import calendar
from PyPDF2 import PdfMerger

def select_pdf_file():
    file_path = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("PDF files", "*.pdf"), ("all files", "*.*")))
    return file_path

# GUI Window
root = tk.Tk()
root.title("PDF OCR Processor")

frame = tk.Frame(root)
frame.pack(pady=20)

# File Selection Button
select_file_button = tk.Button(frame, text="Select File", command=lambda: process_pdf(select_pdf_file()))
select_file_button.pack()

# Status Bar
status = tk.StringVar()
status.set("Ready")
status_bar = tk.Label(root, textvariable=status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")

def process_pdf(file_path):
    status.set("Processing...")
    progress_bar.pack(pady=10)
    progress_bar.start()
    file = os.path.basename(file_path)
    file = file.replace('.pdf', '')

    epoch_time = int(calendar.timegm(time.gmtime()))
    folder = str(int(epoch_time)) + '_' + file
    combined = folder + '/' + file

    if not os.path.exists(folder):
        os.makedirs(folder)

    magick = 'convert -density 150 "' + file_path + '" "' + combined + '-%04d.png"'
    os.system(magick)

    pngs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for pic in pngs:
        if pic.endswith('.png'):
            combined_pic = folder + '/' + pic
            tesseract = 'tesseract "' + combined_pic + '" "' + combined_pic + '-ocr" PDF'
            os.system(tesseract)

    tiffs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for pic in tiffs:
        if pic.endswith(('.tiff', '.tif')):
            combined_pic = folder + '/' + pic
            tesseract = 'tesseract "' + combined_pic + '" "' + combined_pic + '-ocr" PDF'
            os.system(tesseract)

    ocr_pdfs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    merger = PdfMerger()
    for pdf in ocr_pdfs:
        if pdf.endswith('.pdf'):
            merger.append(folder + '/' + pdf)

    merger.write(file + '-ocr-combined.pdf')
    merger.close()

    # Do processing here

    progress_bar.stop()
    status.set("Processing completed.")

root.mainloop()
