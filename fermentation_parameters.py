# Standard libraries
import csv

# Imported libraries

# My libraries


class FermentationParameters:
    """A class for Fermentation tab parameters storage"""
    def __init__(self, database):
        self.database = database

        self.parameters = {}
        self.fv_parameters = {}
        self.extract_csv_data()

        # Prepare variable with fermentation vessels only (for RecipeTabGui only)
        for k in self.parameters:
            if 'fv' in k:
                self.fv_parameters[k] = self.parameters[k]

        # Check fermentation vessels with log = True
        for k in self.parameters:
            if 'fv' in k:
                self.parameters[k] = self.database.get_fermentation_settings_log(k)

        # Check fermentation vessel with master = True
        name = self.database.get_ispindel_settings_master()
        if name:
            # Primary search: check if iSpindel received name has log = True for any fermentation vessel
            # log for fermentation vessel already turned on
            result = self.database.get_fermentation_settings(name, True)
            # Secondary search: check if iSpindel received name has log = False for any fermentation vessel
            # log for fermentation vessel not turned on yet, but settings for fermentation already provided
            if not result:
                result = self.database.get_fermentation_settings(name, False)
            self.parameters[result[0].replace('fv', 'master')] = True

    def extract_csv_data(self):
        # CATIA keys for GUI elements
        filename = 'data/fermentation_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            for row in reader:
                if row[0] != 'rect':
                    self.parameters[row[0]] = False

    def verify_parameters(self, key):
        # Check if set of parameters is allowed
        if 'master' in key:
            self.parameters[key] = not self.parameters[key]

            # If key is True, rest should be False
            if self.parameters[key]:
                for k in self.parameters:
                    if 'master' in k and k != key and self.parameters[k]:
                        self.parameters[k] = False
        else:
            self.parameters[key] = not self.parameters[key]