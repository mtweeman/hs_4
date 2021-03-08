# Standard libraries
import os
import datetime

# Imported libraries
import pyodbc as db

# My libraries


class Database:
    """A class for database handling"""
    def __init__(self):
        # Database setup
        self.database_path = os.getcwd() + r"/hajle_silesia_db.accdb"
        self.connection_string = ("Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
                                  "DBQ=" + self.database_path + ";")

    def establish_connection(self):
        self.db_connection = db.connect(self.connection_string, autocommit=True)
        self.cursor = self.db_connection.cursor()

    def terminate_connection(self):
        self.cursor.close()
        self.db_connection.close()

    def execute_fermentation(self, batch_number, socket_message):
        self.establish_connection()

        fermentation = str(batch_number) + '_Ferm'

        # Preparing query for table creation
        self.query = ("""CREATE TABLE """ + fermentation +
                      """(id AUTOINCREMENT PRIMARY KEY NOT NULL,""" +
                      """measurement_time DATETIME NOT NULL,""" +
                      """angle DOUBLE NOT NULL,""" +
                      """temperature DOUBLE NOT NULL,""" +
                      """battery DOUBLE NOT NULL,""" +
                      """gravity DOUBLE NOT NULL,""" +
                      """rssi SHORT NOT NULL);""")

        # Checking existence / create table
        if not self.cursor.tables(table=fermentation, tableType='TABLE').fetchone():
            self.cursor.execute(self.query)

        # Preparing query
        self.query = """INSERT INTO """ + fermentation + """("""

        for k in socket_message:
            self.query += k + ','
        self.query = self.query[:-1]

        self.query += """) VALUES ("""

        for k in socket_message:
            self.query += '?,'
        self.query = self.query[:-1]
        self.query += """);"""

        if self.cursor.tables(table=fermentation, tableType='TABLE').fetchone():
            self.cursor.execute(self.query, tuple(socket_message.values()))

        self.terminate_connection()

    def execute_fermentation_settings(self, ispindel_parameters):
        self.establish_connection()

        # Preparing query
        self.query = """INSERT INTO Fermentation_settings("""

        for k in ispindel_parameters.parameters:
            self.query += k + ','
        self.query = self.query[:-1]

        self.query += """) VALUES ("""

        for k in ispindel_parameters.parameters:
            self.query += '?,'
        self.query = self.query[:-1]
        self.query += """);"""

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, tuple(ispindel_parameters.parameters.values()))

        self.terminate_connection()

    def get_ispindel_settings_battery_notification(self, ispindel_name):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT battery_notification """ +
                      """FROM iSpindel_settings """ +
                      """WHERE name=?;""")

        if self.cursor.tables(table='iSpindel_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, ispindel_name)

        battery_notification = self.cursor.fetchone()

        self.terminate_connection()

        if battery_notification:
            return battery_notification[0]
        else:
            return None

    def execute_ispindel_settings_battery_notification(self, ispindel_name, battery_notification):
        self.establish_connection()

        # Preparing query
        self.query = ("""UPDATE iSpindel_settings """ +
                      """SET battery_notification=? """
                      """WHERE name=?;""")

        if self.cursor.tables(table='iSpindel_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, battery_notification, ispindel_name)

        self.terminate_connection()

    def get_ispindel_settings_temperature_offset(self, ispindel_name):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT temperature_offset """ +
                      """FROM iSpindel_settings """ +
                      """WHERE name=?;""")

        if self.cursor.tables(table='iSpindel_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, ispindel_name)

        temperature_offset = self.cursor.fetchone()

        self.terminate_connection()

        if temperature_offset:
            return temperature_offset[0]
        else:
            return None

    def get_fermentation_settings(self, ispindel_name, log):
        # Searching master if log = False
        if not log:
            fermentation_vessel = self.get_fermentation_settings_master()
            if not fermentation_vessel:
                return None

        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT fermentation_vessel, batch_number, a, b, temperature_offset, log, batch_name, """ +
                      """gravity_1 """ +
                      """FROM Fermentation_settings """ +
                      """WHERE log=? AND ispindel_name=? """ +
                      """ORDER BY batch_number DESC;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, log, ispindel_name)

        result = self.cursor.fetchone()

        self.terminate_connection()

        if result:
            return result
        else:
            return None

    def get_fermentation_settings_master(self):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT fermentation_vessel """ +
                      """FROM Fermentation_settings """ +
                      """WHERE master=True;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query)

        fermentation_vessel = self.cursor.fetchone()

        self.terminate_connection()

        if fermentation_vessel:
            return fermentation_vessel[0]
        else:
            return None

    def get_fermentation_settings_start(self, key):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT start """ +
                      """FROM Fermentation_settings """ +
                      """WHERE batch_number=?;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, key)

        start = self.cursor.fetchone()

        self.terminate_connection()

        if start:
            return start[0]
        else:
            return None

    def execute_fermentation_settings_start(self, key):
        self.establish_connection()

        # Preparing query
        self.query = ("""UPDATE Fermentation_settings """ +
                      """SET start=? """ +
                      """WHERE batch_number=?;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, datetime.datetime.now(), key)

        self.terminate_connection()

    def execute_fermentation_settings_log(self, fermentation_vessel, log):
        self.establish_connection()

        # Preparing query
        if log:
            self.query = ("""UPDATE Fermentation_settings """ +
                          """SET log=?, pitch=? """ +
                          """WHERE batch_number=(SELECT TOP 1 batch_number """ +
                                              """FROM Fermentation_settings """ +
                                              """WHERE fermentation_vessel=? """ +
                                              """ORDER BY batch_number DESC);""")
        else:
            self.query = ("""UPDATE Fermentation_settings """ +
                          """SET log=?, finish=? """ +
                          """WHERE batch_number=(SELECT TOP 1 batch_number """ +
                                              """FROM Fermentation_settings """ +
                                              """WHERE fermentation_vessel=? """ +
                                              """ORDER BY batch_number DESC);""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, log, datetime.datetime.now(), fermentation_vessel)

        self.terminate_connection()

    def execute_fermentation_settings_master(self, fermentation_vessel, master):
        self.establish_connection()

        # Preparing query
        self.query = ("""UPDATE Fermentation_settings """ +
                      """SET master=False """ +
                      """WHERE master=True;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query)

        if master:
            self.query = ("""UPDATE Fermentation_settings """ +
                          """SET master=True """ +
                          """WHERE batch_number=(SELECT TOP 1 batch_number """ +
                                              """FROM Fermentation_settings """ +
                                              """WHERE fermentation_vessel=? """ +
                                              """ORDER BY batch_number DESC);""")

            if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
                self.cursor.execute(self.query, fermentation_vessel)

        self.terminate_connection()

    def get_fermentation_settings_batch_name(self, fermentation_vessel):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT batch_name """ +
                      """FROM Fermentation_settings """ +
                      """WHERE fermentation_vessel=? """ +
                      """AND master=True """ +
                      """ORDER BY batch_number DESC;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, fermentation_vessel)

        result = self.cursor.fetchone()

        self.terminate_connection()

        if result:
            return result[0]
        else:
            return None

    def get_fermentation_programs_temperature(self, fermentation_program, day):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT * """ +
                      """FROM Fermentation_programs """ +
                      """WHERE program=?;""")

        if self.cursor.tables(table='Fermentation_programs', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, fermentation_program)

        result = self.cursor.fetchone()
        result = result[1:]

        self.terminate_connection()

        if result:
            return result[day]
        else:
            return None

    def get_fermentation_settings_fermentation_data(self, fermentation_vessel, log=True):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT fermentation_program, fermentation_temperature, pitch, start """ +
                      """FROM Fermentation_settings """ +
                      """WHERE fermentation_vessel=? """ +
                      """AND log=? """ +
                      """ORDER BY batch_number DESC;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, fermentation_vessel, log)

        result = self.cursor.fetchone()

        self.terminate_connection()

        if result:
            return result
        else:
            return None

    def get_fermentation_settings_batch_number_batch_name(self, fermentation_vessel):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT batch_number, batch_name """ +
                      """FROM Fermentation_settings """ +
                      """WHERE fermentation_vessel=? """ +
                      """AND log=True """ +
                      """ORDER BY batch_number DESC;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, fermentation_vessel)

        result = self.cursor.fetchone()

        self.terminate_connection()

        if result:
            return result
        else:
            return None

    def get_fermentation_settings_log(self, fermentation_vessel):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT log """ +
                      """FROM Fermentation_settings """ +
                      """WHERE fermentation_vessel=? """ +
                      """AND log=True """ +
                      """ORDER BY batch_number DESC;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, fermentation_vessel)

        fermentation_log = self.cursor.fetchone()

        self.terminate_connection()

        if fermentation_log:
            return fermentation_log[0]
        else:
            return None

    def get_fermentation_settings_ispindel_name(self, fermentation_vessel):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT ispindel_name """ +
                      """FROM Fermentation_settings """ +
                      """WHERE fermentation_vessel=? """ +
                      """ORDER BY batch_number DESC;""")

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, fermentation_vessel)

        ispindel_name = self.cursor.fetchone()

        self.terminate_connection()

        if ispindel_name:
            return ispindel_name[0]
        else:
            return None

    def get_tables(self, table_type):
        results = []

        self.establish_connection()

        for row in self.cursor.tables():
            if '_' + table_type[:4] in row.table_name:
                results.append(row.table_name)

        self.terminate_connection()

        if results:
            return results
        else:
            return None

    def get_columns(self, table):
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT * """ +
                      """FROM %s """ +
                      """;""") % table

        if self.cursor.tables(table=table, tableType='TABLE').fetchone():
            self.cursor.execute(self.query)

        results = [result[0] for result in self.cursor.description]

        self.terminate_connection()

        if results:
            results.pop(0)
            return results
        else:
            return None

    def get_column(self, table, column):
        x, y = [], []
        self.establish_connection()

        # Preparing query
        self.query = ("""SELECT measurement_time, %s """ +
                      """FROM %s;""") % (column, table)

        if self.cursor.tables(table=table, tableType='TABLE').fetchone():
            self.cursor.execute(self.query)

        results = self.cursor.fetchall()

        for result in results:
            x.append(result[0])
            y.append(result[1])

        self.terminate_connection()

        if x:
            return x, y
        else:
            return 0, 0
