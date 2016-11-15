from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
# from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.


class elucidata(models.Model):
    id = models.IntegerField(primary_key=True)
    tokens = models.CharField(max_length=3000, blank=True)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password


# Create tables.
Base.metadata.create_all(bind=engine)
