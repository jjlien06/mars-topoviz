import tkinter as tk
import os
import Martian_3D_Viewer as M3DV
import pickle

root = tk.Tk()

root.title("MTV")
root.geometry("1000x500")
# Icon Uses CC atribution liciense take from https://icon-icons.com/icon/mars/96191.
root.iconbitmap(os.getcwd() + "/GUI_Images/"+"mars_96191.ico")

quitButton = tk.Button(text = "Quit", bg="red", command= root.quit, width=7, height=2, anchor="center")
quitButton.place(relx=.925, rely=.90)

dataFiles = []
for file in os.listdir(os.getcwd() + "/topography_tensors/"):
    dataFiles.append(file)

selected = tk.StringVar()
selected.set("Select a File")

fileSelect = tk.OptionMenu(root, selected,*dataFiles)
fileSelect.place(relx=.5, rely=.5, anchor="center")

titleLabel = tk.Label(root, text = "Select a file to view", font=("Helvetica", 24))
titleLabel.place(relx=.5, rely=.4, anchor="center")



def view():
    FileName = selected.get()
    filePath = os.getcwd() + "/Topography_tensors/"
    resultFile = open(filePath + FileName, "rb")
    tensor = pickle.load(resultFile)
    M3DV.MartianView(tensor)


viewButton = tk.Button(text = "View", bg="green",command= view, width=7, height=2)
viewButton.place(relx=.5, rely=.6, anchor="center")

root.mainloop()