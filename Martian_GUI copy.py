import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import Martain_3D_Arraycopy as M3DA
import Martian_3D_Viewer as M3DV

root = tk.Tk()

root.title("MTG")
root.geometry("1000x500")
# Icon Uses CC atribution liciense take from https://icon-icons.com/icon/mars/96191.
root.iconbitmap(os.getcwd() + "/GUI_Images/"+"mars_96191.ico")

quitButton = tk.Button(text = "Quit", bg="red", command= root.quit, width=7, height=2, anchor="center")
quitButton.place(relx=.925, rely=.90)

dataFiles = []
for file in os.listdir(os.getcwd() + "/dataFiles/"):
    dataFiles.append(file)

selected = tk.StringVar()
selected.set("Select a File")

fileSelect = tk.OptionMenu(root, selected,*dataFiles)
fileSelect.place(relx=.7+.075, rely=.1)

canvasSize = (500,280)

marsCanvas = tk.Canvas(root, background="red",width=500, height=280, relief="raised")
marsCanvas.place(relx=.05,rely=.075)

marsPhoto = Image.open(os.getcwd() + "/GUI_Images/"+"MOLA_mercat.jpg")
marsPhoto = marsPhoto.resize(canvasSize)
marsImage = ImageTk.PhotoImage(marsPhoto)
marsCanvas.create_image(0,0,image= marsImage, anchor = "nw")



xEntry = tk.Entry(root)
yEntry = tk.Entry(root)
zEntry = tk.Entry(root)

xMaxLable = tk.Label(root, text= "Enter X Grid Dimension")
yMaxLable = tk.Label(root, text= "Enter Y Grid Dimension")
zMaxLable = tk.Label(root, text= "Enter Z Grid Dimension")

latMinEntry = tk.Entry(root)
latMaxEntry = tk.Entry(root)
longMinEntry = tk.Entry(root)
longMaxEntry = tk.Entry(root)

latLable = tk.Label(root, text= "Enter Latitude (0-180)")
longLable = tk.Label(root, text= "Enter Longitude (0-360)")

latMinLable = tk.Label(root, text = "Minimum")
latMaxLable = tk.Label(root, text = "Maximum")
longMinLable = tk.Label(root, text = "Minimum")
longMaxLable = tk.Label(root, text = "Maximum")

xMaxLable.place(relx=.575+.075, rely=.2)
yMaxLable.place(relx=.575+.075, rely=.3)
zMaxLable.place(relx=.575+.075, rely=.4)

xEntry.place(relx=.7+.075, rely=.2)
yEntry.place(relx=.7+.075, rely=.3)
zEntry.place(relx=.7+.075, rely=.4)

latMinEntry.place(relx = .05, rely=.85)
latMaxEntry.place(relx = .2, rely=.85)
longMinEntry.place(relx = .35, rely=.85)
longMaxEntry.place(relx = .5, rely=.85)

latLable.place(relx = .125, rely=.75)
longLable.place(relx = .425, rely=.75)

latMinLable.place(relx = .05+.03, rely=.8)
latMaxLable.place(relx = .2+.03, rely=.8)
longMinLable.place(relx = .35+.03, rely=.8)
longMaxLable.place(relx = .5+.03, rely=.8)


altitudeResolutionLabel = tk.Label(root, text="Enter Height of box (m)", justify="right", anchor="center")
altitudeResolutionEntry = tk.Entry(root)

altitudeResolutionLabel.place(relx=.574+.075,rely=.5)
altitudeResolutionEntry.place(relx=.7+.075,rely=.5)

def createTen():
    x = int(xEntry.get())
    y = int(yEntry.get())
    z = int(zEntry.get())
    

    zRes = int(altitudeResolutionEntry.get())
    selectedFile = selected.get()
    if x*y*z >= 256*256*80:
        tk.messagebox.showwarning(title=None, message="The bounds will create a file too large to run.\nPlease select lower numbers.")
    else:
        M3DA.createTensor(x,y,z,zRes,selectedFile)

def createAndShow():
    x = int(xEntry.get())
    y = int(yEntry.get())
    z = int(zEntry.get())
    zRes = int(altitudeResolutionEntry.get())
    selectedFile = selected.get()
    if x*y*z >= 256*256*80:
        tk.messagebox.showwarning(title=None, message="The bounds will create a file too large to run.\nPlease select lower numbers.")
    else:
        M3DV.MartianView(M3DA.createTensor(x,y,z,zRes,selectedFile))

clickOne = (0,0)
clicks = 0
square=0
def onClick(event):
    global clicks
    global clickOne
    global square
    global canvasSize
    x, y = event.x, event.y
    if clicks == 0:
        clickOne = (x,y)
        clicks += 1
    elif clicks == 1:
        clickTwo = (x,y)
        square=marsCanvas.create_rectangle(clickOne[0],clickOne[1],clickTwo[0],clickTwo[1],outline="light blue", fill="light blue", width=2,stipple="gray50")
        
        latImgValue = [clickOne[1],clickTwo[1]]
        longImgValue = [clickOne[0],clickTwo[0]]

        latRealValue = []
        longRealValue = []

        for i in latImgValue:
            latRealValue.append((180/280)*i)
        for i in longImgValue:
            longRealValue.append((360/500)*i)

        

        latMaxEntry.insert(0, str(latRealValue[0]))
        latMinEntry.insert(0, str(latRealValue[1]))
        longMaxEntry.insert(0, str(longRealValue[0]))
        longMinEntry.insert(0, str(longRealValue[1]))
        clicks += 1
        

marsCanvas.bind("<Button-1>", onClick)

def resetCanvas():
    global clicks
    global square
    marsCanvas.delete(square)
    clicks = 0

    latMaxEntry.delete(0, tk.END)
    latMinEntry.delete(0, tk.END)
    longMaxEntry.delete(0, tk.END)
    longMinEntry.delete(0, tk.END)

resetCanvasButton = tk.Button(text = "Reset Canvas", width= 10, height=1, font=('Helvetica',12,'bold'), borderwidth=5, bg="grey", command=resetCanvas)
resetCanvasButton.place(relx=.05, rely = .65)


createTensorButton = tk.Button(text = "Create Tensor File", width= 15, height=3, font=('Helvetica',12,'bold'), borderwidth=5, bg="grey", command=createTen)
createTensorButton.place(relx=.55+.075, rely = .6)

createTensorButton = tk.Button(text = "Create & View", width= 15, height=3, font=('Helvetica',12,'bold'), borderwidth=5, bg="grey", command=createAndShow)
createTensorButton.place(relx=.75+.075, rely = .6)

root.mainloop()