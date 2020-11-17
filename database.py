# Standard libraries
import os

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

    def fermentation_settings_execute(self, ispindel_parameters):
        self.establish_connection()

        self.query = """INSERT INTO Fermentation_settings ("""

        for key in ispindel_parameters.parameters:
            self.query += key + ','
        self.query = self.query[:-1]

        self.query += """) VALUES ("""

        for value in ispindel_parameters.parameters.values():
            self.query += str(value) + ','
        self.query = self.query[:-1]

        self.query += """);"""

        if self.cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
            self.db_connection.execute(self.query)

        self.terminate_connection()

    def establish_connection(self):
        self.db_connection = db.connect(self.connection_string, autocommit=True)
        self.cursor = self.db_connection.cursor()

    def terminate_connection(self):
        self.cursor.close()
        self.db_connection.close()
