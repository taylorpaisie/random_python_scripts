#!/bin/env python
# Import necessary libraries
from geopy.geocoders import Nominatim

def get_lat_lon(location):
    """
    Function to get latitude and longitude for a given location
    :param location: str: Location (e.g., city name, address)
    :return: tuple: Latitude and Longitude as floats, or None if not found
    """
    # Initialize the geolocator using Nominatim service (OpenStreetMap)
    geolocator = Nominatim(user_agent="my_lat_lon_fetcher_1.0")

    # Get location data
    location_data = geolocator.geocode(location)

    # Check if location data is found
    if location_data:
        # Return the latitude and longitude
        return location_data.latitude, location_data.longitude
    else:
        # If location not found, return None
        return None

def process_locations_from_file(input_file_path, output_file_path):
    """
    Function to process locations from an input file and write their latitude and longitude to an output file in tabular format.
    :param input_file_path: str: Path to the input file containing a list of locations
    :param output_file_path: str: Path to the output file where the results will be saved
    """
    try:
        with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            locations = infile.readlines()

            # Write the header of the output file
            outfile.write("Location,Latitude,Longitude\n")

            # Process each location
            for location in locations:
                location = location.strip()  # Remove any leading/trailing whitespace
                if location:
                    coordinates = get_lat_lon(location)
                    if coordinates:
                        outfile.write(f"{location},{coordinates[0]},{coordinates[1]}\n")
                    else:
                        outfile.write(f"{location},Not found,Not found\n")

        print(f"Results have been written to {output_file_path}")

    except FileNotFoundError:
        print(f"File '{input_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    choice = input("Do you want to enter a location manually (m) or use a file (f)? ")

    if choice.lower() == 'm':
        location = input("Enter a location: ")
        coordinates = get_lat_lon(location)

        if coordinates:
            print(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
        else:
            print("Location not found.")
    elif choice.lower() == 'f':
        input_file_path = input("Enter the path to the input file containing the locations: ")
        output_file_path = input("Enter the path to the output file where results will be saved: ")
        process_locations_from_file(input_file_path, output_file_path)
    else:
        print("Invalid choice. Please select either 'm' for manual entry or 'f' for file.")
