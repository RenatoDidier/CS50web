from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("mylist", views.mylist, name="mylist"),
    path("product/<str:id>/<str:title>", views.list, name="list"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("rmv_comment", views.rmv_comment, name="rmv_comment"),
    path("editcomment", views.editcomment, name="editcomment"),
    path("editlist/<str:id_list>", views.editlist, name="editlist"),
]
