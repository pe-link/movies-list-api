from flask import Flask, jsonify, Response
from typing import Any
from config import config
from database import SQLiteDataBase
from sqlalchemy.orm import Session
from services import ProducersService


class App(Flask):
    _instance = None

    def __new__(cls: 'App', *args: list[Any], **kwargs: dict[str, Any]) -> 'App':
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._database = SQLiteDataBase(csv_file=config.MOVIES_CSV_FILE)
        return cls._instance

    @property
    def db_session(self: 'App') -> Session:
        return self._database.session


app = App(__name__)


@app.route('/producers/range-winners', methods=['GET'])
def get_winners_interval() -> Response:
    intervals_ranges = ProducersService.find_interval_range(app.db_session)
    response = intervals_ranges.to_dict()
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
