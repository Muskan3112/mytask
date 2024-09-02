from rest_framework.routers import DefaultRouter
from django.urls import path, include
from home import views

router = DefaultRouter()
router.register(r'', views.MyTaskView)

urlpatterns = [
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name='register'),
    path('', include(router.urls))
]
