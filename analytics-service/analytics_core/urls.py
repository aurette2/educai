from django.contrib import admin
from django.urls import path, include
# from django.views.defaults import server_error
# from tracking.views import test_view
from tracking.views import test

urlpatterns = [
    path("admin/", admin.site.urls),
    path('tracking/', include('tracking.urls')),
    # path('test_vue/', test_view, name="test"),
    path('<str:page>/', test, name="test2"),
    # path('about/', about, name="about"),
]

