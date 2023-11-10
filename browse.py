import tkinter as tk
from tkinter import filedialog

def browse_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()  # Show the file browsing window
    return file_path

file_path = browse_file()
print(f"Selected file: {file_path}")