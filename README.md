# Book_Giveaway_API

The Book Giveaway API is a RESTful web service that allows registered users to offer books for free and also take books that are offered by others.
Non authenticated users can also see the list of books, but can't show interest in them, or add their own books for the giveaway.

API does not support all the features given in the task - each book can have one user interested in it at a time. So book owner can't choose between different users to give the book to. 
This feature can be developer in the future, but for now (caused by lack of time and deadline) it is not supported.

Swagger documentation avaliable at - http://localhost:8000/docs

### Prerequisites

- Python 3.7+
- Pip (Python package manager)
- Virtualenv (optional but recommended)
- Docker and Docker Compose (optional, for containerized deployment)
