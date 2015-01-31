from django.conf.urls import patterns, url

from social_network import views

urlpatterns = patterns('',

    # Main page URLS
    url(r'^$', views.index, name='index'),
    url(r'login/', views.log_in, name='log_in'),
    url(r'authenticate/', views.authentication, name='authentication'),
    url(r'create_account/', views.create_account, name='create_account'),
    url(r'new_account_success/', views.new_account_success, name='new_account_success'),
    url(r'job_search/', views.job_search, name='job_search'),
    url(r'search_backend/', views.job_search_backend, name='job_search_backend'),
    url(r'profile/', views.profile, name='profile'),
                       

                       
    url(r'logout/', views.log_out, name='log_out'),
                       



)
