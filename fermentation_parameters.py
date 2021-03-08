# Standard libraries
import csv
from collections import OrderedDict

# Imported libraries

# My libraries


class FermentationParameters:
    """A class for Fermentation tab parameters storage"""
    def __init__(self, database):
        self.database = database

        self.parameters = OrderedDict()
        self.parameters = {'microcontroller': 'offline',
                           'sensors': 'offline',
                           'temperature_set': 0,
                           'temperature_ambient': 0,
                           'temperature_freezer': 0,
                           'temperature_ambient_offset': 0,
                           'temperature_freezer_offset': 0.2,
                           'control_ambient': False,
                           'control_freezer': False,
                           }
        self.fv_parameters = {}
        self.fermentation_parameters = []

        # Preparing variable with fermentation parameters only (for FermentationTabGUI only)
        for k in self.parameters:
            self.fermentation_parameters.append(k)

        self.extract_csv_data()

        # Preparing variable with fermentation vessels only (for RecipeTabGUI only)
        for k in self.parameters:
            if 'fv_' in k:
                self.fv_parameters[k] = self.parameters[k]

        # Checking fermentation vessels with log = True
        for k in self.parameters:
            if 'fv_' in k:
                self.parameters[k] = self.database.get_fermentation_settings_log(k)

        # Checking fermentation vessel with master = True
        fermentation_vessel = self.database.get_fermentation_settings_master()
        if fermentation_vessel and fermentation_vessel in self.parameters:
            self.parameters[fermentation_vessel.replace('fv', 'master')] = True

    def extract_csv_data(self):
        # CATIA keys for GUI elements
        filename = 'data/fermentation_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            for row in reader:
                if row[0] != 'rect':
                    self.parameters[row[0]] = False
                    if 'fv_' in row[0]:
                        self.parameters['temperature_set_' + row[0].split('_')[1]] = 0

    def verify_parameters(self, key):
        # Checking if set of parameters is allowed
        if 'master_' in key:
            self.parameters[key] = not self.parameters[key]

            # If key is True, rest should be False
            if self.parameters[key]:
                for k in self.parameters:
                    if 'master_' in k and k != key and self.parameters[k]:
                        self.parameters[k] = False
        else:
            self.parameters[key] = not self.parameters[key]
