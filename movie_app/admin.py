from django.contrib import admin, messages
from django.db.models import QuerySet

from .models import Movie, Director, Actor, DressingRoom

admin.site.register(Director)
admin.site.register(Actor)


# admin.site.register(DressingRoom)


@admin.register(DressingRoom)
class DressingRoom(admin.ModelAdmin):
    list_display = ["floor", "number", "actor"]


# from django.db.models import QuerySet
class RatingFilter(admin.SimpleListFilter):
    title = "Фильтр по рейтингу"
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ("<40", "Низкий"),
            ("от 40 до 59", "Средний"),
            ("от 60 до 79", "Высокий"),
            (">=80", "Высочайший"),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<40":
            return queryset.filter(rating__lt=40)
        elif self.value() == "от 40 до 59":
            return queryset.filter(rating__gte=40).filter(rating__lte=59)
        elif self.value() == "от 60 до 79":
            return queryset.filter(rating__gte=60).filter(rating__lte=79)
        elif self.value() == ">=80":
            return queryset.filter(rating__gte=80)

        return queryset


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # fields = []  # определять значения формы при создании записи (все включено по дефолту))
    # exclude = ["slug"]  # исключать значения из формы создания записи
    # readonly_fields = ["year"]    # нельзя изменять (только для чтения)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'rating', 'director', 'budget', 'rating_status']
    list_editable = ['rating', 'director', 'budget']
    filter_horizontal = ['actors']
    ordering = ["-rating", "-name"]
    actions = [
        'set_dollars',
        'set_euro'
    ]
    search_fields = ["name__startswith", "rating"]
    list_filter = ["name", "currency", RatingFilter]

    # list_per_page = 3
    @admin.display(ordering="rating", description="Статус")
    def rating_status(self, movie: Movie):
        if movie.rating < 50:
            return "Зачем это смотреть?!"
        elif movie.rating < 70:
            return "Разок можно глянуть"
        elif movie.rating <= 85:
            return "Зачет"
        else:
            return "Топчик"

    @admin.action(description="Установить валюту в доллар")
    def set_dollars(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.USD)
        self.message_user(request, f"Было обновлено - {count_updated} записей")

    @admin.action(description="Установить валюту в евро")
    def set_euro(self, request, qs: QuerySet):
        count_updated = qs.update(currency=Movie.EUR)
        self.message_user(request, f"Было обновлено - {count_updated} записей", messages.SUCCESS)
