import os			    # for magick and tesseract commands
import time			  # for epoch time
import calendar 	# for epoch time
import tkinter as tk # for GUI
from tkinter import filedialog # for file dialog
from PyPDF2 import PdfMerger

class Application(tk.Frame):
    def __init__(self, master: object = None) -> object:
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.input_label = tk.Label(self, text="Directory:")
        self.input_label.pack()

        self.input_entry = tk.Entry(self)
        self.input_entry.pack()

        self.input_button = tk.Button(self, text="Select", command=self.select_directory)
        self.input_button.pack()

        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.pack()

        self.output_label = tk.Label(self, text="Output:")
        self.output_label.pack()

        self.output_text = tk.Text(self)
        self.output_text.pack()

        self.save_button = tk.Button(self, text="Save", command=self.save)
        self.save_button.pack()

    def select_directory(self):
        self.input_directory = filedialog.askdirectory()
        self.input_entry.insert(0, self.input_directory)

    def start(self):
        os.chdir(self.input_directory)
        dir_files = [f for f in os.listdir(".") if os.path.isfile(os.path.join(".", f))]
        epoch_time = int(calendar.timegm(time.gmtime()))
        self.output_text.insert('1.0', 'Working on files: ' + str(dir_files) + '\n')
        for file in dir_files: # look at every file in the current directory
            if file.endswith('.pdf'): # if it is a PDF, use it
                self.output_text.insert('end', 'Working on converting: ' + file + '\n')
                # setup
                file = file.replace('.pdf', '') # get just the filepath without the extension
                folder = str(int(epoch_time)) + '_' + file # generate a folder name for temporary images
                combined = folder + '/' + file # come up with temporary export path
                # create folder
                if not os.path.exists(folder): # make the temporary folder
                    os.makedirs(folder)
                # convert PDF to PNG(s)
                magick = 'convert -density 150 "' + file + '.pdf" "' + combined
                magick = magick + '-%d.png"' % int(epoch_time)
        os.system(magick)
        # OCR PNG(s)
        #tesseract ='tesseract "' + combined + '-%d.png" "' + file + '" -l deu %d' % (int(epoch_time), int(epoch_time))
        tesseract = 'tesseract "{0}-{1}.png" "{2}" -l deu {1}'.format(combined, int(epoch_time), file)
        os.system(tesseract)
        # Merge PNG(s) and OCR-ed TXT back to PDF
        pdf_merger = PdfMerger()
        pdf_merger.append(file + '.pdf')
        pdf_merger.append(file + '.txt')
        pdf_merger.write(file + '_' + str(int(epoch_time)) + '.pdf')
        pdf_merger.close()
        # Clean up
        os.remove(file + '.txt')
        os.rmdir(folder)
        self.output_text.insert('end', 'Finished converting: ' + file + '\n')

    def save(self):
     save_file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
     save_file.write(self.output_text.get("1.0", "end"))
     save_file.close()

root = tk.Tk()
app = Application(master=root)
app.mainloop()