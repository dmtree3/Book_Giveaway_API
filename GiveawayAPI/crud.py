from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import bcrypt
from sqlalchemy.orm import Session
from. import models, schemas


JWT_SECRET = "Secret"
ALGORITHM = "HS256"
oath2_scheme = OAuth2PasswordBearer(tokenUrl="views/token")


def get_books(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books_by_genre(db: Session, genre: str):
    return db.query(models.Book).filter(models.Book.genre == genre).all()


def get_books_by_author(db: Session, author: str):
    return db.query(models.Book).filter(models.Book.author == author).all()


def get_book_by_condition(db: Session, condition: str):
    return db.query(models.Book).filter(models.Book.condition == condition).all()


def create_book(db: Session, user: int, book: schemas.BookCreate):
    new_book = models.Book(title=book.title, author=book.author, genre=book.genre,
                           condition=book.condition, pickup_location=book.pickup_location, user_id=user)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_books(db: Session, user_id: int):
    return db.query(models.Book).filter(models.Book.user_id == user_id).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def express_interest_in_book(db: Session, book_id: int, user_id: int):
    db_book = get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found...")
    elif db_book.user_id == user_id:
        raise HTTPException(status_code=400, detail="You cannot express interest in your own book")
    elif db_book.interested_user_id is not None:
        raise HTTPException(status_code=400, detail="Book already has interested user")
    db_book.interested_user_id = user_id
    db.commit()
    return db_book


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"expires": expires.isoformat()})
    return jwt.encode(encode, JWT_SECRET, algorithm=ALGORITHM)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


def get_current_user(token: str = Depends(oath2_scheme)):
    authentication_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise authentication_exception
        return user_id
    except JWTError:
        raise authentication_exception
