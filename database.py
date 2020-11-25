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

        # DO NOT REMOVE
        # # Prepare query for table creation
        # self.query = ("""CREATE TABLE Fermentation_settings""" +
        #               """(batch_number short PRIMARY KEY NOT NULL,""" +
        #               """temperature_offset DOUBLE NOT NULL, """ +
        #               """gravity_1 DOUBLE NOT NULL,""" +
        #               """gravity_2 DOUBLE NOT NULL,""" +
        #               """angle_1 DOUBLE NOT NULL,""" +
        #               """angle_2 DOUBLE NOT NULL,""" +
        #               """a DOUBLE NOT NULL,""" +
        #               """b DOUBLE NOT NULL);""")
        #
        # # Check existence / create table
        # if not self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
        #     self.db_connection.execute(self.query)
        # DO NOT REMOVE

    def execute_fermentation(self, fermentation_parameters, batch_number):
        self.establish_connection()

        fermentation = str(batch_number) + '_Ferm'

        # Prepare query for table creation
        self.query = ("""CREATE TABLE """ + fermentation +
                      """(id AUTOINCREMENT PRIMARY KEY NOT NULL,""" +
                      """measurement_time DATETIME NOT NULL,""" +
                      """name VARCHAR(15) NOT NULL,""" +
                      """angle DOUBLE NOT NULL,""" +
                      """temperature DOUBLE NOT NULL,""" +
                      """temp_units VARCHAR(1) NOT NULL, """ +
                      """battery DOUBLE NOT NULL,""" +
                      """gravity DOUBLE NOT NULL,""" +
                      """interval SHORT NOT NULL,""" +
                      """rssi SHORT NOT NULL);""")

        # Check existence / create table
        if not self.cursor.tables(table=fermentation, tableType='TABLE').fetchone():
            self.cursor.execute(self.query)

        # Save new data
        self.query = """INSERT INTO """ + fermentation + """("""

        for key in fermentation_parameters.parameters:
            self.query += key + ','
        self.query = self.query[:-1]

        self.query += """) VALUES ("""

        for key, value in fermentation_parameters.parameters.items():
            if key == 'measurement_time':
                self.query += "'" + value.strftime('%Y-%m-%d %H:%M:%S') + "',"
            elif type(value) == str:
                self.query += "'" + str(value) + "',"
            else:
                self.query += str(value) + ","

        self.query = self.query[:-1]

        self.query += """);"""

        if self.cursor.tables(table='12_Ferm', tableType='TABLE').fetchone():
            self.cursor.execute(self.query)

        self.terminate_connection()

    def execute_fermentation_settings(self, ispindel_parameters):
        self.establish_connection()

        # Prepare query for table creation
        self.query = ("""CREATE TABLE Fermentation_settings""" +
                      """(id AUTOINCREMENT PRIMARY KEY NOT NULL,""" +
                      """batch_number LONG NOT NULL,""" +
                      """fermentation_vessel VARCHAR(25) NOT NULL,""" +
                      """ispindel_name VARCHAR(25) NOT NULL,""" +
                      """temperature_offset DOUBLE NOT NULL,""" +
                      """gravity_0 DOUBLE NOT NULL,""" +
                      """gravity_1 DOUBLE NOT NULL, """ +
                      """angle_0 DOUBLE NOT NULL,""" +
                      """angle_1 DOUBLE NOT NULL,""" +
                      """a DOUBLE NOT NULL,""" +
                      """b DOUBLE NOT NULL,""" +
                      """battery_notification BIT NOT NULL);""")

        # Check existence / create table
        if not self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query)

        self.query = ("""INSERT INTO Fermentation_settings(""" +
                      """batch_number,""" +
                      """fermentation_vessel,""" +
                      """ispindel_name,""" +
                      """temperature_offset,""" +
                      """gravity_0,""" +
                      """gravity_1,""" +
                      """angle_0,""" +
                      """angle_1,""" +
                      """a,""" +
                      """b,""" +
                      """battery_notification) VALUES (""" +
                      """?,""" +
                      """?,""" +
                      """?,""" +
                      """?,""" +
                      """?,""" +
                      """?,""" +
                      """?,""" +
                      """?,""" +
                      """?,""" +
                      """?,""" +
                      """?);""")

        # Save new data
        # self.query = """INSERT INTO Fermentation_settings ("""

        # for key in ispindel_parameters.parameters:
        #     self.query += key + ','
        # self.query = self.query[:-1]
        #
        # self.query += """) VALUES ("""
        #
        # for value in ispindel_parameters.parameters.values():
        #     self.query += str(value) + ','
        #     print(type(value), value)
        # self.query = self.query[:-1]
        #
        # self.query += """);"""

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query, tuple(ispindel_parameters.parameters.values()))

        self.terminate_connection()

    def establish_connection(self):
        self.db_connection = db.connect(self.connection_string, autocommit=True)
        self.cursor = self.db_connection.cursor()

    def terminate_connection(self):
        self.cursor.close()
        self.db_connection.close()

    def plot(self):
        self.establish_connection()

        x = []
        y = []

        # Prepare query
        self.query = """SELECT * FROM 73_Ferm ORDER BY id;"""
        self.cursor.execute(self.query)

        for row in self.cursor.fetchall():
            x.append(row.measurement_time)
            y.append(row.gravity)

        self.terminate_connection()

        return x, y

    def get_ispindel_temperature_offset(self, ispindel_name):
        self.establish_connection()

        # Prepare query
        self.query = """SELECT * FROM iSpindel_settings;"""

        if self.cursor.tables(table='iSpindel_settings', tableType='TABLE').fetchone():
            self.cursor.execute(self.query)

        for row in self.cursor:
            if row.name == ispindel_name:
                break

        self.terminate_connection()
        return row.temperature_offset
