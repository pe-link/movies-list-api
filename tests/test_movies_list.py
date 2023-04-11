import pytest

from src.app import app
from src.config import config
from src.database import SQLiteDataBase
from src.models import Movie, Producer, TimeInterval, WinIntervalTimes
from src.services import ProducersService


@pytest.fixture
def database():
    database = SQLiteDataBase(csv_file=config.MOVIES_CSV_FILE)
    yield database


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_winners_interval(client):
    response = client.get('/producers/range-winners')
    assert response.status_code == 200
    expected_json = {
        'max': [{'followingWin': 2015, 'interval': 13, 'previousWin': 2002, 'producer': 'Matthew Vaughn'}],
        'min': [{'followingWin': 1991, 'interval': 1, 'previousWin': 1990, 'producer': 'Joel Silver'}]
    }

    assert expected_json == response.json


def test_find_interval_range(database):
    with app.app_context():
        result = ProducersService.find_interval_range(database.session)
        assert isinstance(result, WinIntervalTimes)
        assert len(result.min_intervals) > 0
        assert len(result.max_intervals) > 0
        for interval in result.min_intervals + result.max_intervals:
            assert isinstance(interval, TimeInterval)
            assert isinstance(interval.producer_name, str)
            assert isinstance(interval.interval, int)
            assert isinstance(interval.previous_win, int)
            assert isinstance(interval.following_win, int)


def test_insert_csv_database(database):
    with app.app_context():
        session = database.session
        producers = session.query(Producer).all()
        assert len(producers) > 0
        movies = session.query(Movie).all()
        assert len(movies) > 0
