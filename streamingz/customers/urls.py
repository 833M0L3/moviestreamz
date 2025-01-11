from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_videos, name='all_videos'),
    path('signup/', views.user_signup, name='user_signup'),
    path('video/<int:video_id>/hls/', views.serve_hls_playlist, name='serve_hls_playlist'),
    path('video/<int:video_id>/hls/<str:segment_name>/', views.serve_hls_segment, name='serve_hls_segment'),
    path('video/player/<slug:video_id>/', views.hls_video_player, name='hls_video_player'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('plans/', views.choose_plan, name='plans'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('poor-users/', views.poor_users, name='poor_users'),
]
