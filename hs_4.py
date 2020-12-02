# Standard libraries
import os
import datetime

# Imported libraries
import pyodbc as db

database_path = os.getcwd() + r"/hajle_silesia_db.accdb"
connection_string = ("Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
                     "DBQ=" + database_path + ";")

db_connection = db.connect(connection_string, autocommit=True)
cursor = db_connection.cursor()

# Prepare query
# self.query = ("""UPDATE Fermentation_settings """ +
#               """SET log=? """ +
#               """WHERE batch_number=(SELECT MAX(batch_number) FROM Fermentation_settings) """ +
#               """AND fermentation_vessel=?;""")
query = ("""UPDATE Fermentation_settings """ +
         """SET log=? """ +
         """WHERE batch_number=(SELECT TOP 1 batch_number """ +
         """FROM Fermentation_settings """ +
         """WHERE fermentation_vessel=? """ +
         """ORDER BY batch_number DESC);""")
# query = ("""SELECT TOP 1 batch_number """ +
#          """FROM Fermentation_settings """ +
#          """WHERE fermentation_vessel=? """ +
#          """ORDER BY batch_number DESC;""")

print(query)

if cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
    cursor.execute(query, True, 'fv_2')

cursor.close()
db_connection.close()
