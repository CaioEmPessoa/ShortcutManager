import icoextract
from PIL import Image, ImageTk
import tkinter as tk



path_icon = icoextract.IconExtractor("C:\Program Files\GIMP 2\\bin\gimp-2.10.exe").get_icon()
path_icon = Image.open(path_icon)

icon_path = "img/"+"gimp"+".ico"
path_icon.save(icon_path)