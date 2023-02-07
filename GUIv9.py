import os           # for magick and tesseract commands
import time         # for epoch time
import calendar     # for epoch time
from PyPDF2 import PdfFileMerger
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def select_pdf_file():
    file_path = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("PDF files", "*.pdf"), ("all files", "*.*")))
    return file_path

def search_keyword(file_path):
    epoch_time = int(calendar.timegm(time.gmtime()))
    file = os.path.basename(file_path)

    if not file.endswith('.pdf'):
        messagebox.showerror("Error", "Please select a valid PDF file")
        return

    print('Working on converting: ' + file)
    # setup
    file = file.replace('.pdf', '') # get just the filepath without the extension
    folder = str(int(epoch_time)) + '_' + file # generate a folder name for temporary images
    combined = folder + '/' + file # come up with temporary export path
    # create folder
    if not os.path.exists(folder): # make the temporary folder
        os.makedirs(folder)
    # convert PDF to PNG(s)
    magick = 'convert -density 150 "' + file_path + '" "' + combined + '-%04d.png"'
    print(magick)
    os.system(magick)
    # convert PNG(s) to PDF(s) with OCR data
    tiffs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for pic in tiffs:
        if pic.endswith('.png'):
            combined_pic = folder + '/' + pic
            print(combined_pic)
            tesseract = 'tesseract "' + combined_pic + '" "' + combined_pic + '-ocr"'
            print(tesseract)
            os.system(tesseract)
    # merge all PDFs into one PDF with OCR data
    pdfs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.pdf')]
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(os.path.join(folder, pdf))
    merger.write(file + "-OCR.pdf")
    merger.close()
    messagebox.showinfo("Success!", "Your PDF has been converted and saved as " + file + "-OCR.pdf")

# GUI Window
root = tk.Tk()
root.title("PDF OCR Processor")

frame = tk.Frame(root)
frame.pack()

select_file_button
