"""SemanticMatching URL Configuration

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
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.views.generic import TemplateView
from Tester import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.userSigning),
    path('dashboard/', views.dashBoard),
    path('dashboard/testcreate', views.testCreation),
    path('dashboard/testhistory', views.testHistory),
    path('logout/', views.logOut),
    path('dashboard/appear', views.testAppear, name="appear"),
    path('dashboard/appear/<testId>', views.testAppear, name="appear"),
    path('dashboard/result/<testId>', views.loadTestDetails, name="result"),
    path('dashboard/result/<testId>/<user>', views.loadTestDetails, name="result"),
    path('dashboard/summary/<testId>', views.loadTestSummary, name="summary"),

]
