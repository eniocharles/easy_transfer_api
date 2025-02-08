from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomLoginView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
]
