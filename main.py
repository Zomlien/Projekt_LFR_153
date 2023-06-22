import logging
import psycopg2
from zoo.zooInput import ZooInput


def main() -> None:
    try:
        # Run the ZooInput application
        app = ZooInput('zoo/database.ini', 'postgresql')
        app.run()
    except psycopg2.OperationalError as e:
        print(f"Unable to connect to database: {e}")
        logging.error(e)
        print('Exiting')
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(e)
        print('Exiting')
        exit()

    print(app)

if __name__ == '__main__':
    main()
