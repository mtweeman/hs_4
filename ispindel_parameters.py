# Standard libraries
from _collections import OrderedDict

# Imported libraries

# My libraries


class ISpindelParameters:
    """A class for iSpindel tab parameters storage"""
    def __init__(self):
        self.parameters = OrderedDict().fromkeys(['batch_number',
                                                  'batch_name',
                                                  'fermentation_vessel',
                                                  'fermentation_program',
                                                  'ispindel_name',
                                                  'temperature_offset',
                                                  'temp_units',
                                                  'interval',
                                                  'gravity_0',
                                                  'gravity_1',
                                                  'angle_0',
                                                  'angle_1',
                                                  'a',
                                                  'b',
                                                  'log'
                                                  ])

    def calculate_polynomial(self):
        if (self.parameters['gravity_0'] and self.parameters['gravity_1'] and
                self.parameters['angle_0'] and self.parameters['angle_1'] and
                self.parameters['angle_0'] != self.parameters['angle_1']):
                    self.parameters['a'] = (self.parameters['gravity_0'] - self.parameters['gravity_1']) / \
                                           (self.parameters['angle_0'] - self.parameters['angle_1'])
                    self.parameters['b'] = self.parameters['gravity_0'] -\
                                           self.parameters['a'] * self.parameters['angle_0']
