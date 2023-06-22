import psycopg2
import logging
import datetime
from zoo.config import ConfigReader

class zooApp(ConfigReader):

    #DB verbindung
    def __init__(self, configfile, section):
        super().__init__(configfile, section)
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename='zoo/error.log', level=logging.ERROR, format=log_format)
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            params = self.config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as e:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            error_message = f"{timestamp} - {str(e)}"
            logging.error(error_message)
            raise e

    def __repr__(self):
        if self.conn is not None:
            dsn_parameters = self.conn.get_dsn_parameters()
            return f"Connected to database '{dsn_parameters['dbname']}' on host '{dsn_parameters['host']}' as user '{dsn_parameters['user']}'"
        else:
            return "Not connected to any database"

    def create_tables(self) -> None:
        encolsuresql = """
            CREATE TABLE IF NOT EXISTS enclosure(
                ENCLOSURE_ID               SERIAL PRIMARY KEY,
                name                       VARCHAR(100),
                size                       INT
            )"""

        katsql = """
            CREATE TABLE IF NOT EXISTS animalkat(
                ANIMALKAT_ID              SERIAL PRIMARY KEY,
                kategory                  VARCHAR(100)              
            );"""
        breedsql="""
            CREATE TABLE IF NOT EXISTS animalbreed(
                ANIMALBREED_ID             SERIAL PRIMARY KEY,
                breed                      VARCHAR(100),
                ANMIALKAT_ID               INTEGER REFERENCES animalkat(ANIMALKAT_ID) ON DELETE CASCADE
            );"""
        
        keepersql="""
            CREATE TABLE IF NOT EXISTS keeper(
                KEPPER_ID                  SERIAL PRIMARY KEY,
                name                       VARCHAR(100),
                ENCLOSURE_ID               INTEGER REFERENCES enclosure(ENCLOSURE_ID) ON DELETE CASCADE
            );"""
        animalsql="""
            CREATE TABLE IF NOT EXISTS animal(
                ANIMAL_ID                  SERIAL PRIMARY KEY,
                name                       VARCHAR(100),
                birthday                   date,
                ANIMALBREED_ID             INTEGER REFERENCES animalbreed(ANIMALBREED_ID) ON DELETE CASCADE,
                ENCLOSURE_ID               INTEGER REFERENCES enclosure(ENCLOSURE_ID) ON DELETE CASCADE
            );"""

        try:
            self.cur.execute(encolsuresql)
            self.cur.execute(katsql)
            self.cur.execute(breedsql)
            self.cur.execute(keepersql)
            self.cur.execute(animalsql)
            self.conn.commit()
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()

    #CRUD enclosure
    def view_all_enclosures(self):
        sql = "SELECT * FROM enclosure"
        try:
            self.cur.execute(sql)
            enclosures = self.cur.fetchall()
            return enclosures
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving enclosures.")
            return []


    def add_enclosure(self, name, size):
        sql = "INSERT INTO enclosure (name, size) VALUES (%s, %s) RETURNING enclosure_id"
        try:
            self.cur.execute(sql, (name, size))
            self.conn.commit()
            enclosure_id = self.cur.fetchone()[0]
            print(f"Enclosure with ID {enclosure_id} added successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while adding enclosure.")


    def edit_enclosure(self, enclosure_id, name, size):
        sql = "UPDATE enclosure SET name = %s, size = %s WHERE enclosure_id = %s"
        try:
            self.cur.execute(sql, (name, size, enclosure_id))
            self.conn.commit()
            print(f"Enclosure with ID {enclosure_id} updated successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while editing enclosure.")


    def delete_enclosure(self, enclosure_id):
        sql = "DELETE FROM enclosure WHERE enclosure_id = %s"
        try:
            self.cur.execute(sql, (enclosure_id,))
            self.conn.commit()
            print(f"Enclosure with ID {enclosure_id} deleted successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while deleting enclosure.")


    def get_enclosure_by_id(self, enclosure_id):
        sql = "SELECT name, size FROM enclosure WHERE enclosure_id = %s"
        try:
            self.cur.execute(sql, (enclosure_id,))
            result = self.cur.fetchone()
            if result:
                return result
            else:
                return "N/A"
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving enclosure.")
            return "N/A"


    #CRUD kat
    def view_all_animalkats(self):
        sql = "SELECT * FROM animalkat"
        try:
            self.cur.execute(sql)
            animalkats = self.cur.fetchall()
            return animalkats
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving animal kategories.")
            return []


    def add_animalkat(self, kategory):
        sql = "INSERT INTO animalkat (kategory) VALUES (%s) RETURNING animalkat_id"
        try:
            self.cur.execute(sql, (kategory,))
            self.conn.commit()
            animalkat_id = self.cur.fetchone()[0]
            print(f"Animal kategory with ID {animalkat_id} added successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while adding animal kategory.")


    def edit_animalkat(self, animalkat_id, kategory):
        sql = "UPDATE animalkat SET kategory = %s WHERE animalkat_id = %s"
        try:
            self.cur.execute(sql, (kategory, animalkat_id))
            self.conn.commit()
            print(f"Animal kategory with ID {animalkat_id} updated successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while editing animal kategory.")


    def delete_animalkat(self, animalkat_id):
        sql = "DELETE FROM animalkat WHERE animalkat_id = %s"
        try:
            self.cur.execute(sql, (animalkat_id,))
            self.conn.commit()
            print(f"Animal kategory with ID {animalkat_id} deleted successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while deleting animal kategory.")


    def get_animalkat_by_id(self, animalkat_id):
        sql = "SELECT kategory FROM animalkat WHERE animalkat_id = %s"
        try:
            self.cur.execute(sql, (animalkat_id,))
            result = self.cur.fetchone()
            if result:
                return result[0]
            else:
                return "N/A"
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving animal kategory.")
            return "N/A"


    #CRUD breed
    def view_all_animalbreeds(self):
        sql = "SELECT * FROM animalbreed"
        try:
            self.cur.execute(sql)
            animalbreeds = self.cur.fetchall()
            return animalbreeds
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving animal breeds.")
            return []


    def add_animalbreed(self, breed, animalkat_id):
        sql = "INSERT INTO animalbreed (breed, animalkat_id) VALUES (%s, %s) RETURNING animalbreed_id"
        try:
            self.cur.execute(sql, (breed, animalkat_id))
            self.conn.commit()
            animalbreed_id = self.cur.fetchone()[0]
            print(f"Animal breed with ID {animalbreed_id} added successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while adding animal breed.")


    def edit_animalbreed(self, animalbreed_id, breed, animalkat_id):
        sql = "UPDATE animalbreed SET breed = %s, animalkat_id = %s WHERE animalbreed_id = %s"
        try:
            self.cur.execute(sql, (breed, animalkat_id, animalbreed_id))
            self.conn.commit()
            print(f"Animal breed with ID {animalbreed_id} updated successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while editing animal breed.")


    def delete_animalbreed(self, animalbreed_id):
        sql = "DELETE FROM animalbreed WHERE animalbreed_id = %s"
        try:
            self.cur.execute(sql, (animalbreed_id,))
            self.conn.commit()
            print(f"Animal breed with ID {animalbreed_id} deleted successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while deleting animal breed.")


    def get_animalbreed_by_id(self, animalbreed_id):
        sql = "SELECT breed, animalkat_id FROM animalbreed WHERE animalbreed_id = %s"
        try:
            self.cur.execute(sql, (animalbreed_id,))
            result = self.cur.fetchone()
            if result:
                return result[0], result[1]
            else:
                return "N/A", "N/A"
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving animal breed.")
            return "N/A", "N/A"

    #CRUD keeper
    def view_all_keepers(self):
        sql = "SELECT * FROM keeper"
        try:
            self.cur.execute(sql)
            keepers = self.cur.fetchall()
            return keepers
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving keepers.")
            return []


    def add_keeper(self, name, enclosure_id):
        sql = "INSERT INTO keeper (name, enclosure_id) VALUES (%s, %s) RETURNING keeper_id"
        try:
            self.cur.execute(sql, (name, enclosure_id))
            self.conn.commit()
            keeper_id = self.cur.fetchone()[0]
            print(f"Keeper with ID {keeper_id} added successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while adding keeper.")


    def edit_keeper(self, keeper_id, name, enclosure_id):
        sql = "UPDATE keeper SET name = %s, enclosure_id = %s WHERE keeper_id = %s"
        try:
            self.cur.execute(sql, (name, enclosure_id, keeper_id))
            self.conn.commit()
            print(f"Keeper with ID {keeper_id} updated successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while editing keeper.")


    def delete_keeper(self, keeper_id):
        sql = "DELETE FROM keeper WHERE keeper_id = %s"
        try:
            self.cur.execute(sql, (keeper_id,))
            self.conn.commit()
            print(f"Keeper with ID {keeper_id} deleted successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while deleting keeper.")


    def get_keeper_by_id(self, keeper_id):
        sql = "SELECT name, enclosure_id FROM keeper WHERE keeper_id = %s"
        try:
            self.cur.execute(sql, (keeper_id,))
            result = self.cur.fetchone()
            if result:
                return result[0], result[1]
            else:
                return "N/A", "N/A"
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving keeper.")
            return "N/A", "N/A"

    #CRUD animal
    def view_all_animals(self):
        sql = "SELECT * FROM animal"
        try:
            self.cur.execute(sql)
            animals = self.cur.fetchall()
            return animals
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving animals.")
            return []


    def add_animal(self, name, birthday, breed_id, enclosure_id):
        sql = "INSERT INTO animal (name, birthday, breed_id, enclosure_id) VALUES (%s, %s, %s, %s) RETURNING animal_id"
        try:
            self.cur.execute(sql, (name, birthday, breed_id, enclosure_id))
            self.conn.commit()
            animal_id = self.cur.fetchone()[0]
            print(f"Animal with ID {animal_id} added successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while adding animal.")


    def edit_animal(self, animal_id, name, birthday, breed_id, enclosure_id):
        sql = "UPDATE animal SET name = %s, birthday = %s, breed_id = %s, enclosure_id = %s WHERE animal_id = %s"
        try:
            self.cur.execute(sql, (name, birthday, breed_id, enclosure_id, animal_id))
            self.conn.commit()
            print(f"Animal with ID {animal_id} updated successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while editing animal.")


    def delete_animal(self, animal_id):
        sql = "DELETE FROM animal WHERE animal_id = %s"
        try:
            self.cur.execute(sql, (animal_id,))
            self.conn.commit()
            print(f"Animal with ID {animal_id} deleted successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while deleting animal.")


    def get_animal_by_id(self, animal_id):
        sql = "SELECT name, birthday, breed_id, enclosure_id FROM animal WHERE animal_id = %s"
        try:
            self.cur.execute(sql, (animal_id,))
            result = self.cur.fetchone()
            if result:
                return result[0], result[1], result[2], result[3]
            else:
                return "N/A", "N/A", "N/A", "N/A"
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving animal.")
            return "N/A", "N/A", "N/A", "N/A"

    #search function animal name
    def search_animal_by_name(self, name):
        sql = "SELECT * FROM animal WHERE name ILIKE %s"
        try:
            self.cur.execute(sql, ('%' + name + '%',))
            animals = self.cur.fetchall()
            return animals
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while searching animals by name.")
            return []


    #filter function for animal breeds by animal kategories
    def filter_breeds_by_category(self, category):
        sql = """
            SELECT animalbreed.breed
            FROM animalbreed
            JOIN animalkat ON animalbreed.animalkat_id = animalkat.animalkat_id
            WHERE animalkat.kategory = %s
        """
        try:
            self.cur.execute(sql, (category,))
            breeds = self.cur.fetchall()
            return [breed[0] for breed in breeds]
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while filtering breeds by category.")
            return []
   

    