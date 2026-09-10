from sqlalchemy import Column, Integer, String, Date
from config import Base,engine
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(Date)
    organizer = Column(String)
    city = Column(String)
    email = Column(String)
Base.metadata.create_all(bind=engine)
