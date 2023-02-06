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

            ocr_pdfs = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

            merger = PdfFileMerger()

            for pdf in ocr_pdfs:

                if pdf.endswith('.pdf'):

                    merger.append(folder + '/' + pdf)

        merger.write(file + '-ocr-combined.pdf')

        merger.close()

        root = Tk()

        root['bg']='#008080'

        root['bd']=10

        root['relief']='raised'

        root['cursor']='hand2'

        root['height']=200

        root['width']=200

        root['padx']=10

        root['pady']=10

        root['takefocus']=True

        root['highlightcolor']='#008080'

        root['highlightbackground']='#008080'

        root['highlightthickness']=5

        button1=Button(root,text='OCR',command=run_script2,bg='#008080',fg='white',bd=5,relief='raised',cursor='hand2',height=1,width=5,padx=10,pady=10,takefocus=True,highlightcolor='#008080',highlightbackground='#008080',highlightthickness=5)

        button1.pack()

        button1['command']=run_script2

        root.mainloop()