from django.urls import path
from . import views

##### for django-ckeditor-5 ###########################
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
######################################################

urlpatterns=[
    path('', views.home,name='home'),
    path('projects', views.project_list,name='project_list'),
    path('project/<int:pk>/',views.project_view, name='project_view'),
    path('project/new/',views.project_new, name='project_new'),
    path('entry/<int:pk>/',views.entry_view, name='entry_view'),
    path('entry_info/',views.show_entry_info, name='show_entry_info'),
    path('entry/new/<int:pk>/',views.entry_new, name='entry_new'), #where pk is the identifier of the parent entry
    path('req/new/<int:pk>/',views.req_new, name='req_new'), #where pk is the identifier of the parent entry
    path('entry/edit/<int:pk>/', views.entry_edit,name='entry_edit'),
    path('signup/', views.signup, name='signup'),
    path('entry/publish/<int:pk>/', views.entry_publish, name='entry_publish'),
    path('learn/', views.learn, name='learn'),

    # path('post/<pk>/add_comment_to_post/', views.add_comment_to_post, name='add_comment_to_post'),

]

##### for django-ckeditor-5 ###########################
# urlpatterns += [
#     path("ckeditor5/", include('django_ckeditor_5.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
######################################################
