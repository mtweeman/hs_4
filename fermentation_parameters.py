# Standard libraries
from _collections import OrderedDict

# Imported libraries

# My libraries


class FermentationParameters:
    """A class for 'Fermentation' tab parameters storage"""
    def __init__(self):
        self.parameters = OrderedDict().fromkeys(['measurement_time',
                                                  'name',
                                                  'angle',
                                                  'temperature',
                                                  'temp_units',
                                                  'battery',
                                                  'gravity',
                                                  'interval',
                                                  'rssi',
                                                  ])

        self.record_flag = False
