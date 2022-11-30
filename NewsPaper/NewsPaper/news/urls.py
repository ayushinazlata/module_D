from django.urls import path
from .views import (NewsList, NewList, NewsSearch, NewsCreate, NewsEdit, NewsDelete, CategoryList, subscribe,
                    delete_subscribe, upgrade_user)


urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewList.as_view(), name='new_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='new_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='new_delete'),
    path('categories/<int:pk>/', CategoryList.as_view(), name='category_news'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', delete_subscribe, name='delete_subscribe'),
    path('upgrade/', upgrade_user, name='account_upgrade'),
]
