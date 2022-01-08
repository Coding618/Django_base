from django.urls import path
from apps.goods.views import IndexView, ListView, SKUSearchView

urlpatterns = [
    path('index/', IndexView.as_view()),
    path('list/<category_id>/skus/', ListView.as_view()),
    path('search/', SKUSearchView()),

]