from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
DATABASE_URL = os.environ['DATABASE_URL']
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)

session = Session()
