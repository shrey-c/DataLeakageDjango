from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.login_form),
	url(r'^assign', views.login_assign),
]