# Standard libraries
from _collections import OrderedDict

# Imported libraries


# My libraries


class ISpindelParameters:
    """A class for 'iSpindel' tab parameters storage"""
    def __init__(self):
        self.parameters = OrderedDict().fromkeys(['batch_number',
                                                  'tempera  ture_offset',
                                                  'gravity_0',
                                                  'gravity_1',
                                                  'angle_0',
                                                  'angle_1',
                                                  'a',
                                                  'b',
                                                  'battery_notification',
                                                  ])

    def calculate_polynomial(self):
        try:
            self.parameters['a'] = (self.parameters['gravity_0'] - self.parameters['gravity_1']) / \
                                   (self.parameters['angle_0'] - self.parameters['angle_1'])
            self.parameters['b'] = self.parameters['gravity_0'] - self.parameters['a'] * self.parameters['angle_0']
        except KeyError:
            pass
        except ValueError:
            pass
        except ZeroDivisionError:
            pass
