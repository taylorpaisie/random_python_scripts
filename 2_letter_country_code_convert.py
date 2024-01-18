#!/bin/env python
import sys, os
import pandas as pd
import pycountry

def get_country_code(country_name):
    try:
        country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_2
    except Exception:
        return None

# Load the CSV file
file_path = sys.argv[1] 
data = pd.read_csv(file_path)

# Adding a new column with the 2-letter country codes
data['Country Code'] = data['Country'].apply(get_country_code)

# Saving the updated DataFrame to a new CSV file
updated_file_path = sys.argv[2]
data.to_csv(updated_file_path, index=False)


