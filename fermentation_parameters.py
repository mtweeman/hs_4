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

        # Set fermentation vessels with log
        for k in self.parameters:
            self.parameters[k] = self.database.get_fermentation_settings_log(k)

        # Set fermentation vessel with master
        name = self.database.get_ispindel_settings_master()
        if name:
            result = self.database.get_fermentation_settings(name, True)
            if not result:
                result = self.database.get_fermentation_settings(name, False)
            self.parameters[result[0].replace('fv', 'master')] = True

    def extract_csv_data(self):
        filename = 'data/fermentation_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            for row in reader:
                self.parameters[row[0]] = False

    def verify_parameters(self, key):
        if 'master' in key:
            self.parameters[key] = not self.parameters[key]

            if self.parameters[key]:
                for k in self.parameters:
                    if 'master' in k and k != key:
                        self.parameters[k] = False
        else:
            self.parameters[key] = not self.parameters[key]