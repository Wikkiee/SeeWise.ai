from django.urls import path
from . import views

urlpatterns = [
    path("videos/",views.AllVideosListCreate.as_view(),name="all-video-list"),
    path("videos/get/<str:bucket_id>/",views.VideoByBucketIdAPIView.as_view(),name='get_video_by_id'),
    path("videos/retrive-and-upload/",views.VideoListCreate.as_view(),name="user-video-list"),
    path("videos/delete/<int:pk>/", views.VideoDelete.as_view(), name="video-delete"),
    path("videos/update/<int:pk>/", views.UpdateVideoTitleView.as_view(), name="video-title-update"),
    path("videos/search/<str:search_term>/",views.VideoSearchAPIView.as_view(),name="search-video-list"),

    path("truncate/", views.TruncateDatabase.as_view(), name="truncate-db"),
    path("videos/stream/", views.VideoStreamAPIView.as_view(), name="video-stream")

] 