from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

BaseModel = declarative_base()


class ProducerMovie(BaseModel):
    __tablename__ = 'producer_movie'
    producer_id = Column(Integer, ForeignKey('producers.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)


class Producer(BaseModel):
    __tablename__ = 'producers'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    movies = relationship('Movie', secondary='producer_movie', back_populates='producers')


class Movie(BaseModel):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    year = Column(Integer)
    studios = Column(String(256))
    winner = Column(Boolean, default=False)
    producers = relationship('Producer', secondary='producer_movie', back_populates='movies')


class TimeInterval:
    def __init__(self, producer_name: str, interval: int, previous_win: int, following_win: int):
        self.producer_name = producer_name
        self.interval = interval
        self.previous_win = previous_win
        self.following_win = following_win


class WinIntervalTimes:
    def __init__(self, min_intervals: list[TimeInterval], max_intervals: list[TimeInterval]):
        self.min_intervals = min_intervals
        self.max_intervals = max_intervals

    def to_dict(self) -> dict:
        return {
            "min": [self._interval_to_dict(interval) for interval in self.min_intervals],
            "max": [self._interval_to_dict(interval) for interval in self.max_intervals]
        }

    def _interval_to_dict(self, interval: TimeInterval) -> dict:
        return {
            "producer": interval.producer_name,
            "interval": interval.interval,
            "previousWin": interval.previous_win,
            "followingWin": interval.following_win
        }
