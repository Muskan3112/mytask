from rest_framework.routers import DefaultRouter
from django.urls import path, include
from home import views

router = DefaultRouter()
router.register(r'category', views.CategoryView, basename='category')
router.register(r'mytask', views.MyTaskView, basename='mytask')
router.register(r'', views.TaskView,)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name='register'),
]
