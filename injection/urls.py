from django.urls import path
from . import views_old
from . import views
"""path 장고 함수/ views요소 가져오기"""

urlpatterns = [
    path('view/', views.main, name='main'),
    path('retry/', views.retry, name='retry'),
    path('', views.index, name='index'),
]