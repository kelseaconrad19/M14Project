# Movie and Genre GraphQL API

## Project Overview

This project is a GraphQL API built with Flask, SQLAlchemy, and Graphene for managing movies and genres in a movie database. The API allows users to create, read, update, and delete both movies and genres, as well as retrieve information about relationships between movies and genres.

### Key Features:
- GraphQL endpoint for querying and mutating movie and genre data.
- CRUD operations for movies and genres.
- Relational database schema using SQLAlchemy, with movies and genres linked by a foreign key relationship.
- Integration with MySQL as the database backend.
- Flask as the web server to serve the GraphQL endpoint.

## Technologies Used
- **Python**: Main programming language.
- **Flask**: Lightweight web framework for serving the GraphQL API.
- **Graphene**: Python library for building GraphQL APIs.
- **SQLAlchemy**: ORM (Object Relational Mapper) to interact with the MySQL database.
- **MySQL**: Relational database to store movie and genre information.

## Setup Instructions

### Prerequisites
- Python 3.10+
- MySQL server
- MySQL connector library (`PyMySQL`)
- Virtual environment library (`venv`)

### Steps to Run the Application

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL Database**:
   - Create a database called `movie_db2`.
   - Update the connection string in `app.py` if necessary:
     ```python
     app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:<password>@localhost/movie_db2"
     ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   - The application will run at `http://localhost:5000/graphql`. You can use the `/graphql` endpoint to interact with the API.

6. **GraphiQL Interface**:
   - Visit `http://localhost:5000/graphql` to access the GraphiQL interface for testing queries and mutations.

## Example GraphQL Queries and Mutations

### 1. Add a New Genre
```graphql
mutation {
  addGenre(name: "Action") {
    genre {
      id
      name
    }
  }
}
```

### 2. Add a New Movie
```graphql
mutation {
  addMovie(
    title: "Inception"
    director: "Christopher Nolan"
    year: 2010
    genreId: 1
  ) {
    movie {
      id
      title
      director
      year
      genre {
        id
        name
      }
    }
  }
}
```

### 3. Retrieve All Genres
```graphql
query {
  genres {
    id
    name
  }
}
```

### 4. Retrieve Movies by Genre
```graphql
query {
  moviesByGenre(genreId: 1) {
    id
    title
    director
    year
  }
}
```

### 5. Update an Existing Genre
```graphql
mutation {
  updateGenre(id: 1, name: "Adventure") {
    genre {
      id
      name
    }
  }
}
```

### 6. Delete a Movie
```graphql
mutation {
  deleteMovie(id: 1) {
    movie {
      id
      title
    }
  }
}
```

## Project Structure
- **app.py**: Main application file that sets up Flask and GraphQL.
- **model.py**: Contains the SQLAlchemy models for `Movie` and `Genre`.
- **movie_schema.py**: Defines the GraphQL schema for movie queries and mutations.
- **genre_schema.py**: Defines the GraphQL schema for genre queries and mutations.
- **requirements.txt**: Lists all the Python dependencies for the project.

## Notes
- The database tables are recreated every time the server starts (`db.drop_all()` and `db.create_all()`). This is intended for development and testing. You should remove these lines for production to avoid losing data.
- Make sure to add some genres before attempting to add movies since each movie must be associated with an existing genre.

