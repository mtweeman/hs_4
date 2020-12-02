# Standard libraries


# Imported libraries


# My libraries
import csv


class FermentationParameters:
    """A class for 'Fermentation' tab parameters storage"""

    def __init__(self, database):
        self.parameters = {}
        self.database = database

        self.extract_csv_data()

        for k in self.parameters:
            self.parameters[k] = self.database.get_fermentation_settings_log(k)

    def extract_csv_data(self):
        filename = 'data/fermentation_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            for row in reader:
                self.parameters[row[0]] = False

    def verify_parameters(self, key):
        self.parameters[key] = not self.parameters[key]