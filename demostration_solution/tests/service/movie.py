from unittest.mock import MagicMock

import pytest

from demostration_solution.dao.model.director import Director
from demostration_solution.dao.model.genre import Genre
from demostration_solution.dao.model.movie import Movie
from demostration_solution.dao.movie import MovieDAO
from demostration_solution.service.movie import MovieService
from demostration_solution.setup_db import db



@pytest.fixture()
def movie_dao_fixture():
    movie_dao = MovieDAO(db.session)

    d20 = Director(id=20, name="Toto")
    g15 = Genre(id=15, name="Tutu")

    corgy = Movie(id=1,
                  title="Lyagushka",
                  description="About lyagushka",
                  trailer="https://www.youtube.com/watch?v=UKei_d0cbP4",
                  year=2030,
                  rating=8.0,
                  genre=g15,
                  genre_id=15,
                  director=d20,
                  director_id=20)
    corgon = Movie(id=2,
                   title="Lyagushka2",
                   description="About next lyagushka",
                   trailer="https://www.youtube.com/watch?v=UKei_d0cbP5",
                   year=2032,
                   rating=2.0,
                   genre=g15,
                   genre_id=15,
                   director=d20,
                   director_id=20)

    movie_dao.get_one = MagicMock(return_value=corgy)
    movie_dao.get_all = MagicMock(return_value=[corgy, corgon])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao_fixture):
        self.movie_service = MovieService(dao=movie_dao_fixture)

    def test_partially_update(self):
        movie_d = {
        "id": 1,
        "year": 2030,
        }
        movie = self.movie_service.partially_update(movie_d)
        assert movie.year == movie_d.get("year")

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_d = {
        "id": 5,
        "title": "Lyagushka",
        "description": "About lyagushka",
        "trailer": "https://www.youtube.com/watch?v=UKei_d0cbP4",
        "year": 2030,
        "rating": 8.0,
        "genre_id": 15,
        "director_id": 20
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id != None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            "id": 2,
            "name": "Polly"
        }
        self.movie_service.update(movie_d)