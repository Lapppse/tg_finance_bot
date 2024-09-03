__all__ = ("Conn", "create_db")

import sqlite3

from loguru import logger
from utils import config


class Conn:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.file_path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            raise Exception(exc_type, exc_value, traceback)
        self.cursor.close()
        self.conn.commit()
        self.conn.close()


def create_db():
    with Conn("bot/db/test.db") as db:
        with open("bot/db/queries/create_expenses.sql", "r") as f:
            db.execute(f.read())
            logger.debug(f"created expenses table in {config.current_db_path}")
