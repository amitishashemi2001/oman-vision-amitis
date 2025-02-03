from django.urls import path
from .views import (AdminMessageListCreateAPIView, ExpertMessageListCreateAPIView, MessageRecordsListAPIView,
                    MessageRecordCreateAPIView, MessageRecordRetrieveUpdateDestroyAPIView,
                    CloseMessageAPIView, SaveDeviceAPIView)

urlpatterns = [
    path('admin/', AdminMessageListCreateAPIView.as_view(), name='AdminMessageListCreateAPIView'),
    path('expert/', ExpertMessageListCreateAPIView.as_view(), name='ExpertMessageListCreateAPIView'),
    path('<int:pk>/records/', MessageRecordsListAPIView.as_view(), name='MessageRecordsListAPIView'),
    path('records/', MessageRecordCreateAPIView.as_view(), name='MessageRecordCreateAPIView'),
    path('records/<int:pk>', MessageRecordRetrieveUpdateDestroyAPIView.as_view(),
         name='MessageRecordRetrieveUpdateDestroyAPIView'),
    path('<int:pk>/close/', CloseMessageAPIView.as_view(), name='CloseMessageAPIView'),
    path('save-device/', SaveDeviceAPIView.as_view(), name='save_device'),
]
