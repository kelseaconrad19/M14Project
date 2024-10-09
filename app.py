from flask import Flask
from flask_graphql import GraphQLView
import graphene
from movie_schema import MovieQuery, MovieMutation
from genre_schema import GenreQuery, GenreMutation
from model import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:JonJamLil24!@localhost/movie_db2"
db.init_app(app)

class Query(MovieQuery, GenreQuery, graphene.ObjectType):
    pass

class Mutation(MovieMutation, GenreMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

with app.app_context():
    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
