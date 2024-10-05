import logging

from backend.app import Application
from backend.db.establish_db import establish_db

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if True:
        Application().run()
    else:
        establish_db()
        Application().run()
