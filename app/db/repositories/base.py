from abc import ABC

from databases import Database


class BaseRepository(ABC):
    def __init__(self, db: Database):
        self.db = db
