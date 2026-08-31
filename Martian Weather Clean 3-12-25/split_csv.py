#!/usr/bin/env python3
import argparse
import os

# Define the chunk size (4GB)
CHUNK_SIZE = 4 * 1024 * 1024 * 1024  # 4GB in bytes

def split_csv(input_file, output_prefix, chunk_size=CHUNK_SIZE):
    with open(input_file, "rb") as infile:
        # Read the header (assumes first line is header)
        header = infile.readline()
        
        part = 1
        out_filename = f"{output_prefix}_part{part}.csv"
        outfile = open(out_filename, "wb")
        outfile.write(header)
        current_size = len(header)
        
        for line in infile:
            # If adding this line would exceed the chunk size,
            # close current file and start a new one with the header.
            if current_size + len(line) > chunk_size:
                outfile.close()
                part += 1
                out_filename = f"{output_prefix}_part{part}.csv"
                outfile = open(out_filename, "wb")
                outfile.write(header)
                current_size = len(header)
            outfile.write(line)
            current_size += len(line)
        
        outfile.close()
        print(f"Created {part} files.")

def main():
    parser = argparse.ArgumentParser(
        description="Split a large CSV file into 4GB chunks, preserving the header in each file."
    )
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument(
        "--output-prefix",
        default="output",
        help="Prefix for the output CSV files (default: output)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=CHUNK_SIZE,
        help="Chunk size in bytes (default: 4GB)",
    )
    args = parser.parse_args()
    
    if not os.path.isfile(args.input_file):
        print(f"Error: {args.input_file} does not exist!")
        return
    
    split_csv(args.input_file, args.output_prefix, args.chunk_size)

if __name__ == "__main__":
    main()
