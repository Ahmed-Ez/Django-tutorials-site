from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('tutorial/<int:tutorial_id>',views.tutorial,name='tutorial'),
    path("register/",views.register,name="register"),
    path("logout",views.logout_request,name="logout"),
    path("login",views.login_request,name="login"),
    path("search",views.search_results,name="search")
]
