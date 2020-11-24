# Standard libraries


# Imported libraries


# My libraries
import csv


class FermentationParameters:
    """A class for 'Fermentation' tab parameters storage"""

    def __init__(self):
        self.parameters = {}

        self.extract_csv_data()

    def extract_csv_data(self):
        filename = 'data/fermentation_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            for row in reader:
                self.parameters[row[0]] = False

    def verify_parameters(self, key):
        if key:
            self.parameters[key] = not self.parameters[key]