from flask import Flask
from typing import Any
from config import config
from database import SQLiteDataBase
from sqlalchemy.orm import Session


class App(Flask):
    _instance = None

    def __new__(cls: 'App', *args: list[Any], **kwargs: dict[str, Any]) -> 'App':
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._database = SQLiteDataBase(csv_file=config.MOVIES_CSV_FILE)
        return cls._instance


app = App(__name__)


if __name__ == '__main__':
    app.run(debug=True)
