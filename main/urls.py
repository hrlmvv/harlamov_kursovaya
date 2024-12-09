from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ArticleDetailView
from .views import NewsDetailView
from .views import CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('about/', views.about),
    path('news/', views.news, name='news'),
    path('articles/', views.articles),
    path('article/new/', views.create_article, name='create_article'),
    path('news/new/', views.create_news, name='create_news'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', views.search_results, name='search_results'),
    path('article/', views.article),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
