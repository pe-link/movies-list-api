from sqlalchemy.orm import Session
from models import WinIntervalTimes
from repositories import ProducersRepository
from utils.enum import IntervalsRange


class ProducersService:
    @staticmethod
    def find_interval_range(db_session: Session) -> WinIntervalTimes:
        min_win_interval = ProducersRepository.find_win_interval_times(db_session, IntervalsRange.MIN)
        max_win_interval = ProducersRepository.find_win_interval_times(db_session, IntervalsRange.MAX)
        return WinIntervalTimes(min_win_interval.min_intervals, max_win_interval.max_intervals)
