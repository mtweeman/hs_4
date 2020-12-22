# Standard libraries
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import xml.etree.ElementTree as element_tree

# Imported libraries
from PIL import Image, ImageTk

# My libraries
from xml_list_config import *


class RecipeTabGUI(Frame):
    """A class for Recipe tab creation"""

    def __init__(self, tab_control, recipe_parameters, ispindel_tab_gui, fermentation_parameters, ispindel_parameters,
                 database):
        super().__init__(tab_control)
        self.name = 'Recipe'
        self.xml_filepath = ''
        self.recipe_parameters = recipe_parameters
        self.ispindel_tab_gui = ispindel_tab_gui
        self.fermentation_parameters = fermentation_parameters
        self.ispindel_parameters = ispindel_parameters
        self.database = database

        # Images for labels
        self.img_switch_on = Image.open('images/switch_on.png')
        self.img_switch_off = Image.open('images/switch_off.png')

        self.img_switch_on_copy = self.img_switch_on.copy()
        self.img_switch_off_copy = self.img_switch_off.copy()

        self.img_l_switch_on = ImageTk.PhotoImage(image=self.img_switch_on)
        self.img_l_switch_off = ImageTk.PhotoImage(image=self.img_switch_off)

        # Names of GUI objects in the tab
        self.f_user_settings = Frame(self)
        self.f_miscs = Frame(self, borderwidth=4, relief=SOLID)
        self.f_fermentables = Frame(self, borderwidth=4, relief=SOLID)
        self.f_parameters = Frame(self, borderwidth=4, relief=SOLID)
        self.f_mash = Frame(self, borderwidth=4, relief=SOLID)
        self.f_hops = Frame(self, borderwidth=4, relief=SOLID)

        # f_user_settings
        self.l_yos = Label(self.f_user_settings, font=(None, 14), text='YOS')
        self.l_mlt_rinse = Label(self.f_user_settings, font=(None, 14), text='MLT rinse')
        self.l_mlt_cip = Label(self.f_user_settings, font=(None, 14), text='MLT CIP')
        self.l_bk_rinse = Label(self.f_user_settings, font=(None, 14), text='BK rinse')
        self.l_bk_cip = Label(self.f_user_settings, font=(None, 14), text='BK CIP')
        self.l_fv = Label(self.f_user_settings, font=(None, 14), text='FV')
        self.l_fermentation_program = Label(self.f_user_settings, font=(None, 14), text='Fermentation program')
        self.b_import_recipe = Button(self.f_user_settings, font=(None, 14), text='Import recipe',
                                      command=self.import_xml_recipe)
        self.t_yos = Label(self.f_user_settings, image=self.img_l_switch_off)
        self.t_mlt_rinse = Label(self.f_user_settings, image=self.img_l_switch_off)
        self.t_mlt_cip = Label(self.f_user_settings, image=self.img_l_switch_off)
        self.t_bk_rinse = Label(self.f_user_settings, image=self.img_l_switch_off)
        self.t_bk_cip = Label(self.f_user_settings, image=self.img_l_switch_off)
        self.cb_fv = ttk.Combobox(self.f_user_settings, font=(None, 14),
                                  values=tuple(self.fermentation_parameters.fv_parameters),
                                  state='readonly')
        self.cb_fermentation_program = ttk.Combobox(self.f_user_settings, font=(None, 14),
                                                    values=self.database.get_columns('Fermentation_programs'),
                                                    state='readonly')
        self.l_recipe_name = Label(self.f_user_settings, font=(None, 20, 'bold'))

        # f_miscs
        self.l_miscs_name = Label(self.f_miscs, font=(None, 20, 'bold'), text='')
        self.l_misc_name = Label(self.f_miscs, font=(None, 14), text='', justify=LEFT)
        self.l_misc_use = Label(self.f_miscs, font=(None, 14), text='', justify=LEFT)
        self.l_misc_amount = Label(self.f_miscs, font=(None, 14), text='', justify=LEFT)
        self.l_misc_time = Label(self.f_miscs, font=(None, 14), text='', justify=LEFT)

        # f_fermentables
        self.l_fermentables_name = Label(self.f_fermentables, font=(None, 20, 'bold'), text='')
        self.l_fermentable_name = Label(self.f_fermentables, font=(None, 14), text='', justify=LEFT)
        self.l_fermentable_amount = Label(self.f_fermentables, font=(None, 14), text='', justify=LEFT)

        # f_parameters
        self.l_parameters_name = Label(self.f_parameters, font=(None, 20, 'bold'), text='')
        self.l_parameter_name = Label(self.f_parameters, font=(None, 14), text='', justify=LEFT)
        self.l_parameter_value = Label(self.f_parameters, font=(None, 14), text='', justify=LEFT)

        # f_mash
        self.l_mash_name = Label(self.f_mash, font=(None, 20, 'bold'), text='')
        self.l_mash_step_name = Label(self.f_mash, font=(None, 14), text='', justify=LEFT)
        self.l_mash_step_time = Label(self.f_mash, font=(None, 14), text='', justify=LEFT)
        self.l_mash_step_temp = Label(self.f_mash, font=(None, 14), text='', justify=LEFT)

        # f_hops
        self.l_hops_name = Label(self.f_hops, font=(None, 20, 'bold'), text='')
        self.l_hop_name = Label(self.f_hops, font=(None, 14), text='', justify=LEFT)
        self.l_hop_use = Label(self.f_hops, font=(None, 14), text='', justify=LEFT)
        self.l_hop_amount = Label(self.f_hops, font=(None, 14), text='', justify=LEFT)
        self.l_hop_time = Label(self.f_hops, font=(None, 14), text='', justify=LEFT)

        # Creating list with all frames for looping
        self.f_frames = [self.f_miscs,
                         self.f_fermentables,
                         self.f_parameters,
                         self.f_mash,
                         self.f_hops,
                         ]

        # Creatiing list with all toggles for looping
        self.t_toggles = [self.t_yos,
                          self.t_mlt_rinse,
                          self.t_mlt_cip,
                          self.t_bk_rinse,
                          self.t_bk_cip,
                          ]

        # Adding GUI objects to the grid
        self.f_user_settings.grid(row=0, columnspan=3, sticky=N+W+E)

        # f_user_settings
        self.l_yos.grid(row=0, column=1)
        self.l_mlt_rinse.grid(row=0, column=2)
        self.l_mlt_cip.grid(row=0, column=3)
        self.l_bk_rinse.grid(row=0, column=4)
        self.l_bk_cip.grid(row=0, column=5)
        self.l_fv.grid(row=0, column=6)
        self.l_fermentation_program.grid(row=0, column=7)
        self.b_import_recipe.grid(row=1, column=0)
        self.t_yos.grid(row=1, column=1)
        self.t_mlt_rinse.grid(row=1, column=2)
        self.t_mlt_cip.grid(row=1, column=3)
        self.t_bk_rinse.grid(row=1, column=4)
        self.t_bk_cip.grid(row=1, column=5)
        self.cb_fv.grid(row=1, column=6)
        self.cb_fermentation_program.grid(row=1, column=7)
        self.l_recipe_name.grid(row=3, columnspan=self.f_user_settings.grid_size()[0])

        # f_miscs
        self.l_miscs_name.grid(row=0, columnspan=4)
        self.l_misc_name.grid(row=1, column=0, sticky=W)
        self.l_misc_use.grid(row=1, column=1, sticky=W)
        self.l_misc_amount.grid(row=1, column=2, sticky=W)
        self.l_misc_time.grid(row=1, column=3, sticky=W)

        # f_fermentables
        self.l_fermentables_name.grid(row=0, columnspan=2)
        self.l_fermentable_name.grid(row=1, column=0, sticky=W)
        self.l_fermentable_amount.grid(row=1, column=1, sticky=W)

        # f_parameters
        self.l_parameters_name.grid(row=0, columnspan=2)
        self.l_parameter_name.grid(row=1, column=0, sticky=W)
        self.l_parameter_value.grid(row=1, column=1, sticky=W)

        # f_mash
        self.l_mash_name.grid(row=0, columnspan=3)
        self.l_mash_step_name.grid(row=1, column=0, sticky=W)
        self.l_mash_step_time.grid(row=1, column=1, sticky=W)
        self.l_mash_step_temp.grid(row=1, column=2, sticky=W)

        # f_hops
        self.l_hops_name.grid(row=0, columnspan=4)
        self.l_hop_name.grid(row=1, column=0, sticky=W)
        self.l_hop_use.grid(row=1, column=1, sticky=W)
        self.l_hop_amount.grid(row=1, column=2, sticky=W)
        self.l_hop_time.grid(row=1, column=3, sticky=W)

        # Adding commands to GUI objects
        self.t_yos.bind('<Button-1>', lambda event, key='yos': self.toggle_switch(key))
        self.t_mlt_rinse.bind('<Button-1>', lambda event, key='mlt_rinse': self.toggle_switch(key))
        self.t_mlt_cip.bind('<Button-1>', lambda event, key='mlt_cip': self.toggle_switch(key))
        self.t_bk_rinse.bind('<Button-1>', lambda event, key='bk_rinse': self.toggle_switch(key))
        self.t_bk_cip.bind('<Button-1>', lambda event, key='bk_cip': self.toggle_switch(key))
        self.cb_fv.bind('<<ComboboxSelected>>',
                        lambda event: self.ispindel_tab_gui.external_parameters_update(
                            fermentation_vessel=self.cb_fv.get()))
        self.cb_fermentation_program.bind('<<ComboboxSelected>>',
                                          lambda event: self.ispindel_tab_gui.external_parameters_update(
                                              fermentation_program=self.cb_fermentation_program.get()))

        # Setting rows and columns properties
        for i in range(1, 3):
            self.rowconfigure(i, weight=1)
        for i in range(self.grid_size()[0]):
            self.columnconfigure(i, weight=1, uniform='column')

        for i in range(self.f_user_settings.grid_size()[1]):
            self.f_user_settings.rowconfigure(i, weight=1, uniform='row')
        for i in range(self.f_user_settings.grid_size()[0]):
            self.f_user_settings.columnconfigure(i, weight=1, uniform='column')

        for f in self.f_frames:
            for i in range(f.grid_size()[0]):
                f.columnconfigure(i, weight=1)

        # Adding separators to columns in frames
        for f in self.f_frames:
            for i in range(f.grid_size()[0]-1):
                ttk.Separator(f, orient=VERTICAL).grid(row=1, column=i, padx=20, sticky=N+S+E)

    def extract_xml_data(self):
        # Open XML file
        xml_filepath = filedialog.askopenfilename()
        recipe = element_tree.parse(xml_filepath).getroot()
        xml_dict = XmlDictConfig(recipe)

        # Extract data for recipe_parameters
        self.recipe_parameters.extract_xml_data(xml_dict)

        # Extract parameters for ispindel_tab_gui
        self.ispindel_tab_gui.external_parameters_update(
            batch_number=int(xml_dict['RECIPE']['NAME'].split()[0][1:]),
            og=self.recipe_parameters.parameters['OG'],
            batch_name=xml_dict['RECIPE']['NAME'].strip(xml_dict['RECIPE']['NAME'].split()[0] + ' '),
        )

    def print_parameters(self):
        # Prepare texts for GUI objects
        miscs_texts = {}
        fermentables_texts = {}
        parameters_texts = {'NAME': 'NAME', 'VALUE': 'VALUE'}
        mash_texts = {}
        hops_texts = {}

        # Creating list with all text labels for looping
        texts = [miscs_texts,
                 fermentables_texts,
                 mash_texts,
                 hops_texts,
                 ]

        # Create text from recipe parameters (lists)
        for i, current_list in enumerate(self.recipe_parameters.lists):
            if current_list:
                for current_dict in current_list:
                    if not texts[i]:
                        for k in current_dict:
                            texts[i][k] = k
                    for k, v in current_dict.items():
                        texts[i][k] += '\n' + str(v)

        # Create text from recipe parameters (dictionary)
        if self.recipe_parameters.parameters:
            for k, v in self.recipe_parameters.parameters.items():
                if k != 'recipe_name' and k != 'equipment_name' and k != 'mash_program':
                    parameters_texts['NAME'] += '\n' + k
                    parameters_texts['VALUE'] += '\n' + str(v)

        # Adding texts to GUI objects
        self.l_recipe_name.config(text=self.recipe_parameters.parameters['recipe_name'])

        # f_miscs
        self.l_miscs_name.config(text='Minerals & Boil additions')
        self.l_misc_name.config(text=miscs_texts['NAME'])
        self.l_misc_use.config(text=miscs_texts['USE'])
        self.l_misc_amount.config(text=miscs_texts['AMOUNT'])
        self.l_misc_time.config(text=miscs_texts['TIME'])

        # f_fermentables
        self.l_fermentables_name.config(text='Grains: ' + str(self.recipe_parameters.parameters['GRAINS_WEIGHT']))
        self.l_fermentable_name.config(text=fermentables_texts['NAME'])
        self.l_fermentable_amount.config(text=fermentables_texts['AMOUNT'])

        # f_parameters
        self.l_parameters_name.config(text='Parameters, equipment: ' +
                                           self.recipe_parameters.parameters['equipment_name'])
        self.l_parameter_name.config(text=parameters_texts['NAME'])
        self.l_parameter_value.config(text=parameters_texts['VALUE'])

        # f_mash
        self.l_mash_name.config(text='Mash program: ' + self.recipe_parameters.parameters['mash_program'])
        self.l_mash_step_name.config(text=mash_texts['NAME'])
        self.l_mash_step_time.config(text=mash_texts['STEP_TIME'])
        self.l_mash_step_temp.config(text=mash_texts['STEP_TEMP'])

        # f_hops
        self.l_hops_name.config(text='Hops: ' + str(self.recipe_parameters.parameters['HOPS_WEIGHT']))
        self.l_hop_name.config(text=hops_texts['NAME'])
        self.l_hop_use.config(text=hops_texts['USE'])
        self.l_hop_amount.config(text=hops_texts['AMOUNT'])
        self.l_hop_time.config(text=hops_texts['TIME'])

        # Adding GUI objects to the grid
        self.f_miscs.grid(row=1, column=0, sticky=NSEW)
        self.f_fermentables.grid(row=1, column=1, sticky=NSEW)
        self.f_parameters.grid(row=1, column=2, rowspan=2, sticky=NSEW)
        self.f_mash.grid(row=2, column=0, sticky=NSEW)
        self.f_hops.grid(row=2, column=1, sticky=NSEW)

    def import_xml_recipe(self):
        self.extract_xml_data()
        self.print_parameters()
        self.update_toggles()

    def update_toggles(self):
        for i, toggle in enumerate(self.t_toggles):
            if list(self.recipe_parameters.user_parameters.items())[i][1]:
                toggle.config(image=self.img_l_switch_on)
            else:
                toggle.config(image=self.img_l_switch_off)

    def toggle_switch(self, key):
        self.recipe_parameters.verify_user_parameters(key)
        self.update_toggles()
