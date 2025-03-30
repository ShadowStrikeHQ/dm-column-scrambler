import argparse
import csv
import logging
import random
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command line interface.
    """
    parser = argparse.ArgumentParser(description='Scrambles the order of columns in a CSV file.')
    parser.add_argument('input_file', help='The input CSV file.')
    parser.add_argument('output_file', help='The output CSV file.')
    parser.add_argument('--seed', type=int, help='Optional seed for the random number generator (for reproducibility).')
    return parser

def scramble_columns(input_file, output_file, seed=None):
    """
    Scrambles the columns of the input CSV file and writes the result to the output CSV file.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
        seed (int, optional): Seed for the random number generator. Defaults to None.
    """
    try:
        with open(input_file, 'r', newline='') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read the header row
            data = list(reader)  # Read all the data rows

        # Seed the random number generator if a seed is provided
        if seed is not None:
            random.seed(seed)
            logging.info(f"Using seed: {seed}")

        # Generate a random permutation of column indices
        column_indices = list(range(len(header)))
        random.shuffle(column_indices)

        # Create the scrambled header
        scrambled_header = [header[i] for i in column_indices]

        # Create the scrambled data
        scrambled_data = []
        for row in data:
            scrambled_row = [row[i] for i in column_indices]
            scrambled_data.append(scrambled_row)

        # Write the scrambled data to the output file
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(scrambled_header)  # Write the scrambled header
            writer.writerows(scrambled_data)  # Write the scrambled data

        logging.info(f"Successfully scrambled columns from {input_file} to {output_file}")

    except FileNotFoundError:
        logging.error(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

def main():
    """
    Main function to parse arguments and call the scrambling function.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Input validation: Check if files are the same
    if args.input_file == args.output_file:
        logging.error("Error: Input and output files cannot be the same.")
        sys.exit(1)
        
    scramble_columns(args.input_file, args.output_file, args.seed)


if __name__ == "__main__":
    main()


# Usage Examples:
# 1. Scramble columns of input.csv and save to output.csv:
#    python main.py input.csv output.csv
#
# 2. Scramble columns with a specific seed for reproducibility:
#    python main.py input.csv output.csv --seed 42
#
# 3. If the input file doesn't exist:
#    python main.py nonexistent_file.csv output.csv
#    # This will log an error message and exit.
#
# 4. If the input and output files are the same:
#    python main.py input.csv input.csv
#    # This will log an error message and exit.