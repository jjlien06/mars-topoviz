import numpy as np
import torch
import pickle
import pandas as pd
import os
import torch.nn.functional as F

def createTensor(x_max, y_max, z_max, latMax, latMin, longMax, longMin, AltResolution, file):
    # Construct file name and file path
    filePath = os.getcwd() + "/Topography_Tensors/"
    resultFileName = ("Mars" + str(round(latMin,2)) + "-" + str(round(latMax,2)) + "x" +
                      str(round(longMin,2)) + "-" + str(round(longMin,2)) + " " +
                      str(x_max) + "x" + str(y_max) + "x" + str(z_max) + " " +
                      str(AltResolution) + "(m)")
    
    # Read CSV data (only the columns we need)
    dataFolderPath = os.getcwd()
    columns = ['LONG_EAST', 'LAT_NORTH', 'TOPOGRAPHY']
    df = pd.read_csv(dataFolderPath + '/dataFiles/MergedFiles/' + file, usecols=columns)
    
    # Determine the minimum altitude (used later)
    altMin = float(df['TOPOGRAPHY'].min())
    
    # Calculate grid step sizes
    latStep = (latMax - latMin) / y_max
    longStep = (longMax - longMin) / x_max
    print("latStep:", latStep)
    print("longStep:", longStep)
    
    # Convert dataframe to NumPy array and compute grid cell indices
    data = df.to_numpy()  # shape (N, 3)
    longitudes = data[:, 0]
    latitudes = data[:, 1]
    altitudes = data[:, 2]
    
    x_indices = np.floor((longitudes - longMin) / longStep).astype(int)
    y_indices = np.floor((latitudes - latMin) / latStep).astype(int)
    
    valid_mask = (x_indices >= 0) & (x_indices < x_max) & (y_indices >= 0) & (y_indices < y_max)
    x_indices = x_indices[valid_mask]
    y_indices = y_indices[valid_mask]
    altitudes = altitudes[valid_mask]
    
    temp_df = pd.DataFrame({'x': x_indices, 'y': y_indices, 'alt': altitudes})
    grouped = temp_df.groupby(['x', 'y'], sort=False).first().reset_index()
    
    altitude_array = np.zeros((x_max, y_max), dtype=np.float32)
    altitude_array[grouped['x'], grouped['y']] = grouped['alt']
    
    # Move data to torch tensor and (if available) GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    altitude_tensor = torch.from_numpy(altitude_array).to(device)
    
    # --- Option 1: Iterative Neighbor-Averaging (GPU Accelerated) ---
    kernel = torch.tensor([[0, 1, 0],
                           [1, 0, 1],
                           [0, 1, 0]], dtype=torch.float32, device=device).unsqueeze(0).unsqueeze(0)
    alt_t = altitude_tensor.unsqueeze(0).unsqueeze(0)
    max_iter = 1000  # safeguard against endless loops
    iter_count = 0

    # Iterative filling loop
    while (altitude_tensor == 0).any() and iter_count < max_iter:
        mask = (altitude_tensor != 0).float().unsqueeze(0).unsqueeze(0)
        sum_neighbors = F.conv2d(alt_t, kernel, padding=1)
        count_neighbors = F.conv2d(mask, kernel, padding=1)
        new_vals = sum_neighbors / (count_neighbors + 1e-8)
        update_mask = ((altitude_tensor == 0) & (count_neighbors.squeeze(0).squeeze(0) > 0))
        altitude_tensor[update_mask] = new_vals.squeeze(0).squeeze(0)[update_mask]
        alt_t = altitude_tensor.unsqueeze(0).unsqueeze(0)
        iter_count += 1

    # If the loop still leaves zeros, you can optionally apply a few rounds of max pooling for a nearest-neighbor fill.
    if (altitude_tensor == 0).any():
        print("Applying max pooling to fill remaining gaps.")
        for _ in range(10):
            filled = F.max_pool2d(altitude_tensor.unsqueeze(0).unsqueeze(0), kernel_size=3, stride=1, padding=1).squeeze(0).squeeze(0)
            if torch.equal(altitude_tensor, filled):
                break
            altitude_tensor = torch.where(altitude_tensor == 0, filled, altitude_tensor)

    
    # Create the 3D topography tensor using broadcasting
    z_values = altMin + torch.arange(z_max, dtype=torch.float32, device=device) * AltResolution
    topography_tensor = (altitude_tensor.unsqueeze(2) > z_values.view(1, 1, -1)).int()
    
    # Bring result back to CPU and save
    topography_tensor_cpu = topography_tensor.cpu()
    with open(filePath + resultFileName[13:len(resultFileName)-1], "wb") as resultFile:
        pickle.dump(topography_tensor_cpu, resultFile)
    
    return topography_tensor_cpu
