# Standard libraries
import csv

# Imported libraries

# My libraries


class BreweryParameters:
    """A class for Brewery tab parameters storage"""
    def __init__(self):
        self.parameters = {}
        self.extract_csv_data()

    def extract_csv_data(self):
        # CATIA keys for GUI elements
        filename = 'data/brewery_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            for row in reader:
                if row[0] != 'rect':
                    self.parameters[row[0]] = False

    def verify_parameters(self, key):
        # Check if set of parameters is allowed
        if key:
            self.parameters[key] = not self.parameters[key]
