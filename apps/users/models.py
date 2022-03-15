from sqlalchemy import Column, Integer, String
from apps.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    last_name = Column(String)
    hashed_password = Column(String)
    
    books = relationship("Book", secondary="book_users", back_populates='users')
