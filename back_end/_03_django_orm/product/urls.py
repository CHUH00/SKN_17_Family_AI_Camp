from django.urls import path
from product import views

app_name = 'product'

urlpatterns = [
    path('n_1/', views.test_n_1, name='test_n_1'),
    path('1_1/', views.test_1_1, name='test_1_1'),
    path('prefetch/', views.test_prefetch, name='test_prefetch'),
    path('n_m/', views.test_n_m, name='test_n_m'),
]
