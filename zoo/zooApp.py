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
                enclosure_id               SERIAL PRIMARY KEY,
                name                       VARCHAR(100),
                size                       INT
            )"""

        catsql = """
            CREATE TABLE IF NOT EXISTS animalcat(
                animalcat_id            SERIAL PRIMARY KEY,
                category                  VARCHAR(100)              
            );"""
        breedsql="""
            CREATE TABLE IF NOT EXISTS animalbreed(
                animalbreed_id             SERIAL PRIMARY KEY,
                breed                      VARCHAR(100),
                animalcat_id               INTEGER REFERENCES animalcat(animalcat_id) ON DELETE CASCADE
            );"""
        
        keepersql="""
            CREATE TABLE IF NOT EXISTS keeper(
                keeper_id                  SERIAL PRIMARY KEY,
                name                       VARCHAR(100),
                enclosure_id               INTEGER REFERENCES enclosure(enclosure_id ) ON DELETE CASCADE
            );"""
        animalsql="""
            CREATE TABLE IF NOT EXISTS animal(
                animal_id                  SERIAL PRIMARY KEY,
                name                       VARCHAR(100),
                birthday                   date,
                animalbreed_id            INTEGER REFERENCES animalbreed(animalbreed_id) ON DELETE CASCADE,
                enclosure_id               INTEGER REFERENCES enclosure(enclosure_id ) ON DELETE CASCADE
            );"""

        try:
            self.cur.execute(encolsuresql)
            self.cur.execute(catsql)
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


    #CRUD cat
    def view_all_animalcats(self):
        sql = "SELECT * FROM animalcat"
        try:
            self.cur.execute(sql)
            animalcats = self.cur.fetchall()
            return animalcats
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving animal categorys.")
            return []


    def add_animalcat(self, category):
        sql = "INSERT INTO animalcat (category) VALUES (%s) RETURNING animalcat_id"
        try:
            self.cur.execute(sql, (category,))
            self.conn.commit()
            animalcat_id = self.cur.fetchone()[0]
            print(f"Animal category with ID {animalcat_id} added successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while adding animal category.")


    def edit_animalcat(self, animalcat_id, category):
        sql = "UPDATE animalcat SET category = %s WHERE animalcat_id = %s"
        try:
            self.cur.execute(sql, (category, animalcat_id))
            self.conn.commit()
            print(f"Animal category with ID {animalcat_id} updated successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while editing animal category.")


    def delete_animalcat(self, animalcat_id):
        sql = "DELETE FROM animalcat WHERE animalcat_id = %s"
        try:
            self.cur.execute(sql, (animalcat_id,))
            self.conn.commit()
            print(f"Animal category with ID {animalcat_id} deleted successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while deleting animal category.")


    def get_animalcat_by_id(self, animalcat_id):
        sql = "SELECT category FROM animalcat WHERE animalcat_id = %s"
        try:
            self.cur.execute(sql, (animalcat_id,))
            result = self.cur.fetchone()
            if result:
                return result[0]
            else:
                return "N/A"
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving animal category.")
            return "N/A"


    #CRUD breed
    def view_all_animalbreed(self):
        sql = "SELECT * FROM animalbreed"
        try:
            self.cur.execute(sql)
            animalbreed = self.cur.fetchall()
            return animalbreed
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while retrieving animal breeds.")
            return []


    def add_animalbreed(self, breed, animalcat_id):
        sql = "INSERT INTO animalbreed (breed, animalcat_id) VALUES (%s, %s) RETURNING animalbreed_id"
        try:
            self.cur.execute(sql, (breed, animalcat_id))
            self.conn.commit()
            animalbreed_id = self.cur.fetchone()[0]
            print(f"Animal breed with ID {animalbreed_id} added successfully.")
        except psycopg2.Error as e:
            logging.error(e)
            self.conn.rollback()
            print("Error occurred while adding animal breed.")


    def edit_animalbreed(self, animalbreed_id, breed, animalcat_id):
        sql = "UPDATE animalbreed SET breed = %s, animalcat_id = %s WHERE animalbreed_id = %s"
        try:
            self.cur.execute(sql, (breed, animalcat_id, animalbreed_id))
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
        sql = "SELECT breed, animalcat_id FROM animalbreed WHERE animalbreed_id = %s"
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
        sql = "INSERT INTO animal (name, birthday, animalbreed_id, enclosure_id) VALUES (%s, %s, %s, %s) RETURNING animal_id"
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
        sql = "UPDATE animal SET name = %s, birthday = %s, animalbreed_id = %s, enclosure_id = %s WHERE animal_id = %s"
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
        sql = "SELECT name, birthday, animalbreed_id, enclosure_id FROM animal WHERE animal_id = %s"
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
    def search_animal_name(self, name):
        sql = "SELECT * FROM animal WHERE name ILIKE %s"
        try:
            self.cur.execute(sql, ('%' + name + '%',))
            animals = self.cur.fetchall()
            return animals
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while searching animals by name.")
            return []



    #filter function for animal breeds by animal categorys
    def filter_breeds_by_category(self, category):
        sql = """
            SELECT animalbreed.breed
            FROM animalbreed
            JOIN animalcat ON animalbreed.animalcat_id = animalcat.animalcat_id
            WHERE animalcat.name = %s
        """
        try:
            self.cur.execute(sql, (category,))
            breeds = self.cur.fetchall()
            return [breed[0] for breed in breeds]
        except psycopg2.Error as e:
            logging.error(e)
            print("Error occurred while filtering breeds by category.")
            return []

   

    