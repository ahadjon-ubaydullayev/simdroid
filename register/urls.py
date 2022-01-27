from django.urls import path
from register.views import index


urlpatterns = [
    path('api/', index, name='handler'),
    # path('detail/', detail, name='detail'),
]
