from rest_framework import serializers
from .models import NDir, NEntry

class DirSerializer(serializers.ModelSerializer):
    class Meta:
        model = NDir
        fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = NEntry
        fields = '__all__'

class EntryNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NEntry
        fields =['id','name'] 

# New Serializer for creating entries
class EntryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NEntry
        fields = ['name', 'dir_ref']
