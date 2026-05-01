import sqlite3
import tempfile
import shutil
import pathlib

class Database(object):
    def __init__(self):
        # SQLite
        self.connection = None
        self.db_open = False
        self.db_path = None
        self.is_db_saved = False
        self.db_cursor = None
        self.new_db_command = """BEGIN;
CREATE TABLE park_manager(id INTEGER NOT NULL UNIQUE PRIMARY KEY, plate TEXT NOT NULL UNIQUE, name TEXT NOT NULL);
CREATE INDEX index_plate ON park_manager (plate);
COMMIT;"""
        
        # Tempfolder
        self.temp = None
    
    def clean_temp(self):
        if self.temp:
            path = pathlib.Path(self.temp.name, "temp.db")

            with open(path, 'w') as file:
                pass
            
            print("Contents of temporary file removed")
    
    def create_temp(self):
        self.clean_temp()

        if not self.temp:
            self.temp = tempfile.TemporaryDirectory()
            path = pathlib.Path(self.temp.name, "temp.db")

            with open(path, 'w') as file:
                pass

            print(f"Temporary folder created at {self.temp.name}")
            print(f"Created a temporary file inside the folder at {path}")
    
    def destroy_temp(self):
        self.temp.cleanup()
        self.temp = None
    
    def new_database(self):
        if self.db_open:
            return

        self.create_temp()

        temp_path = pathlib.Path(self.temp.name, "temp.db")

        try:
            self.connection = sqlite3.connect(temp_path)
        except sqlite3.Error as error:
            print(error)
        else:
            self.db_cursor = self.connection.cursor()
            self.db_cursor.executescript(self.new_db_command)
            self.db_open = True
            self.is_db_saved = False
            print("Database created!")
    
    def open_database(self, path):
        if self.db_open:
            return False
        
        self.create_temp()

        temp_path = pathlib.Path(self.temp.name, "temp.db")

        shutil.copy2(path, temp_path)

        try:
            self.connection = sqlite3.connect(temp_path)
        except sqlite3.Error as error:
            print(error)
            return False
        else:
            self.db_cursor = self.connection.cursor()
            self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='park_manager';")
            if self.db_cursor.fetchone()[0] == "park_manager":
                self.db_open = True
                self.db_path = path
                self.is_db_saved = True
                print("Database opened!")
                return True
            else:
                print("Invalid database!")
                return False
    
    def close_database(self, force_close=False):
        if not self.connection:
            return True
        
        if (self.is_db_saved and self.db_path) or force_close:
            self.connection.close()
            
            self.connection = None
            self.db_open = False
            self.db_path = None
            self.is_db_saved = False
            self.db_cursor = None

            self.clean_temp()

            return True
        
        return False
    
    def save_database(self):
        if not self.db_open or self.is_db_saved:
            print("File already saved or not open!")
            return True
        
        if self.db_path:
            path = pathlib.Path(self.temp.name, "temp.db")

            self.connection.commit()
            self.connection.close()
            self.db_cursor = None
            self.connection = None

            shutil.copy2(path, self.db_path)

            self.connection = sqlite3.connect(path)
            self.db_cursor = self.connection.cursor()
            self.is_db_saved = True
            print("Database saved!")
            return True
        else:
            print("Couldn't save. Path missing!")
            return False

    def set_database_path(self, path):
        self.db_path = path

    def fetch_database_data(self):
        if not self.db_open:
            return None
        
        command = self.db_cursor.execute("SELECT plate, name FROM park_manager")
        results = command.fetchall()

        if results:
            formatted_data = list()
            plates = list()
            for result in results:
                plate = result[0]
                name = result[1]
                formatted_data.append(f"{plate} ({name})")
                plates.append(plate)
            return (formatted_data, plates)
        
        return None
    
    def check_if_plate_is_allowed(self, plate):
        try:
            self.db_cursor.execute("SELECT EXISTS(SELECT 1 FROM park_manager WHERE plate = ? LIMIT 1)", [plate])
        except sqlite3.IntegrityError as error:
            print(error)
            return False
        else:
            if self.db_cursor.fetchone()[0]:
                return True
            else:
                return False

    def add_to_database(self, plate, name):
        if not self.db_open:
            return False
        
        try:
            self.db_cursor.execute("INSERT INTO park_manager (plate, name) VALUES(?, ?)", [plate, name])
        except sqlite3.IntegrityError as error:
            print(error)
            return False
        else:
            self.connection.commit()
            self.is_db_saved = False
            return True
        
        return False
    
    def remove_from_database(self, plate):
        if not self.db_open:
            return False

        try:
            self.db_cursor.execute("DELETE FROM park_manager WHERE plate = ?", [plate])
        except sqlite3.IntegrityError as error:
            print(error)
            return False
        else:
            self.connection.commit()
            self.is_db_saved = False
            return True

        return False

    def edit_database(self, plate, new_plate = None, new_name = None):
        if not self.db_open:
            return False

        if new_plate or new_name:
            try:
                if new_plate and new_name:
                    self.db_cursor.execute("UPDATE park_manager SET plate = ?, name = ? WHERE plate = ?", [new_plate, new_name, plate])
                elif new_plate:
                    self.db_cursor.execute("UPDATE park_manager SET plate = ? WHERE plate = ?", [new_plate, plate])
                else:
                    self.db_cursor.execute("UPDATE park_manager SET name = ? WHERE plate = ?", [new_name, plate])
            except sqlite3.IntegrityError as error:
                print(error)
                return False
            else:
                self.connection.commit()
                self.is_db_saved = False
                return True
        else:
            return False

        return False
        
    def dummy_write(self):
        if not self.db_open:
            return False
        
        try:
            self.db_cursor.execute("INSERT INTO park_manager (plate, name) VALUES(?, ?)", ["BN 18 CTL", "Hosu Adrian"])
        except sqlite3.IntegrityError as error:
            print(error)
            return False
        else:
            self.connection.commit()
            self.is_db_saved = False
            return True

        
database = Database()



