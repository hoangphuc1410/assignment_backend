import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def wait_for_db_connection(db_url: str, max_retries=10, delay=2):
    engine = create_engine(db_url)
    for attempt in range(max_retries):
        try:
            with engine.connect():
                print("Connected to the database!")
                return
        except OperationalError:
            print(f"DB not ready (attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)
    raise Exception("Could not connect to DB after several attempts.")
