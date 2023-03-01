from django.urls import path
from . import views
urlpatterns = [
    path('',views.HomeView,name='home'),
    path('scrape',views.scrapeview,name='scrape')
]