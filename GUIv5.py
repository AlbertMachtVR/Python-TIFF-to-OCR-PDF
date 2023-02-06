import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess


def run_script():
    file_path = input_field.get()
    keyword = keyword_field.get()
    subprocess.call(["python", "Start2.py", file_path, keyword])

root = tk.Tk()
root.geometry("500x500")
root.configure(bg='#6495ED')

welcome_label = tk.Label(root, text="OCR your PDF", bg='#6495ED', font=("Helvetica", 20))
welcome_label.pack(pady=20)

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

input_frame = tk.Frame(root, bg='#6495ED')
input_frame.pack(pady=20)

input_label = tk.Label(input_frame, text="Drag your PDF here:", bg='#6495ED', font=("Helvetica", 14))
input_label.pack(side='left')

input_field = tk.Entry(input_frame, width=30, font=("Helvetica", 14))
input_field.pack(side='left')

browse_button = tk.Button(input_frame, text="Browse", command=lambda: input_field.insert(0, choose_file()), font=("Helvetica", 14))
browse_button.pack(side='left', padx=10)

keyword_frame = tk.Frame(root, bg='#6495ED')
keyword_frame.pack(pady=20)

keyword_label = tk.Label(keyword_frame, text="Keyword:", bg='#6495ED', font=("Helvetica", 14))
keyword_label.pack(side='left')

keyword_field = tk.Entry(keyword_frame, width=30, font=("Helvetica", 14))
keyword_field.pack(side='left')

generate_button = tk.Button(root, text="Generate", font=("Helvetica", 14), command=run_script)
generate_button.pack(pady=20)

root.mainloop()
