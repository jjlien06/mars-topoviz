import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import Martian_3D_Array as M3DA
import Martian_3D_Viewer as M3DV
import pandas as pd
import runpy as rp
import sys
import threading
from tkinter.ttk import *

# TK creates main window as root

root = tk.Tk()

root.title("MTG")
root.geometry("1250x600")
# Icon Uses CC atribution liciense take from https://icon-icons.com/icon/mars/96191.
root.iconbitmap(os.getcwd() + "/GUI_Images/"+"mars_96191.ico")

quitButton = tk.Button(text = "Quit", bg="red", command= root.quit, width=7, height=2, anchor="center")
quitButton.place(relx=.925, rely=.90)

# Create a drop down menu for selecting the data file
# Mainly used before the manual file inputs, may still be useful.

dataFiles = []
for file in os.listdir(os.getcwd() + "/dataFiles/"):
    dataFiles.append(file)

selected = tk.StringVar()
selected.set("Manual Data File Select")

fileSelect = tk.OptionMenu(root, selected,*dataFiles)
fileSelect.place(relx=.75+.075, rely=.1)

# Create a canvas to display the image of Mars
# Further code will allow the user to select a region of the image to create a tensor file.
tallyCanvas = tk.Canvas(root,width=600+2*20, height=336+2*20, relief="raised")
tallyCanvas.place(relx=.275,rely=.35, anchor="center")

for i in range(6):
    tallyCanvas.create_line(20+((i-1)*600/4), 15, 20+((i-1)*600/4), 20, fill="black", width=2)
    tallyCanvas.create_line(15, 20+((i-1)*336/4), 20, 20+((i-1)*336/4), fill="black", width=2)
    if i <= 3:
        tallyCanvas.create_text(20+((i-1)*600/4), 15, text=str(180+ (i-1)*90), font=("Helvetica", 8), anchor="s")
    else:
        tallyCanvas.create_text(20+((i-1)*600/4), 15, text=str((i-3)*90), font=("Helvetica", 8), anchor="s")
    tallyCanvas.create_text(15, 20+((i-1)*336/4), text=str(90-(i-1)*45), font=("Helvetica", 8), anchor="e")

canvasSize = (600,336)

marsCanvas = tk.Canvas(root,width=600, height=336, relief="raised")
marsCanvas.place(relx=.275,rely=.35, anchor="center")

marsPhoto = Image.open(os.getcwd() + "/GUI_Images/"+"MOLA_mercat.jpg")
marsPhoto = marsPhoto.resize(canvasSize)
marsImage = ImageTk.PhotoImage(marsPhoto)
marsCanvas.create_image(0,0,image= marsImage, anchor = "nw")



# Create the entry boxes for the user to input the dimensions of the tensor file


xEntry = tk.Entry(root)
yEntry = tk.Entry(root)
zEntry = tk.Entry(root)
altitudeResolutionEntry = tk.Entry(root)

xMaxLable = tk.Label(root, text= "Enter X Grid Dimension")
yMaxLable = tk.Label(root, text= "Enter Y Grid Dimension")
zMaxLable = tk.Label(root, text= "Enter Z Grid Dimension")
altitudeResolutionLabel = tk.Label(root, text="Enter Height of box (m)", justify="right", anchor="center")

TensorfileLable = tk.Label(root, text= "Tensor File Settings", font=('Helvetica',12,'bold'), anchor="center")

# Creates the boxes for the user to input the latitude and longitude values

datafileLable = tk.Label(root, text= "Data File Settings", font=('Helvetica',12,'bold'), anchor="center")

latMinEntry = tk.Entry(root, width=10)
latMaxEntry = tk.Entry(root,width=10)
longMinEntry = tk.Entry(root,width=10)
longMaxEntry = tk.Entry(root,width=10)

latLable = tk.Label(root, text= "Enter Latitude \n(-90-90)")
longLable = tk.Label(root, text= "Enter Longitude \n(0-360)")

latMinLable = tk.Label(root, text = "Minimum")
latMaxLable = tk.Label(root, text = "Maximum")
longMinLable = tk.Label(root, text = "Minimum")
longMaxLable = tk.Label(root, text = "Maximum")

# Large portion of code place the boxes and labels in the correct location on the GUI, relx and rely place using percentages across the window.
# I think I might go back and change the UI with bigger window size and change things to make it more user friendly.
# Have what controls the file and what controls the tenor seperate.

