from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

base = declarative_base()


class PlayerModel(base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    score = Column(Integer, default=0)


class GameModel(base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player1_name = Column(String)
    player2_name = Column(String)
    player1_wins = Column(Integer)
    player2_wins = Column(Integer)
    sets = Column(Integer)


class Database:
    def __init__(self, db_url, Base):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def add_record(self, model, **kwargs):
        session = self.Session()
        entry = session.query(model).filter_by(**{k: v for k, v in kwargs.items() if k != 'score'}).first()
        if entry and model == PlayerModel:
            # Update the score if the entry exists
            score = kwargs.pop('score')
            entry.score += score
        else:
            new_entry = model(**kwargs)
            session.add(new_entry)
        session.commit()
        session.close()

    def get_all_record(self, model):
        session = self.Session()
        result = session.query(model).all()
        session.close()
        return result
