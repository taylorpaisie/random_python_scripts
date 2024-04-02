#!/bin/env python
import argparse
import os
import pandas as pd
import pycountry

def get_country_code(country_name):
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_2
    except Exception:
        return None

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert country names in a CSV to their 2-letter codes.')
    parser.add_argument('--input', required=True, help='The path to the input CSV file.')
    parser.add_argument('--output', required=True, help='The path to the output CSV file.')
    parser.add_argument('--country_column', default='Country', help='The name of the column containing country names. Defaults to "Country".')
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Corrected attribute names according to the argparse setup
    input_file_path = args.input
    output_file_path = args.output

    if not os.path.exists(input_file_path):
        print(f"Error: The file '{input_file_path}' does not exist.")
        return

    try:
        data = pd.read_csv(input_file_path)
    except Exception as e:
        print(f"Error reading the file '{input_file_path}'. Ensure it is a valid CSV file. Error: {e}")
        return

    if args.country_column not in data.columns:
        print(f"Error: The specified column '{args.country_column}' does not exist in the CSV file.")
        return

    print("Processing...")
    data['Country Code'] = data[args.country_column].apply(get_country_code)

    try:
        data.to_csv(output_file_path, index=False)
        print(f"File has been successfully updated and saved as '{output_file_path}'.")
    except Exception as e:
        print(f"Error saving the file. Please check if the path is correct and you have write permissions. Error: {e}")

if __name__ == "__main__":
    main()
