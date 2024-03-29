"""internshipProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
import GovAnalysis.views as views

router = routers.DefaultRouter()
router.register(r'ent', views.EntityViewAPI, 'Entity')
router.register(r'entArt', views.EntitiesInArticleViewAPI, 'EntityInArticle')
router.register(r'art', views.ArticlesViewAPI, 'Articles')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('articlesList/', views.articlesList),
    path('entitiesOverv/', views.entitiesOverv),
    path('article/<str:id>', views.Article),
    path('list-of-articles/<int:page>', views.ListArticle),
    path('entity-overview/<str:id>', views.EntityOverview),
    path('api/', include(router.urls))
]
