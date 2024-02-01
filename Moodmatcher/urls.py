# Moodmatcher/urls.py

from django.urls import path
from . import views
from .views import image_upload_recommend
from .views import my_profile
from .views import post_like

urlpatterns = [
    path('community/', views.community, name='community'),
    path('customer-service/', views.customer_service, name='customer_service'),
    path('post/<int:post_id>/like/', post_like, name='post_like'),  # 수정된 부분
    path('<str:category>/post/create/community/', views.post_create, name='post_create'),
    path('<str:category>/post/create/customer-service/', views.post_create_customer_service, name='post_create_customer_service'),
    path('<str:category>/post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('<str:category>/post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('<str:category>/post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('<str:category>/post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('image_upload_recommend/', image_upload_recommend, name='image_upload_recommend'),
    path('my_profile/', my_profile, name='my_profile'),
]
