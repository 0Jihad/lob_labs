"""mysites URL Configuration

The `urlpatterns` list  routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
#from django.contrib.auth import views as auth_views
import blogs.views as views
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.logins, name='blog_login'),
    path('log_out/', views.logout, name='blog_logout'),
    path('', include('blogs.urls')),
    path('blogs/', include('django.contrib.auth.urls')), # new
    path('profile/', views.update_profile, name='update_profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('password/', views.password, name='password'),
    path('home/?next=/settings/', views.settings, name='settings'),
    path('upload/', views.model_form_upload, name='model_form_upload'),
    path('student_reg/', views.StudentReg, name='student_reg'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),#$
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

##############################################myproject.views.SignupView.as_view()

