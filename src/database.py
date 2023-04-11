from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.models import BaseModel, Movie, Producer


class SQLiteDataBase:
    def __init__(self, csv_file: Path):
        self.engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False},
                                    poolclass=StaticPool)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        BaseModel.metadata.create_all(self.engine)
        self._insert_csv_database(csv_file)

    def _insert_csv_database(self, csv_file: Path) -> None:
        movie_table = pd.read_csv(csv_file, sep=';', keep_default_na=False)
        producers_names = {}

        for _, movie in movie_table.iterrows():
            producers_replace = movie.producers.replace(' and ', ',')
            producers = [producer.strip() for producer in producers_replace.split(',')]
            producers_list: list[Producer] = []
            for producer in producers:
                if producer not in producers_names:
                    novo_produtor = Producer(name=producer)
                    producers_names[producer] = novo_produtor
                producers_list.append(producers_names[producer])

            new_movie = Movie(title=movie.title, year=movie.year, studios=movie.studios,
                              winner=movie.winner == 'yes', producers=producers_list)
            self.session.add(new_movie)

        self.session.commit()
