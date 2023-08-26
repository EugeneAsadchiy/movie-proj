from . import views
from django.urls import path

urlpatterns = [
    path('', views.show_all_movie),
    path('movie/<slug:slug_movie>', views.show_one_movie, name="movie-detail"),
    path('directors/', views.show_directors, name="directors"),
    path('actors/', views.show_actors, name="actors"),
    path('directors/<int:id_director>', views.show_director, name="director-detail"),
    path('actors/<int:id_actor>', views.show_actor, name="actor-detail"),


]
