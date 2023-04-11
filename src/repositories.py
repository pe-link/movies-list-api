from sqlalchemy.orm import Session

from models import Producer, Movie, TimeInterval, WinIntervalTimes
from utils.enum import IntervalsRange


class ProducersRepository:
    @staticmethod
    def find_win_interval_times(db_session: Session, interval_range: IntervalsRange) -> WinIntervalTimes:
        producers = db_session.query(Producer).join(Producer.movies).filter(Movie.winner.is_(True)).all()
        intervals = []
        for producer in producers:
            win_years = sorted(movie.year for movie in producer.movies if movie.winner)
            for i in range(len(win_years) - 1):
                interval = win_years[i + 1] - win_years[i]
                intervals.append(TimeInterval(producer.name, interval, win_years[i], win_years[i + 1]))

        if interval_range == IntervalsRange.MIN:
            min_interval = min(intervals, key=lambda interval: interval.interval).interval
            result = WinIntervalTimes([interval for interval in intervals if interval.interval == min_interval], [])
        else:
            max_interval = max(intervals, key=lambda interval: interval.interval).interval
            result = WinIntervalTimes([], [interval for interval in intervals if interval.interval == max_interval])

        return result
