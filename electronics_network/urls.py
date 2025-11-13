from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='api_root.html'), name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('electronics.urls')),
]