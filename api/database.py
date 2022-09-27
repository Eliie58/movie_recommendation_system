from sqlalchemy import MetaData, Table, Column, String, Integer
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
import os

db_instance = None


class Database():
    engine = db.create_engine(os.environ["DATABASE_URL"])

    def __init__(self):
        self.connection = self.engine.connect()
        print("DB Instance created")

    def fetchAllUsers(self):
        self.session = Session(bind=self.connection)
        customers = self.session.query(Test).all()
        for cust in customers:
            print(cust)

    @staticmethod
    def instance():
        global db_instance
        if db_instance is None:
            db_instance = Database()
        return db_instance


Base = declarative_base()


class Test(Base):
    """Model for test."""
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    description = Column(String)

    def __repr__(self):
        return "<Test(id='%s', description='%s')>" % (self.id, self.description)
