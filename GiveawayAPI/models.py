import bcrypt
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    books = relationship("Book", back_populates="owner", foreign_keys="[Book.user_id]")
    interested_books = relationship("Book", back_populates="interested_user", foreign_keys="[Book.interested_user_id]")

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    author = Column(String)
    genre = Column(String)
    condition = Column(String)
    pickup_location = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    interested_user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", foreign_keys=[user_id], back_populates="books")
    interested_user = relationship("User", foreign_keys=[interested_user_id], back_populates="interested_books")
