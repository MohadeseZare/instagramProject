"""instagramProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='instagram API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('follow/', include('follow.urls')),
    path('scheduled-post/', include('scheduled_post.urls')),
    path('posts/', include('post.urls')),
    path('main-setting/', include('main_setting.urls')),
    path('login/', include('login.urls')),
    path('api-auth/', include('rest_framework.urls')),
    url(r'docs/', schema_view),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
