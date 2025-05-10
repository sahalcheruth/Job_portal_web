from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('job/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('post-job/', views.post_job_view, name='post_job'),
    path('apply/<int:job_id>/', views.apply_job_view, name='apply_job'),
    path('my-applications/', views.employer_applications_view, name='employer_applications'),
    path('jobs/',views.home_view,name='job_list'),
    path('my-applied-jobs/', views.my_applied_jobs_view, name='my_applied_jobs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


