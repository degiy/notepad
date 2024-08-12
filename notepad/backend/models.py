from django.db import models

# Create your models here.

class NDir(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class NEntry(models.Model):
    name = models.CharField(max_length=64)
    content = models.TextField()
    dir_ref = models.ForeignKey(NDir, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
