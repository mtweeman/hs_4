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
                # rect for background image dimension
                # _cam for cameras only (separate _sightglass parameter for on/off)
                if row[0] != 'rect' and '_cam' not in row[0]:
                    self.parameters[row[0]] = False

    def verify_parameters(self, key):
        # Check if set of parameters is allowed
        self.parameters[key] = not self.parameters[key]
