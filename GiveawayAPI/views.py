from datetime import timedelta
from enum import Enum
from fastapi import Path, HTTPException, Depends, Query, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from . import crud, schemas, models
from typing import List, Annotated
from sqlalchemy.orm import Session
from .dependencies import get_db


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[models.User, Depends(crud.get_current_user)]


class Tags(Enum):
    users = "users"
    books = "books"


@router.post("/token")
def generate_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    token = crud.create_access_token(user.username, user.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/books/", response_model=List[schemas.BookBase], status_code=200, tags=[Tags.books])
def get_all_books(db: db_dependency, skip: int = 0, limit: int = 50):
    return crud.get_books(db, skip=skip, limit=limit)


@router.get("/books/by_genre", response_model=List[schemas.BookBase], status_code=200, tags=[Tags.books])
def get_books_by_genre(db: db_dependency, genre: str = Query(..., description="Filter books by genre.", min_length=3)):
    return crud.get_books_by_genre(db, genre=genre)


@router.get("/books/by_author", response_model=List[schemas.BookBase], status_code=200, tags=[Tags.books])
def get_books_by_author(db: db_dependency, author: str = Query(..., description="Filter books by author", min_length=3)):
    return crud.get_books_by_author(db, author=author)


@router.get("/books/by_condition", response_model=List[schemas.BookBase], status_code=200, tags=[Tags.books])
def get_books_by_condition(db: db_dependency, condition: str = Query(..., description="Filter books by condition")):
    return crud.get_book_by_condition(db, condition=condition)


@router.get("/books/{book_id}", response_model=schemas.Book, status_code=200, tags=[Tags.books])
def get_book_by_id(db: db_dependency, book_id: int = Path(..., ge=0)):
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found...")
    return db_book


@router.get("/users/", response_model=List[schemas.UserBase], status_code=200, tags=[Tags.users])
def get_all_users(db: db_dependency, skip: int = 0, limit: int = 50):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/users/id/{user_id}", response_model=schemas.UserBase, status_code=200, tags=[Tags.users])
def get_user_by_id(db: db_dependency, user_id: int = Path(..., ge=0)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found...")
    return db_user


@router.get("/users/username/{username}", response_model=schemas.UserBase, status_code=200, tags=[Tags.users])
def get_user_by_username(db: db_dependency, username: str = Path(...)):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User {username} not found...")
    return db_user


@router.post("/create_user", response_model=schemas.User, status_code=201, tags=[Tags.users])
def create_user(user: schemas.UserCreate, db: db_dependency):
    db_email = crud.get_user_by_email(db, user_email=user.email)
    db_username = crud.get_user_by_username(db, username=user.username)
    if db_email or db_username:
        raise HTTPException(status_code=400, detail="User already exists...")
    return crud.create_user(db, user=user)


@router.get("/users/{user_id}/books", response_model=List[schemas.Book], status_code=200, tags=[Tags.users, Tags.books])
def get_users_books(db: db_dependency, user_id: int = Path(..., ge=0)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found...")
    return db_user.books


@router.post("/add_book", status_code=201, response_model=schemas.Book, tags=[Tags.books])
def add_book(db: db_dependency, book: schemas.BookCreate, user: user_dependency):
    new_book = crud.create_book(db, user=user, book=book)
    return new_book


@router.put("/update_book/{book_id}", response_model=schemas.Book, status_code=201, tags=[Tags.books])
def update_book(*, book_id: int = Path(...), db: db_dependency, book: schemas.BookCreate, user: user_dependency):
    db_book = crud.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found...")
    elif db_book.user_id != user:
        raise HTTPException(status_code=401, detail="You are allowed to edit books that are only yours!")

    book_update_data = book.model_dump(exclude_unset=True)
    for field, value in book_update_data.items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/delete_book/{book_id}", response_model=List[schemas.Book], status_code=202, tags=[Tags.books])
def delete_book(*, book_id: int = Path(...), db: db_dependency, user: user_dependency):
    db_book = crud.get_book_by_id(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found...")
    elif db_book.user_id != user:
        raise HTTPException(status_code=401, detail="You are allowed to delete books that are only yours!")

    db.delete(db_book)
    db.commit()
    return crud.get_user_books(db, user)


@router.post("/express_interest/{book_id}", response_model=schemas.Book, status_code=201, tags=[Tags.books])
def express_interest_in_book(*, book_id: int = Path(..., ge=0), db: db_dependency, user: user_dependency):
    return crud.express_interest_in_book(db, book_id, user)
