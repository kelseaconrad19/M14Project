import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from model import Genre as GenreModel, Movie as MovieModel, db
from sqlalchemy.orm import Session
from movie_schema import Movie


class Genre(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel

class GenreQuery(graphene.ObjectType):
    genres = graphene.List(Genre)
    movies_by_genre = graphene.List(Movie, genre_id=graphene.Int(required=True))
    genre_by_movie = graphene.Field(Genre, movie_id=graphene.Int(required=True))

    def resolve_genres(self, info):
        return db.session.execute(db.select(GenreModel)).scalars()

    def resolve_movies_by_genre(self, info, genre_id):
        with Session(db.engine) as session:
            genre = session.execute(db.select(GenreModel).where(GenreModel.id == genre_id)).scalars().first()
            if genre:
                return genre.movies
            else:
                raise ValueError(f"Genre with ID {genre_id} does not exist.")

    def resolve_genre_by_movie(self, info, movie_id):
        with Session(db.engine) as session:
            movie = session.execute(db.select(MovieModel).where(MovieModel.id == movie_id)).scalars().first()
            if movie:
                return movie.genre
            else:
                raise ValueError(f"Movie with ID {movie_id} does not exist.")


class AddGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, name):
        if not name or len(name) > 55:
            raise ValueError("Genre name cannot be empty and must be under 55 characters.")

        with Session(db.engine) as session:
            with session.begin():
                genre = GenreModel(name=name)
                session.add(genre)
            session.refresh(genre)
            return AddGenre(genre=genre)


class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id, name):
        if not name or len(name) > 255:
            raise ValueError("Genre name cannot be empty and must be under 255 characters.")

        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel).where(GenreModel.id == id)).scalars().first()
                if genre:
                    genre.name = name
                else:
                    raise ValueError(f"Genre with ID {id} does not exist.")
            session.refresh(genre)
            return UpdateGenre(genre=genre)


class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    genre = graphene.Field(Genre)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                genre = session.execute(db.select(GenreModel).where(GenreModel.id == id)).scalars().first()
                if genre:
                    session.delete(genre)
                else:
                    raise ValueError(f"Genre with ID {id} does not exist.")
            return DeleteGenre(genre=genre)


class GenreMutation(graphene.ObjectType):
    add_genre = AddGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()