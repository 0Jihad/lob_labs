# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 12:20:49 2018

@author: AdeolaOlalekan
"""

from django.urls import path, include
from .import views
urlpatterns = [path('user_home', views.home, name = 'user_home'), 
               path('post/post_list', views.post_list, name='post_list'),
               path('post/<int:pk>/', views.post_detail, name='post_detail'),
               path('post/new', views.post_new, name='post_new'),
               path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
               path('drafts/', views.post_draft_list, name='post_draft_list'),#post approvals
               path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),#review post uncomment for no review
               path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
               path('profile/<int:pk>/', views.update_profile, name='profile'),
               path('home/', views.home, name='home'),
               path('settings/', views.settings, name='settings'),
               path('password/', views.password, name='password'),
               path(r'^oauth/', include('social_django.urls', namespace='social')),
               path('search/', views.search, name='search'),
               path('login/', views.logins, name='blog_login'),
               path('log_out/', views.logout, name='blog_logout'),
               path('student_reg/', views.StudentReg, name='student_reg'),
               path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
               path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
              
               ]