TensorfileLable.place(relx=.75+.075, rely=.05)

xMaxLable.place(relx=.75+.075, rely=.20)
yMaxLable.place(relx=.75+.075, rely=.30)
zMaxLable.place(relx=.75+.075, rely=.40)

xEntry.place(relx=.75+.075, rely=.25)
yEntry.place(relx=.75+.075, rely=.35)
zEntry.place(relx=.75+.075, rely=.45)
altitudeResolutionLabel.place(relx=.75+.075,rely=.5)
altitudeResolutionEntry.place(relx=.75+.075,rely=.55)

datafileLable.place(relx=.6, rely=.05)

latMinEntry.place(relx = .55+.025, rely=.25)
latMaxEntry.place(relx = .55+.025, rely=.35)
longMinEntry.place(relx = .65+.025, rely=.25)
longMaxEntry.place(relx = .65+.025, rely=.35)

latLable.place(relx = .55+.015, rely=.15)
longLable.place(relx = .65+.015, rely=.15)

latMinLable.place(relx = .55+.025, rely=.2)
latMaxLable.place(relx = .55+.025, rely=.3)
longMinLable.place(relx = .65+.025, rely=.2)
longMaxLable.place(relx = .65+.025, rely=.3)



pointsPerDegreeLabel = tk.Label(root, text="Enter Points per Degree", justify="right", anchor="center")
pointsPerDegreeEntry = tk.Entry(root)

pointsPerDegreeLabel.place(relx=.6,rely=.4)
pointsPerDegreeEntry.place(relx=.6,rely=.45)


fileNameLabel = tk.Label(root, text="Tensor File Name:",font=(16), justify="right", anchor="center")
fileNameLabel.place(relx=.55,rely=.6)

progress = Progressbar(root, orient="horizontal", length=325, mode="determinate")
progressLabel = tk.Label(root, text="Progress", font=("Helvetica",14), justify="right", anchor="center")
progressLabel.place(relx=.25, rely=.8, anchor="center")
progress.place(relx=.25, rely=.85, anchor="center")



def selectFile(longMin, longMax):
    dataLibaraies = [(0,90,"0-90.csv"), (90,180,"90-179.csv"), (180,270,"180-270.csv"), (270,360,"270-360.csv")]
    usedFiles= []
    for i in dataLibaraies:
        if (longMin <= i[0] <= longMax or longMin <= i[1] <= longMax  ) or (i[0] <= longMin <= i[1] and i[0] <= longMax <= i[1]):
            usedFiles.append(i[2])

    print(usedFiles)
    return usedFiles

# The two sister functions createTen and createAndShow, they are nearly identical



