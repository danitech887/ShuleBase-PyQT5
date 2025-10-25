import shutil
from tkinter import filedialog
folder = filedialog.askdirectory()
output = "cbc"
shutil.make_archive(output, 'zip', folder)
print(f"Folder {folder} to {output}.zip")