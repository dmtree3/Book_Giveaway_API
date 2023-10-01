# Book_Giveaway_API

The Book Giveaway API is a RESTful web service that allows registered users to offer books for free and also take books that are offered by others.
Non-authenticated users can also see the list of books, but can't show interest in them, or add their own books for the giveaway.

API does not support all the features given in the task - each book can have one user interested in it at a time. So book owner can't choose between different users to give the book to. 
This feature can be developed in the future, but for now (caused by lack of time and deadline) it is not supported.

Swagger documentation available at - http://localhost:8000/docs

### Prerequisites

- Python 3.7+
- Pip (Python package manager)
- Virtualenv (optional but recommended)
- Docker and Docker Compose (optional, for containerized deployment)


### Installing Dependencies

Clone the repository:

   git clone https://github.com/dmtree3/Book_Giveaway_API.git

Navigate to the project directory:
  cd Book_Giveaway_API

Create a virtual environment
  python -m venv venv
  source venv/bin/activate  # On Windows, use venv\Scripts\activate

Install project dependencies:
   pip install -r requirements.txt
   

### Running the Application
Use the following command to run the FastAPI application: 
  uvicorn GiveAwayAPI.main:app --reload

### Deployment
The project can be deployed using Docker and Docker Compose. To build and run the containers, use:
  docker-compose up --build
