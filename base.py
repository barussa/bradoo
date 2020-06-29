from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://henrique_gfc:hbcm@localhost:5432/henrique_gfc'
)
Session = sessionmaker(bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)

session = Session()
