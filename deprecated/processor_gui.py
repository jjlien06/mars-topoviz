#This script is no longer in use


"""import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import math
import os

#This Python-based GUI processes data in the following order
# 1. Using data points per degree to group data
# 2. Converts data points to KM using trigonometry and Mars' radius 
# 3. Creates tiles with length and width and KM using the converted data

# Import tkinterdnd2 for drag and drop support.
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    messagebox.showerror("Error", "Please install tkinterdnd2: pip install tkinterdnd2")
    raise

# Global variable to store the selected file path.
selected_file_path = None

def lonlat_to_km(lon, lat, ref_lon, ref_lat, planet_radius_km):
    """
    Convert a longitude/latitude coordinate (in degrees) to Cartesian (x, y) coordinates in kilometers.
    
    This function uses an equirectangular projection with a reference point.
    
    Parameters:
      lon, lat         : The longitude and latitude of the point (in degrees)
      ref_lon, ref_lat : The reference longitude and latitude (in degrees), typically from your data.
      planet_radius_km : The planet's radius in kilometers.
      
    Returns:
      (x, y) in kilometers.
    """
    # Convert degrees to radians.
    lon_rad = math.radians(lon)
    lat_rad = math.radians(lat)
    ref_lon_rad = math.radians(ref_lon)
    ref_lat_rad = math.radians(ref_lat)
    
    # Compute x and y in kilometers.
    x = planet_radius_km * (lon_rad - ref_lon_rad) * math.cos(ref_lat_rad)
    y = planet_radius_km * (lat_rad - ref_lat_rad)
    return x, y

def drop(event):
    """Handle file drop event."""
    global selected_file_path
    # event.data may contain one or more filenames; here we use the first one.
    # Remove curly braces (in case of spaces in the filename)
    file_path = event.data.strip('{}')
    if os.path.isfile(file_path):
        selected_file_path = file_path
        file_label.config(text=f"Selected File:\n{selected_file_path}")
    else:
        messagebox.showerror("Error", "Dropped item is not a file.")

def process_file():
    global selected_file_path

    # Use the dropped file if available; otherwise, ask user to select one.
    if selected_file_path:
        input_file = selected_file_path
    else:
        input_file = filedialog.askopenfilename(
            title="Select CSV file", filetypes=[("CSV Files", "*.csv")]
        )
        if not input_file:
            return

    # Get user parameters from the GUI textboxes.
    try:
        datapoints_per_group = int(entry_datapoints.get())
        tile_width = float(entry_tile_width.get())
        tile_length = float(entry_tile_length.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric parameters.")
        return

    raw_data = []
    planet_rads = []

    # -------------------------------------------------
    # Read CSV
    # -------------------------------------------------
    try:
        with open(input_file, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            
            # DEBUG: Print raw fieldnames
            print("DEBUG: Raw fieldnames:", reader.fieldnames)
            
            # Strip whitespace from each field name
            reader.fieldnames = [h.strip() for h in reader.fieldnames]
            
            # DEBUG: Print stripped fieldnames
            print("DEBUG: Stripped fieldnames:", reader.fieldnames)

            # Iterate over each row
            for row in reader:
                # DEBUG: Print the row as read
                print("DEBUG: Row before stripping keys:", row)

                # Strip whitespace from each key and each value
                row = {k.strip(): v.strip() for k, v in row.items() if k is not None}

                # DEBUG: Print the row after stripping
                print("DEBUG: Row after stripping keys:", row)

                # Try to parse the three columns we need
                try:
                    lon = float(row["LONG_EAST"])
                    lat = float(row["LAT_NORTH"])
                    topo = float(row["TOPOGRAPHY"])
                    raw_data.append((lon, lat, topo))
                    
                    # Also try to parse planet radius if available
                    try:
                        pr = float(row["PLANET_RAD"])
                        planet_rads.append(pr)
                    except:
                        pass
                    
                except KeyError as e:
                    # This means the row doesn't have the required key
                    print("DEBUG: Missing column:", e, " -> skipping row.")
                    continue
                except ValueError as e:
                    # This means we couldn't convert the value to float
                    print("DEBUG: Invalid numeric data:", e, " -> skipping row.")
                    continue

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read CSV: {e}")
        return

    # Check if we got any valid data
    if not raw_data:
        messagebox.showerror("Error", "No valid data found in CSV.")
        return

    # -------------------------------------------------
    # At this point, raw_data should contain valid rows
    # planet_rads may or may not have data
    # -------------------------------------------------

    # Group (average) the data every 'datapoints_per_group' rows.
    averaged_data = []
    group = []
    for point in raw_data:
        group.append(point)
        if len(group) == datapoints_per_group:
            avg_lon = sum(p[0] for p in group) / len(group)
            avg_lat = sum(p[1] for p in group) / len(group)
            avg_topo = sum(p[2] for p in group) / len(group)
            averaged_data.append((avg_lon, avg_lat, avg_topo))
            group = []
    # If leftover points remain, average them too
    if group:
        avg_lon = sum(p[0] for p in group) / len(group)
        avg_lat = sum(p[1] for p in group) / len(group)
        avg_topo = sum(p[2] for p in group) / len(group)
        averaged_data.append((avg_lon, avg_lat, avg_topo))

    # Use the first averaged data point as reference for coordinate conversion.
    ref_lon, ref_lat, _ = averaged_data[0]

    # Planet radius: use average if found, else fallback (e.g., Mars radius in km).
    if planet_rads:
        avg_planet_rad = sum(planet_rads) / len(planet_rads) / 1000.0  # convert m -> km
    else:
        avg_planet_rad = 3389.5  # fallback to Mars radius in km

    # -------------------------------------------------
    # Convert lat/lon to x,y in km using the new conversion function.
    # -------------------------------------------------
    km_data = []
    for lon, lat, topo in averaged_data:
        x, y = lonlat_to_km(lon, lat, ref_lon, ref_lat, avg_planet_rad)
        km_data.append((x, y, topo))

    # Determine bounding box
    xs = [pt[0] for pt in km_data]
    ys = [pt[1] for pt in km_data]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Determine how many tiles
    num_tiles_x = int(math.ceil((max_x - min_x) / tile_width))
    num_tiles_y = int(math.ceil((max_y - min_y) / tile_length))

    # Create a dictionary to hold points in each tile
    tiles = {}
    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            tiles[(i, j)] = []

    # Assign each data point to the appropriate tile
    for (x, y, topo) in km_data:
        tile_x = int((x - min_x) // tile_width)
        tile_y = int((y - min_y) // tile_length)
        tiles[(tile_x, tile_y)].append((x, y, topo))

    # Average each tile
    tile_averages = []
    for (i, j), points in tiles.items():
        if points:
            avg_x = sum(p[0] for p in points) / len(points)
            avg_y = sum(p[1] for p in points) / len(points)
            avg_topo = sum(p[2] for p in points) / len(points)
            tile_averages.append((i, j, avg_x, avg_y, avg_topo))
        else:
            tile_averages.append((i, j, None, None, None))

    # Construct output filename
    output_filename = f"{datapoints_per_group}_{tile_width}_{tile_length}.csv"
    output_path = os.path.join(os.path.dirname(input_file), output_filename)

    # Write the output CSV
    try:
        with open(output_path, "w", newline="") as csvfile_out:
            writer = csv.writer(csvfile_out)
            writer.writerow(["Tile_X", "Tile_Y", "Avg_X_km", "Avg_Y_km", "Avg_Topography"])
            for row in tile_averages:
                writer.writerow(row)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write output CSV: {e}")
        return

    messagebox.showinfo("Success", f"Output CSV created:\n{output_path}")


# ---------------------------
# Build the GUI using tkinterdnd2.Tk for drag and drop support.
# ---------------------------
root = TkinterDnD.Tk()
root.title("Data Tile Processor")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Data points per group entry.
tk.Label(frame, text="Data points per degree (group):").grid(row=0, column=0, sticky="e")
entry_datapoints = tk.Entry(frame)
entry_datapoints.grid(row=0, column=1, pady=2)

# Tile width entry.
tk.Label(frame, text="Tile width (km):").grid(row=1, column=0, sticky="e")
entry_tile_width = tk.Entry(frame)
entry_tile_width.grid(row=1, column=1, pady=2)

# Tile length entry.
tk.Label(frame, text="Tile length (km):").grid(row=2, column=0, sticky="e")
entry_tile_length = tk.Entry(frame)
entry_tile_length.grid(row=2, column=1, pady=2)

# Drag-and-Drop area for the input file.
file_label = tk.Label(frame, text="Drag and drop CSV file here", relief="groove", width=50, height=2)
file_label.grid(row=3, column=0, columnspan=2, pady=10)
file_label.drop_target_register(DND_FILES)
file_label.dnd_bind("<<Drop>>", drop)

# Process button.
process_button = tk.Button(frame, text="Process CSV", command=process_file)
process_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
"""