def createTen():
    x = int(xEntry.get())
    y = int(yEntry.get())
    z = int(zEntry.get())
    latMax = round(float(latMaxEntry.get()), 2)
    latMin = round(float(latMinEntry.get()), 2)
    longMax = round(float(longMaxEntry.get()),2)
    longMin = round(float(longMinEntry.get()),2)
    datapoints = int(pointsPerDegreeEntry.get())

    zRes = float(altitudeResolutionEntry.get())

    if x*y*z >= 256*256*80:
        tk.messagebox.showwarning(title=None, message="The bounds will create a file too large to run.\nPlease select lower numbers.")
        progress['value'] = 0
        root.update_idletasks() 
        return None
    

    fileNameLabel.config(text="Tensor File Name:"+"Mars" + str(round(latMin,2)) + "-" + str(round(latMax,2)) + "x" +
                    str(round(longMin,2)) + "-" + str(round(longMin,2)) + " " +
                    str(x) + "x" + str(y) + "x" + str(z) + " " +
                    str(zRes) + "(m)")

    outputFileName = (str(round(latMin,2)) + "-" + str(round(latMax,2)) + "x" +
                    str(round(longMin,2)) + "-" + str(round(longMin,2)) + " " +
                    str(x) + "x" + str(y) + "x" + str(z) + " " +
                    str(zRes) + "(m)"+".csv")

    progressLabel.config(text="Collecting Data Files from Library")
    
    inputFiles = selectFile(longMin, longMax)
    
    progress['value'] = 20
    root.update_idletasks() 
    
    progressLabel.config(text="Shaping Data Files")

    outputFileNames = []
    for i in inputFiles:
        if len(inputFiles) == 1:
            outputFileName = i[0:-4]+"tempData"+str(latMin)+"-"+str(latMax)+"x"+str(longMin)+"-"+str(longMin)+".csv"
            sys.argv = [ 'dataptsPerDeg.py', '--bin_size', "1", '--points_per_bin', str(datapoints), '--output_file', os.getcwd() +'/dataFiles/MergedFiles/'+outputFileName, '--min_long', str(longMin), '--max_long', str(longMax), '--min_lat', str(latMin), '--max_lat', str(latMax), os.getcwd() +'/DataLibarary/'+i]
            rp.run_module('dataptsPerDeg', run_name='__main__', alter_sys=True)
        else:

            outputFileName = i[0:-4]+"tempData"+str(latMin)+"-"+str(latMax)+"x"+str(longMin)+"-"+str(longMin)+".csv"
            print(os.getcwd() +'/DataLibarary/'+i)
            sys.argv = [ 'dataptsPerDeg.py', '--bin_size', "1", '--points_per_bin', str(datapoints), '--output_file', os.getcwd() +'/dataFiles/BrokenFiles/'+outputFileName, '--min_long', str(longMin), '--max_long', str(longMax), '--min_lat', str(latMin), '--max_lat', str(latMax), os.getcwd() +'/DataLibarary/'+i]
            rp.run_module('dataptsPerDeg', run_name='__main__', alter_sys=True)
        
        
        outputFileNames.append(outputFileName)
    

    progress['value'] = 30
    root.update_idletasks() 
    progressLabel.config(text="Merging Data Files into 1")


    if len(outputFileNames) > 1:
        
        if len(outputFileNames) == 2:
            sys.argv = [ 'zipper.py', '--output_file', os.getcwd()+'/dataFiles/MergedFiles/'+outputFileName, os.getcwd()+'/dataFiles/BrokenFiles/'+outputFileNames[0],os.getcwd()+ '/dataFiles/BrokenFiles/'+outputFileNames[1]]
            rp.run_module('zipper', run_name='__main__', alter_sys=True)
        elif len(outputFileNames) == 3:
            sys.argv = [ 'zipper.py','--output_file', os.getcwd()+'/dataFiles/MergedFiles/'+outputFileName, os.getcwd()+'/dataFiles/BrokenFiles/'+outputFileNames[0], os.getcwd()+'/dataFiles/BrokenFiles/'+ outputFileNames[1], os.getcwd()+ '/dataFiles/BrokenFiles/'+outputFileNames[2]]
            rp.run_module('zipper', run_name='__main__', alter_sys=True)
        elif len(outputFileNames) == 4:
            sys.argv = [ 'zipper.py','--output_file', os.getcwd()+'/dataFiles/MergedFiles/'+outputFileName, os.getcwd()+'/dataFiles/BrokenFiles/'+outputFileNames[0], os.getcwd()+'/dataFiles/BrokenFiles/'+ outputFileNames[1], os.getcwd()+'/dataFiles/BrokenFiles/'+ outputFileNames[2],os.getcwd()+ outputFileNames[3] ]
            rp.run_module('zipper', run_name='__main__', alter_sys=True)

    selectedFile = outputFileName

    print(selectedFile)

    columns = ['LONG_EAST', 'LAT_NORTH', 'TOPOGRAPHY']
    df = pd.read_csv(os.getcwd() +'/dataFiles/MergedFiles/'+selectedFile, usecols=columns)
    max_alt = float(df['TOPOGRAPHY'].max())
    min_alt = float(df['TOPOGRAPHY'].min())
    if max_alt - min_alt > zRes*z:
        tk.messagebox.showwarning(title=None, message="The height of the tensor is too small.\nPlease select a larger number.")
        progress['value'] = 0
        root.update_idletasks() 
        return None
    

    progress['value'] = 60
    root.update_idletasks() 
    progressLabel.config(text="Creating Tensor File")

    if x*y*z >= 256*256*80:
        tk.messagebox.showwarning(title=None, message="The bounds will create a file too large to run.\nPlease select lower numbers.")
    else:
        tensor = M3DA.createTensor(x,y,z,latMax,latMin,longMax, longMin,zRes,selectedFile)
        progress['value'] = 100
        root.update_idletasks()
        progressLabel.config(text="Tensor File Created")
        return tensor

