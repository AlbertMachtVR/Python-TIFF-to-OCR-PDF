import os           # for magick and tesseract commands
import time         # for epoch time
import calendar     # for epoch time
from PyPDF2 import PdfFileMerger
from tkinter import *


def run_script2():
    dir_files = [f for f in os.listdir(".") if os.path.isfile(os.path.join(".", f))]
    epoch_time = int(calendar.timegm(time.gmtime()))

    for file in dir_files: # look at every file in the current directory
        if file.endswith('.pdf'): # if it is a PDF, use it
            # setup
            file = file.replace('.pdf', '') # get just the filepath without the extension
            folder = str(int(epoch_time)) + '_' + file # generate a folder name for temporary images
            combined = folder + '/' + file # come up with temporary export path
            # create folder
            if not os.path.exists(folder): # make the temporary folder
                os.makedirs(folder)
            # convert PDF to PNG(s)
            magick = 'convert -density 150 "' + file + '.pdf" "' + combined + '-%04d.png"'
            os.system(magick)
            # convert PNG(s) to PDF(s) with OCR data
            pngs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            for pic in pngs:
                if pic.endswith('.png'):
                    combined_pic = folder + '/' + pic
                    tesseract = 'tesseract "' + combined_pic + '" "' + combined_pic + '-ocr" PDF'
                    os.system(tesseract)
            # convert TIFF(s) to PDF(s) with OCR data
            tiffs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            for pic in tiffs:
                if pic.endswith('.tiff', '.tif'):
                    combined_pic = folder + '/' + pic
                    tesseract = 'tesseract "' + combined_pic + '" "' + combined_pic + '-ocr" PDF'
                    os.system(tesseract)
            # combine OCR'd PDFs into one
            ocr_pdfs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

            merger = PdfFileMerger()
            for pdf in ocr_pdfs:
                if pdf.endswith('.pdf'):
                    merger.append(folder + '/' + pdf)

        merger.write(file + '-ocr-combined.pdf')
        merger.close()

