#!/usr/bin/env python3
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Combine multiple CSV files into a single CSV file."
    )
    parser.add_argument('input_files', nargs='+', help="Paths to the input CSV files")
    parser.add_argument('-o', '--output_file', default="combined.csv",
                        help="Path for the combined CSV file (default: combined.csv)")
    args = parser.parse_args()

    # Read each CSV file into a DataFrame
    dataframes = [pd.read_csv(file) for file in args.input_files]

    # Concatenate all DataFrames, ignoring the original indices
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Write the combined DataFrame to the output CSV file
    combined_df.to_csv(args.output_file, index=False)
    print(f"Combined {len(args.input_files)} files into {args.output_file}")

if __name__ == "__main__":
    main()