def createAndShow():
    tensor = createTen()
    progress['value'] = 80
    root.update_idletasks()
    progressLabel.config(text="Loading Tensor File")
    M3DV.MartianView(tensor)
    

#These break the button functions into their own threads, so the GUI does not freeze while the tensor is being created.
# It fixes the volitility of the GUI.

def threadTensor():
    progress['value'] = 0
    root.update_idletasks()

    createTensorButton.config(state="disabled")
    createTensorandShowButton.config(state="disabled")
    thread = threading.Thread(target=createTen)
    thread.start()
    
    createTensorButton.config(state="normal")
    createTensorandShowButton.config(state="normal")


def threadShowTensor():

    progress['value'] = 0
    root.update_idletasks()


    createTensorButton.config(state="disabled")
    createTensorandShowButton.config(state="disabled")
    thread = threading.Thread(target=createAndShow)
    thread.start()


    createTensorButton.config(state="normal")
    createTensorandShowButton.config(state="normal")




# This determines the two points the user clicks on the canvas, and creates a square between them.
# The square is used to determine the bounds of the tensor file.

clickOne = (0,0)
clicks = 0
square=0
circles = []
def onClick(event):
    global clicks
    global clickOne
    global square
    global circles
    global canvasSize
    x, y = event.x, event.y
    if clicks == 0:
        clickOne = (x,y)
        i= marsCanvas.create_oval(x-2.5,y-2.5,x+2.5,y+2.5,fill="Black")
        circles.append(i)
        clicks += 1
    elif clicks == 1:
        clickTwo = (x,y)
        i = marsCanvas.create_oval(x-2.5,y-2.5,x+2.5,y+2.5,fill="Black")
        circles.append(i)
        square=marsCanvas.create_rectangle(clickOne[0],clickOne[1],clickTwo[0],clickTwo[1],outline="light blue", fill="light blue", width=2,stipple="gray50")
        


        latImgValue = [clickOne[1],clickTwo[1]]
        longImgValue = [clickOne[0],clickTwo[0]]

        latRealValue = []
        longRealValue = []

        # This is the conversion from the image values to the real values of latitude and longitude
        # The image is 280x500, and the real values are 180x360

        for i in latImgValue:
            latRealValue.append((180/336)*i)
        for i in longImgValue:
            longRealValue.append((360/600)*i)

        

        minLat = 180-90-max(latRealValue)
        maxLat = 180-90-min(latRealValue)

        minLong = min(longRealValue)
        if minLong < 180:
            minLong = 180 + minLong
        elif minLong > 180:
            minLong = minLong - 180
        maxLong = max(longRealValue)
        if maxLong < 180:
            maxLong = 180 + maxLong
        elif maxLong > 180:
            maxLong = maxLong - 180

        latMaxEntry.insert(0, round(maxLat,4))
        latMinEntry.insert(0, round(minLat,4))
        
        longMaxEntry.insert(0, round(maxLong,4))
        longMinEntry.insert(0, round(minLong,4))
        
        clicks += 1
        

marsCanvas.bind("<Button-1>", onClick)


# This function resets the canvas, and allows a new box to be drawn.

def resetCanvas():
    global clicks
    global square
    global circles
    for i in circles:
        marsCanvas.delete(i)
    marsCanvas.delete(square)
    clicks = 0

    latMaxEntry.delete(0, tk.END)
    latMinEntry.delete(0, tk.END)
    longMaxEntry.delete(0, tk.END)
    longMinEntry.delete(0, tk.END)

resetCanvasButton = tk.Button(text = "Reset Canvas", width= 10, height=1, font=('Helvetica',12,'bold'), borderwidth=5, bg="grey", command=resetCanvas)
resetCanvasButton.place(relx=.05, rely = .675)
    


createTensorButton = tk.Button(text = "Create Tensor File", width= 15, height=3, font=('Helvetica',12,'bold'), borderwidth=5, bg="grey", command=threadTensor)
createTensorButton.place(relx=.55+.075, rely = .75)

createTensorandShowButton = tk.Button(text = "Create & View", width= 15, height=3, font=('Helvetica',12,'bold'), borderwidth=5, bg="grey", command=threadShowTensor)
createTensorandShowButton.place(relx=.75+.075, rely = .75)



root.mainloop()
