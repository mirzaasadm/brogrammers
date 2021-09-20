from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('',views.WelcomePage, name='welcomepage'),
	path("document/<pk>",views.document,name='documentpage'),
    path("editcontent",views.editcontent,name='editcontentpage'),
    path("editfilename",views.editfilename,name='editfilepage'),
    path("refreshdata",views.refreshdata,name='refreshpage'),
    path("download",views.downloadfile,name='downloadpage'),
]