from django.urls import path

from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('logs', views.table_data, name='logs'),
    path('', views.loginPage, name='login'),
    path('rec_feed', views.recognizer_feed, name='rec_feed'),
    path('logout', views.logoutUser, name="logout")
]

urlpatterns += staticfiles_urlpatterns()