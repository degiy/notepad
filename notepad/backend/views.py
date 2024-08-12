from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import NDir, NEntry
from .serializers import DirSerializer, EntrySerializer, EntryNamesSerializer

def index(request):
    return HttpResponse("use api")



class DirListCreate(generics.ListCreateAPIView):
     queryset = NDir.objects.all()
     serializer_class = DirSerializer

class DirDetail(generics.RetrieveUpdateDestroyAPIView):
     serializer_class = DirSerializer
     queryset = NDir.objects.all()
 
class EntryListCreate(generics.ListCreateAPIView):
     serializer_class = EntryNamesSerializer

     def get_queryset(self):
         dir_id=self.kwargs.get('dir_id')
         if dir_id is not None:
            return NEntry.objects.filter(dir_ref=dir_id)
         return NEntry.objects.none()

class EntryDetail(generics.RetrieveUpdateDestroyAPIView):
     queryset = NEntry.objects.all()
     serializer_class = EntrySerializer

