from pydantic import BaseModel


class BookBase(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    condition: str | None = None
    pickup_location: str | None = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    user_id: int
    interested_user_id: int | None = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int | None = None
    hashed_password: str
    books: list[Book] = []
    interested_books: list[Book] = []

    class Config:
        from_attributes = True
