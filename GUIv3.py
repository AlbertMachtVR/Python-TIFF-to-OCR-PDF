import tkinter as tk
import subprocess

def run_script():
    subprocess.call(["python", "Start.py"])

root = tk.Tk()

welcome_label = tk.Label(root, text="OCR your PDF")
welcome_label.pack()

input_field = tk.Entry(root)
input_field.pack()

generate_button = tk.Button(root, text="Generate", command=run_script)
generate_button.pack()

root.mainloop()
