from django.shortcuts import render, get_object_or_404
from django.db.models import F, Sum, Max, Min, Count, Avg, Value
from movie_app.models import Movie, Director, Actor


# Create your views here.
def show_all_movie(request):
    # movies = Movie.objects.order_by(F("year").desc(nulls_first=True))
    movies = Movie.objects.annotate(
        true_bool=Value(True),
        false_bool=Value(False),
        new_budget=F("budget") + 100,
    )

    agg = movies.aggregate(Avg("budget"), Max("rating"), Min("rating"), Count("id"))

    # for movie in movies:
    #     movie.save()
    return render(request, "movie_app/all_movies.html", {
        "movies": movies,
        "agg": agg,
        "total": movies.count(),
    })


def show_one_movie(request, slug_movie: str):
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, "movie_app/one_movie.html", {
        "movie": movie,
    })


def show_directors(request):
    directors = Director.objects.annotate(
        true_bool=Value(True),
        false_bool=Value(False),
    )

    # for movie in movies:
    #     movie.save()
    return render(request, "movie_app/all_directors.html", {
        "directors": directors,

    })


def show_director(request, id_director: int):
    director = get_object_or_404(Director, id=id_director)
    return render(request, "movie_app/director.html", {
        "director": director
    })


def show_actors(request):
    actors = Actor.objects.annotate(
        true_bool=Value(True),
        false_bool=Value(False),
    )
    return render(request, "movie_app/all_actors.html", {
        "actors": actors,

    })


def show_actor(request, id_actor: int):
    actor = get_object_or_404(Actor, id=id_actor)
    return render(request, "movie_app/actor.html", {
        "actor": actor
    })
