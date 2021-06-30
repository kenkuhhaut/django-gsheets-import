from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView


##
## Configuration of the URL dispatcher
##
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='admin:index'), name='home'),
]
