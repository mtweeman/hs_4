# Standard libraries
import datetime
from _collections import OrderedDict

# Imported libraries

# My libraries
import xml_list_config


class RecipeParameters:
    """A class for Recipe tab parameters storage"""
    def __init__(self):
        # Lists and dictionaries for XML parameters
        self.miscs = []
        self.fermentables = []
        self.parameters = {}
        self.mash = []
        self.hops = []
        self.user_parameters = OrderedDict()
        self.user_parameters = {'yos': False,
                                'mlt_rinse': False,
                                'mlt_cip': False,
                                'bk_rinse': False,
                                'bk_cip': False,
                                }

        # Create a list of lists for looping
        self.lists = [self.miscs,
                      self.fermentables,
                      self.mash,
                      self.hops,
                      ]

    def extract_xml_data(self, xml_dict):
        current_item = {}

        # Clear earlier values
        for element in self.lists:
            if element:
                element.clear()

        # Extract data from XML file
        # Miscs
        if 'MISCS' in xml_dict['RECIPE']:
            # Convert to list if dict
            if isinstance(xml_dict['RECIPE']['MISCS']['MISC'], xml_list_config.XmlDictConfig):
                xml_dict['RECIPE']['MISCS']['MISC'] = list([xml_dict['RECIPE']['MISCS']['MISC']])

            # Extract data
            for v in xml_dict['RECIPE']['MISCS']['MISC']:
                current_item['NAME'] = v['NAME']
                if v['USE']:
                    current_item['USE'] = v['USE']
                else:
                    current_item['USE'] = 'Sparge'
                current_item['AMOUNT'] = round(1e3 * float(v['AMOUNT']), 2)
                current_item['TIME'] = datetime.timedelta(minutes=int(round(float(v['TIME']), 0)))
                self.miscs.append(current_item.copy())

                # Turn on YOS when Baker's Dry Yeast found
                if v['NAME'] == "Baker's Dry Yeast" and not self.user_parameters['yos']:
                    self.user_parameters['yos'] = True

            # Sort
            order = {'Mash': 0, 'Sparge': 1, 'Boil': 2, 'Primary': 3, 'Secondary': 4, 'Bottling': 5}
            self.miscs.sort(key=lambda k: (order[k['USE']], -k['TIME']))

        # Fermentables
        current_item.clear()
        self.parameters['GRAINS_WEIGHT'] = 0.0

        if 'FERMENTABLES' in xml_dict['RECIPE']:
            # Convert to list if dict
            if isinstance(xml_dict['RECIPE']['FERMENTABLES']['FERMENTABLE'], xml_list_config.XmlDictConfig):
                xml_dict['RECIPE']['FERMENTABLES']['FERMENTABLE'] =\
                    list([xml_dict['RECIPE']['FERMENTABLES']['FERMENTABLE']])

            # Extract data
            for v in xml_dict['RECIPE']['FERMENTABLES']['FERMENTABLE']:
                current_item['NAME'] = v['NAME']
                current_item['AMOUNT'] = round(float(v['AMOUNT']), 2)
                self.fermentables.append(current_item.copy())

                # Count total amount of grain
                if v['TYPE'] == 'Grain':
                    self.parameters['GRAINS_WEIGHT'] += current_item['AMOUNT']

            self.parameters['GRAINS_WEIGHT'] = round(self.parameters['GRAINS_WEIGHT'], 2)
            self.fermentables.sort(key=lambda k: -k['AMOUNT'])

        # Mash
        current_item.clear()

        if 'MASH_STEPS' in xml_dict['RECIPE']['MASH']:
            # Convert to list if dict
            if isinstance(xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP'], xml_list_config.XmlDictConfig):
                xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP'] =\
                    list([xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP']])

            # Extract data
            for v in xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP']:
                current_item['NAME'] = v['NAME']
                current_item['STEP_TIME'] = datetime.timedelta(minutes=int(round(float(v['STEP_TIME']), 0)))
                current_item['STEP_TEMP'] = int(round(float(v['STEP_TEMP']), 0))
                self.mash.append(current_item.copy())

        # Hops
        current_item.clear()
        self.parameters['HOPS_WEIGHT'] = 0

        if 'HOPS' in xml_dict['RECIPE']:
            # Convert to list if dict
            if isinstance(xml_dict['RECIPE']['HOPS']['HOP'], xml_list_config.XmlDictConfig):
                xml_dict['RECIPE']['HOPS']['HOP'] = list([xml_dict['RECIPE']['HOPS']['HOP']])

            for v in xml_dict['RECIPE']['HOPS']['HOP']:
                if v['USE'] == 'Mash' or v['USE'] == 'First Wort' or v['USE'] == 'Boil' or v['USE'] == 'Aroma':
                    current_item['NAME'] = v['NAME']
                    current_item['USE'] = v['USE']
                    current_item['AMOUNT'] = int(round(1e3 * float(v['AMOUNT']), 0))
                    current_item['TIME'] = datetime.timedelta(minutes=int(round(float(v['TIME']), 0)))
                    self.parameters['HOPS_WEIGHT'] += current_item['AMOUNT']
                    self.hops.append(current_item.copy())

            order = {'Mash': 0, 'First Wort': 1, 'Boil': 2, 'Aroma': 3}
            self.hops.sort(key=lambda k: (order[k['USE']], -k['TIME']))

        # Parameters
        self.parameters['GRAIN_TEMP'] = round(float(xml_dict['RECIPE']['MASH']['GRAIN_TEMP']), 2)
        self.parameters['WATER_GRAIN_RATIO'] = \
            round(float(xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP'][0]['WATER_GRAIN_RATIO'].
                        split()[0].replace(',', '.')), 1)
        self.parameters['INFUSE_VOLUME'] = round(
            float(xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP'][0]['DISPLAY_INFUSE_AMT'].split()[0]), 2)
        self.parameters['INFUSE_TEMP'] = round(
            float(xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP'][0]['INFUSE_TEMP'].split()[0]), 1)
        self.parameters['MLT_DEADSPACE_VOLUME'] = round(float(xml_dict['RECIPE']['EQUIPMENT.LAUTER_DEADSPACE']), 2)

        self.parameters['SPARGE_VOLUME'] = round(float(xml_dict['RECIPE']['SPARGE_VOLUME'].split()[0]), 2)

        self.parameters['BOIL_VOLUME'] = round(float(xml_dict['RECIPE']['BOIL_SIZE']), 2)
        self.parameters['PRE_BOIL_OG'] = round(float(xml_dict['RECIPE']['PRE_BOIL_OG'].split()[0]), 3)
        self.parameters['BOIL_TIME'] = datetime.timedelta(minutes=int(round(float(xml_dict['RECIPE']['BOIL_TIME']), 0)))

        self.parameters['TRUB_CHILLER_VOLUME'] = round(float(xml_dict['RECIPE']['EQUIPMENT.TRUB_CHILLER_LOSS']), 2)
        self.parameters['COOLING_SHRINKAGE_PERCENTAGE'] =\
            round(float(xml_dict['RECIPE']['EQUIPMENT.COOLING_LOSS_PCT']), 2)
        self.parameters['EVAPORATION_PERCENTAGE'] = round(float(xml_dict['RECIPE']['EVAP_RATE']), 2)
        self.parameters['POST_BOIL_VOLUME'] =\
            round(self.parameters['BOIL_VOLUME'] -
                  (self.parameters['EVAPORATION_PERCENTAGE'] / 100 * self.parameters['BOIL_VOLUME'] *
                   int(round(float(xml_dict['RECIPE']['BOIL_TIME']), 0)) / 60.0), 2)
        self.parameters['KNOCKOUT_VOLUME'] =\
            round(self.parameters['POST_BOIL_VOLUME'] *
                  (1 - self.parameters['COOLING_SHRINKAGE_PERCENTAGE'] / 100), 2)

        self.parameters['BATCH_VOLUME'] = round(float(xml_dict['RECIPE']['BATCH_SIZE']), 2)
        self.parameters['FERMENTATION_TEMP'] = round(float(xml_dict['RECIPE']['PRIMARY_TEMP']), 1)
        self.parameters['OG'] = round(float(xml_dict['RECIPE']['EST_OG'].split()[0]), 3)
        self.parameters['IBU'] = round(float(xml_dict['RECIPE']['IBU'].split()[0]), 1)

        self.parameters['recipe_name'] = xml_dict['RECIPE']['NAME']
        self.parameters['equipment_name'] = xml_dict['RECIPE']['EQUIPMENT.NAME']
        self.parameters['mash_program'] = xml_dict['RECIPE']['MASH']['NAME']

    def verify_user_parameters(self, key):
        # Check if set of parameters is allowed
        if key == 'yos':
            self.user_parameters[key] = not self.user_parameters[key]
        elif key == 'mlt_rinse' or key == 'bk_rinse':
            if not self.user_parameters[key]:
                self.user_parameters[key] = True
            else:
                if key == 'mlt_rinse' and self.user_parameters['mlt_cip']:
                    self.user_parameters['mlt_cip'] = False
                elif key == 'bk_rinse' and self.user_parameters['bk_cip']:
                    self.user_parameters['bk_cip'] = False
                self.user_parameters[key] = False
        elif key == 'mlt_cip' or key == 'bk_cip':
            if self.user_parameters[key]:
                self.user_parameters[key] = False
            else:
                if key == 'mlt_cip' and not self.user_parameters['mlt_rinse']:
                    self.user_parameters['mlt_rinse'] = True
                elif key == 'bk_cip' and not self.user_parameters['bk_rinse']:
                    self.user_parameters['bk_rinse'] = True
                self.user_parameters[key] = True
