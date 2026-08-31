import matplotlib.pyplot as plt
import pickle
import os


#uses matLab to plot the 3D tensor

def MartianView(TensorFile):
    

    # Plot
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.voxels(TensorFile, facecolors="red", edgecolors="black", linewidth=0.125)

    ax.set(xticklabels=[],yticklabels=[],zticklabels=[])

    plt.show()
