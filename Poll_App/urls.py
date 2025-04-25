from django.urls import path
from . import views
from django.views.generic import TemplateView

#Create your urls here.

app_name = 'Poll_App'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('detail/<int:question_id>/', views.detail_view, name='detail'),
    path('results/<int:question_id>/', views.results_view, name='results'),
    path('vote/<int:question_id>/', views.vote_view, name='vote'),
    path('create/', views.question_form, name='create'),
    path('update/<int:pk>/', views.question_update, name='update'),
    path('delete/<int:pk>/', views.question_delete, name='delete'),
]