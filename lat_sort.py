#!/usr/bin/env python3
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Sort a CSV file by the LAT_NORTH column in ascending order."
    )
    parser.add_argument('input_file', help="Path to the input CSV file")
    parser.add_argument('output_file', help="Path to save the sorted CSV file")
    parser.add_argument('--sort_col', default='LAT_NORTH', 
                        help="Column to sort by (default: LAT_NORTH)")

    args = parser.parse_args()

    # Read the CSV file
    df = pd.read_csv(args.input_file)

    # Sort the DataFrame by the specified column in ascending order
    df_sorted = df.sort_values(by=args.sort_col, ascending=True)

    # Write the sorted data to the output CSV file
    df_sorted.to_csv(args.output_file, index=False)
    print(f"Data sorted by {args.sort_col} and saved to {args.output_file}")

if __name__ == "__main__":
    main()
