from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new, name="new"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.cat_items, name="cat_items"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<str:name>", views.listing, name="listing")
]
