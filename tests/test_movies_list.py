from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app import app
from src.config import config
from src.database import SQLiteDataBase
from src.models import (BaseModel, Movie, Producer, TimeInterval,
                        WinIntervalTimes)
from src.services import ProducersService


@pytest.fixture
def database():
    database = SQLiteDataBase(csv_file=config.MOVIES_CSV_FILE)
    yield database


@pytest.fixture(scope='session')
def memory_db():
    engine = create_engine('sqlite:///:memory:')
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    BaseModel.metadata.drop_all(engine)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_winners_interval_api(client):
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


def test_find_interval_range_max_and_min_intervals_in_memory_db(memory_db):
    movie1 = Movie(title='Movie 1', year=2000, studios='Studio 1', winner=True)
    movie2 = Movie(title='Movie 2', year=2001, studios='Studio 2', winner=True)
    movie3 = Movie(title='Movie 3', year=2010, studios='Studio 3', winner=True)
    movie4 = Movie(title='Movie 4', year=2017, studios='Studio 4', winner=True)
    movie5 = Movie(title='Movie 5', year=2020, studios='Studio 5', winner=True)
    producer1 = Producer(name='Producer 1', movies=[movie1, movie2])
    producer2 = Producer(name='Producer 2', movies=[movie3, movie4])
    producer3 = Producer(name='Producer 3', movies=[movie2, movie5])
    memory_db.add_all([movie1, movie2, movie3, movie4, movie5, producer1, producer2, producer3])
    memory_db.commit()
    win_interval_times = ProducersService.find_interval_range(memory_db)

    # MIN INTERVALS
    assert len(win_interval_times.min_intervals) == 1
    assert win_interval_times.min_intervals[0].producer_name == 'Producer 1'
    assert win_interval_times.min_intervals[0].interval == 1

    # MAX INTERVALS
    assert len(win_interval_times.max_intervals) == 1
    assert win_interval_times.max_intervals[0].producer_name == 'Producer 3'
    assert win_interval_times.max_intervals[0].interval == 19


def test_mock_consecutive_wins_min_and_max_intervals():
    db_session_mock = Mock()
    producer_1_mock = Mock(spec=Producer)
    producer_2_mock = Mock(spec=Producer)
    movie_1_mock = Mock(spec=Movie)
    movie_2_mock = Mock(spec=Movie)
    movie_3_mock = Mock(spec=Movie)
    movie_4_mock = Mock(spec=Movie)

    producer_1_mock.name = 'Producer 1'
    producer_2_mock.name = 'Producer 2'
    movie_1_mock.year = 2000
    movie_1_mock.winner = True
    movie_2_mock.year = 2005
    movie_2_mock.winner = True
    movie_3_mock.year = 2010
    movie_3_mock.winner = True
    movie_4_mock.year = 2020
    movie_4_mock.winner = True
    producer_1_mock.movies = [movie_1_mock, movie_2_mock]
    producer_2_mock.movies = [movie_3_mock, movie_4_mock]
    db_session_mock.query.return_value.join.return_value.filter.return_value.all.return_value = [producer_1_mock, producer_2_mock]

    result = ProducersService.find_interval_range(db_session_mock)

    # MIN INTERVALS
    assert len(result.min_intervals) == 1
    assert result.min_intervals[0].producer_name == 'Producer 1'
    assert result.min_intervals[0].interval == 5
    assert result.min_intervals[0].previous_win == 2000
    assert result.min_intervals[0].following_win == 2005

    # MAX INTERVALS
    assert len(result.max_intervals) == 1
    assert result.max_intervals[0].producer_name == 'Producer 2'
    assert result.max_intervals[0].interval == 10
    assert result.max_intervals[0].previous_win == 2010
    assert result.max_intervals[0].following_win == 2020
