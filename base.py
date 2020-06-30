from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://postgres:postgres@127.0.0.1:5432/vendor'
)
Session = sessionmaker(bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)

session = Session()
