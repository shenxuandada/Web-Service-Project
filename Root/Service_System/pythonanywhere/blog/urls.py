from django.urls import path, include
from . import views
from rest_framework import routers

from .views import ImageListView  #12.14xintianjia
from .views import upload_detection_data

router=routers.DefaultRouter()
router.register('Post', views.BlogImages)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('js_test/', views.js_test, name='js_test'),
    path('api_root/', include(router.urls)),
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls')),
    path('login/', views.user_login, name='login'),   #12.14xintianjia
    path('api/images/', ImageListView.as_view(), name='image_list'), #12.14xintianjia
    path('api/upload_detection/', upload_detection_data, name='upload_detection'),
]