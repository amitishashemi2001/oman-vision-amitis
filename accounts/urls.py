from django.urls import path
from .views import (AdminExpertListView, ExpertHomePageView, AdminHomePageView, ExpertProfileView, UserProfileView)

urlpatterns = [
    # مسیرهای مربوط به ادمین
    path('admin/homepage/', AdminHomePageView.as_view(), name='AdminHomePageView'),
    path('admin/expertlist/', AdminExpertListView.as_view(), name='AdminExpertListView'),
    path('admin/expert-profile/<int:pk>/', ExpertProfileView.as_view(), name='ExpertProfileView'),

    # مسیرهای مربوط به کارشناس
    path('expert/homepage/', ExpertHomePageView.as_view(), name='ExpertHomePageView'),

    # مسیر مربوط به پروفایل کاربر
    path('profile/', UserProfileView.as_view(), name='UserProfileView'),
]
