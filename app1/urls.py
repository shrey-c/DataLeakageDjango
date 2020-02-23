from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^userhome', views.userhome),
	url(r'^detectorhome', views.detectorhome),
	url(r'^changepassword', views.changepassword),
	url(r'^upload', views.modelformupload),
    url(r'^displayfiles', views.displayfiles),
	url(r'^checkdocument', views.checkdocument),
	url(r'^history', views.history),
	url(r'^deletefile', views.deletefile),
]