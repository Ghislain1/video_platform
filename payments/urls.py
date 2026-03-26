from videos.urls import urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:video_id>/', views.create_checkout_session, name='pay'),
    path('payment-success/', views.payment_success, name='success'),
    path('payment-cancel', views.payment_cancel, name='cancel'),
]