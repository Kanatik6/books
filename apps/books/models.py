from sqlalchemy import Column, Integer, String, ForeignKey,Table
from sqlalchemy.orm import relationship

from apps.database import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False,unique=True)
    descriptions = Column(String)
    file_name = Column(String)

    author_id = Column(Integer,ForeignKey('users.id'))
    author = relationship("User",backref='author_books')
    
    in_favorite_users = relationship("User", secondary="book_users", back_populates='favorite_books')


book_users = Table('book_users', Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('users_id', ForeignKey('users.id'), primary_key=True),
)


class Part(Base):
    __tablename__ = 'parts'
    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    descriptions = Column(String)
    
    book_id = Column('book_id',ForeignKey('books.id'))
    book = relationship('Book',backref='parts')
