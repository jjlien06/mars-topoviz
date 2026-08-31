#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np

def bin_data(df, bin_size, points_per_bin):
    # Clean up column names (remove any extra whitespace)
    df.columns = [col.strip() for col in df.columns]
    
    # Ensure coordinate columns are numeric
    df['LONG_EAST'] = pd.to_numeric(df['LONG_EAST'], errors='coerce')
    df['LAT_NORTH'] = pd.to_numeric(df['LAT_NORTH'], errors='coerce')
    
    # Compute the bin for each coordinate.
    # For each row, the bin is the floor of (coordinate / bin_size) multiplied back by bin_size.
    df['lon_bin'] = np.floor(df['LONG_EAST'] / bin_size) * bin_size
    df['lat_bin'] = np.floor(df['LAT_NORTH'] / bin_size) * bin_size

    # List to store binned (or sampled) data
    binned_list = []
    
    # Group the data by the calculated bin coordinates
    grouped = df.groupby(['lon_bin', 'lat_bin'])
    
    for (lon, lat), group in grouped:
        if len(group) > points_per_bin:
            # More points than needed: randomly sample the target number of rows
            group_sample = group.sample(n=points_per_bin, random_state=42)
        else:
            # If fewer points are available, keep the entire group
            group_sample = group
        binned_list.append(group_sample)
    
    # Combine all the groups back into one DataFrame
    return pd.concat(binned_list)

def main():
    parser = argparse.ArgumentParser(
        description='Bin Mars data into degree by degree boxes with a specified number of data points per box.'
    )
    parser.add_argument('input_file', type=str, help='Path to the input CSV file containing Mars data')
    parser.add_argument('--bin_size', type=float, default=1.0,
                        help='The size (in degrees) of each square bin (default: 1 degree)')
    parser.add_argument('--points_per_bin', type=int, default=10,
                        help='Target number of data points per bin (default: 10)')
    parser.add_argument('--output_file', type=str, default='binned_data.csv',
                        help='Output CSV file (default: binned_data.csv)')
    
    args = parser.parse_args()
    
    # Read the CSV file (skip any extra spaces after delimiters)
    df = pd.read_csv(args.input_file, skipinitialspace=True)
    
    # Bin the data and optionally downsample bins with too many points
    binned_df = bin_data(df, args.bin_size, args.points_per_bin)
    
    # Save the result to a new CSV file
    binned_df.to_csv(args.output_file, index=False)
    print(f"Binned data saved to {args.output_file}")

if __name__ == "__main__":
    main()