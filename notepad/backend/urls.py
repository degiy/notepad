from django.urls import path

from . import views
from .views import DirListCreate,DirDetail,EntryListCreate,EntryDetail

urlpatterns = [
    path("", views.index, name="index"),
    path('dirs/', DirListCreate.as_view(), name='dir-list-create'),
    path('dir/<int:pk>/', DirDetail.as_view(), name='dir-detail'),
    path('entries/<int:dir_id>/', EntryListCreate.as_view(), name='entry-list-create'),
    path('entry/<int:pk>/', EntryDetail.as_view(), name='entry-detail'),

]